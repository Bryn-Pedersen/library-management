import argparse
import json
import os
import sys
from typing import Any, Dict, List

from dotenv import load_dotenv
from openai import OpenAI


PROMPT = """You are a helpful assistant generating structured synthetic book data.
Return ONLY a valid JSON array. Each element must be an object with:
- title: string
- author: string
- genre: string
- average_rating: number between 1.0 and 5.0
- isbn: 13-digit string
- language_code: string like 'en'
- rating_count: integer

Generate exactly {count} items, realistic and varied. No prose, no backticks, JSON array only.
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate synthetic book data via OpenAI")
    parser.add_argument("--count", type=int, default=1, help="Number of books to generate")
    parser.add_argument("--model", default="gpt-4o-mini", help="OpenAI model to use")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("OPENAI_API_KEY is not set. Set it in your environment or .env file.", file=sys.stderr)
        sys.exit(1)

    client = OpenAI(api_key=api_key)
    prompt = PROMPT.format(count=args.count)

    completion = client.chat.completions.create(
        model=args.model,
        messages=[
            {"role": "system", "content": "You produce strictly valid JSON only."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
    )

    content = completion.choices[0].message.content.strip()
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        print("The model did not return valid JSON. Raw output:", file=sys.stderr)
        print(content, file=sys.stderr)
        sys.exit(2)

    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()


