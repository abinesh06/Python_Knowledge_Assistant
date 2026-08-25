from unittest.mock import Mock
import pytest
from anthropic import RateLimitError, APITimeoutError, APIConnectionError, AuthenticationError

from pka.llm_client import summarize_note, ask_note


def make_fake_response(text: str):
    """Builds a Mock that looks like a real Anthropic API response object."""
    fake_block = Mock()
    fake_block.text = text

    fake_response = Mock()
    fake_response.content = [fake_block]
    return fake_response


def test_summarize_note_returns_mocked_summary(monkeypatch):
    """summarize_note() should return exactly what the (mocked) API responds with,
    without making any real network call."""
    fake_response = make_fake_response("This is a fake summary.")
    mock_create = Mock(return_value=fake_response)

    monkeypatch.setattr("pka.llm_client.client.messages.create", mock_create)

    result = summarize_note("Some long note content about Python decorators.")

    assert result == "This is a fake summary."
    mock_create.assert_called_once()

def test_retry_recovers_from_rate_limit(monkeypatch):
    """@retry should retry on RateLimitError and return the result once
    a later attempt succeeds — proving the decorator, not just the function."""

    # Kill the real sleep so this test runs instantly
    monkeypatch.setattr("pka.decorators.time.sleep", Mock())

    fake_success = make_fake_response("Summary after retry.")

    fake_http_response = Mock()
    fake_http_response.status_code = 429

    call_count = 0

    def flaky_create(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise RateLimitError(
                "rate limited",
                response=fake_http_response,
                body={"error": {"message": "rate limited"}},
            )
        return fake_success

    monkeypatch.setattr("pka.llm_client.client.messages.create", flaky_create)

    result = summarize_note("Some note content.")

    assert call_count == 3
    assert result == "Summary after retry."

def test_retry_does_not_retry_authentication_error(monkeypatch):
    """@retry should NOT retry AuthenticationError — it should raise
    immediately, since a bad API key won't fix itself on attempt 2."""

    monkeypatch.setattr("pka.decorators.time.sleep", Mock())

    fake_http_response = Mock()
    fake_http_response.status_code = 401

    call_count = 0

    def always_fails(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        raise AuthenticationError(
            "invalid api key",
            response=fake_http_response,
            body={"error": {"message": "invalid api key"}},
        )

    monkeypatch.setattr("pka.llm_client.client.messages.create", always_fails)

    with pytest.raises(AuthenticationError):
        summarize_note("Some note content.")

    assert call_count == 1

def test_retry_exhausts_all_attempts_then_raises(monkeypatch):
    """@retry should attempt exactly max_attempts times on persistent
    RateLimitError, then give up and raise — not retry forever."""

    monkeypatch.setattr("pka.decorators.time.sleep", Mock())

    fake_http_response = Mock()
    fake_http_response.status_code = 429

    call_count = 0

    def always_rate_limited(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        raise RateLimitError(
            "rate limited",
            response=fake_http_response,
            body={"error": {"message": "rate limited"}},
        )

    monkeypatch.setattr("pka.llm_client.client.messages.create", always_rate_limited)

    with pytest.raises(RateLimitError):
        summarize_note("Some note content.")

    assert call_count == 3  # matches max_attempts=3 on summarize_note