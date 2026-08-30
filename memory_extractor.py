import os

from dotenv import load_dotenv
from openai import OpenAI


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError(
        "OPENAI_API_KEY not found in .env file"
    )


# ============================================================
# OPENAI CLIENT
# ============================================================

client = OpenAI(
    api_key=api_key
)


# ============================================================
# MEMORY EXTRACTION
# ============================================================

def extract_memory(user_message):

    prompt = f"""
You are a memory extraction system for SIRA
(Sid's Intelligent Resource Assistant).

Analyze the user's message below.

Determine whether it contains information
that would be useful for SIRA to remember
about the user.

Useful memories may include:

- Interview experiences
- Things the user struggled with
- Career goals
- Learning goals
- Important decisions
- Project information
- Preferences
- Long-term plans
- Important personal context

Do NOT store:

- Casual conversation
- Greetings
- Generic questions
- Temporary information
- Facts unrelated to the user

If there is no useful memory, return exactly:

NONE

Otherwise return exactly:

TYPE: <memory type>
MEMORY: <one concise memory>

USER MESSAGE:

{user_message}
"""

    response = client.responses.create(
        model="gpt-5.6-luna",
        input=prompt
    )

    return response.output_text.strip()