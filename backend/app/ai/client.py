"""Anthropic Haiku client for flavor text and narration."""

import anthropic
from ..config import ANTHROPIC_API_KEY, AI_MODEL, AI_MAX_TOKENS

_client = None


def get_client() -> anthropic.Anthropic | None:
    global _client
    if not ANTHROPIC_API_KEY:
        return None
    if _client is None:
        _client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    return _client


async def call_haiku(system_prompt: str, user_prompt: str) -> str | None:
    """Call Haiku and return the response text. Returns None on failure."""
    client = get_client()
    if not client:
        return None
    try:
        message = client.messages.create(
            model=AI_MODEL,
            max_tokens=AI_MAX_TOKENS,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
        return message.content[0].text.strip()
    except Exception:
        return None
