"""
pka/decorators.py

Decorators used across NoteStore to add cross-cutting behavior
(logging, timing) without touching the core business logic.
"""

import functools
import time
import anthropic
import logging

logger = logging.getLogger(__name__)


def log_calls(level="INFO"):
    """
    Decorator factory: logs before/after a function call, at the given level.
    ...
    """
    log_level = getattr(logging, level.upper())  # "INFO" -> logging.INFO (an int)

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger.log(log_level, "Calling %s()", func.__name__)
            result = func(*args, **kwargs)
            logger.log(log_level, "%s() finished", func.__name__)
            return result
        return wrapper
    return decorator


def timed(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        logger.debug("%s() took %.4fs", func.__name__, elapsed)
        return result
    return wrapper


def retry(max_attempts: int = 3, backoff_base: float = 1.0):
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
                        logger.error(
                            "%s failed permanently after %d attempts (%s)",
                            func.__name__, max_attempts, e.__class__.__name__,
                        )
                        raise
                    wait = backoff_base * (2 ** (attempt - 1))
                    logger.warning(
                        "%s failed (%s), attempt %d/%d. Retrying in %ss...",
                        func.__name__, e.__class__.__name__, attempt, max_attempts, wait,
                    )
                    time.sleep(wait)
                    attempt += 1
        return wrapper
    return decorator