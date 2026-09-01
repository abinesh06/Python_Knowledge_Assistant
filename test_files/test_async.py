# test_files/test_async_summarize.py
import asyncio
from pka.llm_client import summarize_note_async

async def main():
    result = await summarize_note_async("Bought milk, eggs, and bread. Also need to call the plumber about the leak.")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())