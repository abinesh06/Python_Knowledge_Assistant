"""
LLM integration layer for the Personal Knowledge Assistant.
Wraps the Anthropic API so the rest of the app (CLI, note operations)
never has to know about request/response shapes or the API key directly.
"""

import os
from dotenv import load_dotenv
from anthropic import Anthropic
from pka.decorators import retry, log_calls, timed

# Load environment variables (ANTHROPIC_API_KEY) from .env
load_dotenv(override=True)

# Created once at import time, reused by every function in this module.
# Mirrors a Connected System: configure the connection once, call it many times.
client = Anthropic()

MODEL = "claude-sonnet-4-5"


@retry(max_attempts=3, backoff_base=1)
@timed
@log_calls()
def summarize_note(note_content: str) -> str:
    """
    Send a note's content to Claude and return a concise summary.

    Args:
        note_content: The raw text of the note to summarize.

    Returns:
        A plain-text summary string.

    Raises:
        ValueError: If note_content is empty or whitespace-only.
    """
    if not note_content or not note_content.strip():
        raise ValueError("Cannot summarize empty note content.")

    response = client.messages.create(
        model=MODEL,
        max_tokens=300,
        messages=[
            {
                "role": "user",
                "content": (
                    "Summarize the following note in 2-3 concise sentences. "
                    "Focus on the key points only.\n\n"
                    f"Note:\n{note_content}"
                ),
            }
        ],
    )

    return response.content[0].text



@retry(max_attempts=3, backoff_base=1)
@timed
@log_calls()
def ask_note(note_content: str, question: str) -> str:
    """
    Answer a question about a note's content using Claude.

    Args:
        note_content: The raw text of the note to use as context.
        question: The user's question about that note.

    Returns:
        A plain-text answer string, grounded in the note content.

    Raises:
        ValueError: If note_content or question is empty or whitespace-only.
    """
    if not note_content or not note_content.strip():
        raise ValueError("Cannot answer a question about empty note content.")
    if not question or not question.strip():
        raise ValueError("Question cannot be empty.")

    response = client.messages.create(
        model=MODEL,
        max_tokens=500,
        messages=[
            {
                "role": "user",
                "content": (
                    "Answer the following question using ONLY the information "
                    "in the note below. If the note doesn't contain enough "
                    "information to answer, say so explicitly.\n\n"
                    f"Note:\n{note_content}\n\n"
                    f"Question: {question}"
                ),
            }
        ],
    )

    return response.content[0].text