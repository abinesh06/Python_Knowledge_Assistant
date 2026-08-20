"""
Scratch script for Week 6 Day 2: exploring the Claude API request/response
shape and error handling. Not part of the pka package — throwaway once
today's concepts have landed.
"""

import os
from dotenv import load_dotenv
import anthropic

# Load ANTHROPIC_API_KEY from .env into the environment.
# The anthropic.Anthropic() client (below) reads this env var automatically —
# we don't pass the key in directly, same pattern as Day 1.
load_dotenv(override=True)


def show_successful_response():
    """Send a real request and print the full response shape."""

    client = anthropic.Anthropic()

    # This is the request payload from today's theory:
    # - messages: the conversation so far, as a list of role/content dicts
    # - model: which Claude model answers
    # - max_tokens: the CEILING on reply length, not a target
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=200,
        messages=[
            {
                "role": "user",
                "content": "In one sentence, what is SQLite?",
            }
        ],
    )

    print("--- SUCCESSFUL RESPONSE ---")

    # .content is a LIST of content blocks, not a string.
    # For a plain text reply, there's normally exactly one block.
    print("Raw .content:", response.content)
    print("Reply text:", response.content[0].text)

    # Why generation stopped. "end_turn" = Claude finished naturally.
    # "max_tokens" would mean the reply got cut off by our ceiling.
    print("stop_reason:", response.stop_reason)

    # Token usage — useful later for cost tracking.
    print("usage:", response.usage)
    print()


def trigger_401():
    """Deliberately use an invalid API key to see AuthenticationError fire."""

    # Passing a bad key directly overrides the env var, so this client
    # is intentionally broken — just for this one call.
    bad_client = anthropic.Anthropic(api_key="sk-ant-invalid-test-key")

    print("--- TRIGGERING 401 ---")
    try:
        bad_client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=50,
            messages=[{"role": "user", "content": "Hello"}],
        )
    except anthropic.AuthenticationError as e:
        # 401: the key itself is wrong. Retrying won't help —
        # this is a "your code/config is wrong" error, not a transient one.
        print(f"Caught AuthenticationError (401): {e}")
    print()


def trigger_400():
    """Deliberately send an empty messages list to see BadRequestError fire."""

    client = anthropic.Anthropic()

    print("--- TRIGGERING 400 ---")
    try:
        client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=50,
            messages=[],  # invalid — Claude needs at least one message
        )
    except anthropic.BadRequestError as e:
        # 400: the request itself is malformed. Same category as 401 —
        # retrying the identical request will fail identically every time.
        print(f"Caught BadRequestError (400): {e}")
    print()


if __name__ == "__main__":
    show_successful_response()
    trigger_401()
    trigger_400()