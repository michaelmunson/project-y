from dotenv import load_dotenv
from anthropic import Anthropic
from src.prompts import create_prompt
import sys

load_dotenv()

client = Anthropic()

prompt = create_prompt(sys.argv[1], [
  {
    "id": "TICKET-123",
    "description": "Fetching a list of 5 items to analyze their sales data. This will provide the base data needed for the analysis.",
    "status": "COMPLETED"
  }
])

response = client.messages.create(
  max_tokens=1024,
  system=prompt['system'],
  messages=prompt['messages'],
  model="claude-3-7-sonnet-latest",
)

print("\n".join([(msg.text if msg.type == "text" else "") for msg in response.content]))