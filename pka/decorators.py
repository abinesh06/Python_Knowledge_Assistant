"""
pka/decorators.py

Decorators used across NoteStore to add cross-cutting behavior
(logging, timing) without touching the core business logic.
"""

import functools
import time


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