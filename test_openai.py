import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

print(
    "API key loaded:",
    bool(api_key)
)


client = OpenAI(
    api_key=api_key
)


response = client.responses.create(
    model="gpt-5.6-luna",
    input="Reply with exactly: OpenAI connection works."
)


print(
    response.output_text
)