"""
pka/decorators.py

Decorators used across NoteStore to add cross-cutting behavior
(logging, timing) without touching the core business logic.
"""

import functools
import time
import anthropic


def log_calls(level="INFO"):
    """
    Decorator factory: logs before/after a function call, at the given level.

    Usage:
        @log_calls(level="DEBUG")
        def search(...): ...

    Note: always call with parentheses, e.g. @log_calls() or
    @log_calls(level="WARNING") — never bare @log_calls, since this
    is a factory (Layer 1) that must run first to produce the real
    decorator (Layer 2).
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(f"[{level}] Calling {func.__name__}()")
            result = func(*args, **kwargs)
            print(f"[{level}] {func.__name__}() finished")
            return result
        return wrapper
    return decorator


def timed(func):
    """
    Decorator: prints how long a function took to execute.

    Plain decorator (2 layers, no factory) since it takes no
    configuration — nothing needs a separate resolution stage.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"⏱ {func.__name__}() took {elapsed:.4f}s")
        return result
    return wrapper


def retry(max_attempts: int = 3, backoff_base: float = 1.0):
    """Retry a function on transient Claude API errors, with exponential backoff."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 1
            while True:
                try:
                    return func(*args, **kwargs)
                except (anthropic.RateLimitError,
                        anthropic.APITimeoutError,
                        anthropic.APIConnectionError) as e:
                    if attempt >= max_attempts:
                        raise  # out of attempts, let it fail for real
                    wait = backoff_base * (2 ** (attempt - 1))
                    print(f"[retry] {func.__name__} failed "
                          f"({e.__class__.__name__}), attempt {attempt}/{max_attempts}. "
                          f"Retrying in {wait}s...")
                    time.sleep(wait)
                    attempt += 1
        return wrapper
    return decorator