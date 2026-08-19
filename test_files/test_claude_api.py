from dotenv import load_dotenv
from anthropic import Anthropic

# Load variables from .env into the environment
load_dotenv()

# Client auto-detects ANTHROPIC_API_KEY from the environment - no need to pass it manually
client = Anthropic()

print(client.api_key)
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=200,
    messages=[
        {"role": "user", "content": "In one sentence, what does a REST API do?"}
    ]
)

print(response)