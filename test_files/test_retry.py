from pka.decorators import retry
import anthropic

attempt_count = 0

@retry(max_attempts=3, backoff_base=0.5)
def flaky_function():
    global attempt_count
    attempt_count += 1
    if attempt_count < 3:
        raise anthropic.APITimeoutError("simulated timeout")
    return "success!"

result = flaky_function()
print(f"Result: {result}")
print(f"Took {attempt_count} attempts")