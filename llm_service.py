"""
LLM Service
-----------
Thin wrapper around the OpenRouter API using openai/gpt-4o-mini.
Reads OPENROUTER_API_KEY from environment (or a .env file).

Run standalone: python llm_service.py
"""

import os
import httpx
from dotenv import load_dotenv  # pip install python-dotenv

load_dotenv()  # Reads .env in the project root if present

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "openai/gpt-4o-mini"


def ask_llm(
    prompt: str,
    system_prompt: str = "You are a helpful assistant for a quick-commerce grocery platform.",
    model: str = DEFAULT_MODEL,
) -> str:
    """
    Send a prompt to the LLM via OpenRouter and return the text response.

    Args:
        prompt:        The user message / question.
        system_prompt: Optional system context (defaults to a commerce assistant).
        model:         OpenRouter model identifier.

    Returns:
        The assistant's reply as a plain string.

    Raises:
        ValueError: If the API key is missing.
        httpx.HTTPStatusError: On non-2xx HTTP responses.
    """
    if not OPENROUTER_API_KEY:
        raise ValueError(
            "OPENROUTER_API_KEY is not set. "
            "Add it to your .env file or export it as an environment variable."
        )

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        # OpenRouter recommends these headers for attribution
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "HyperLocal QCommerce",
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": prompt},
        ],
    }

    response = httpx.post(OPENROUTER_URL, json=payload, headers=headers, timeout=30)
    response.raise_for_status()

    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


# ── Convenience helpers ───────────────────────────────────────────────────────

def suggest_alternatives(product_name: str) -> str:
    """Ask the LLM to suggest substitute products."""
    prompt = f"Suggest 3 alternative products for '{product_name}' in a grocery store. Be concise."
    return ask_llm(prompt)


def summarize_order(items: list[dict]) -> str:
    """Ask the LLM to produce a friendly order summary."""
    item_lines = "\n".join(f"- {i['product_name']} × {i['quantity']}" for i in items)
    prompt = f"Summarize this grocery order in one friendly sentence:\n{item_lines}"
    return ask_llm(prompt)


# ── Standalone test ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    test_prompt = "What are the top 3 selling grocery items in South India?"
    print(f"Prompt: {test_prompt}\n")

    try:
        reply = ask_llm(test_prompt)
        print("LLM response:\n", reply)
    except ValueError as e:
        print(f"[Config error] {e}")
    except httpx.HTTPStatusError as e:
        print(f"[API error] {e.response.status_code}: {e.response.text}")
