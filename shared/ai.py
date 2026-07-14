"""Thin AI wrapper used by all prototypes.

Priority: ANTHROPIC_API_KEY (Claude) -> OPENAI_API_KEY (GPT) -> None.
When no key is present, prototypes fall back to deterministic templates and
label the output "[template mode]" — the same pattern I use in internal
automations so the pipeline degrades gracefully instead of failing.
Stdlib only; no packages to install.
"""
import json
import os
import urllib.request

ANTHROPIC_MODEL = os.environ.get("AI_MODEL", "claude-sonnet-4-5")
OPENAI_MODEL = os.environ.get("AI_MODEL", "gpt-4o")


def generate(prompt: str, system: str = "", max_tokens: int = 1200) -> str | None:
    """Return AI text, or None if no API key is configured."""
    if os.environ.get("ANTHROPIC_API_KEY"):
        return _anthropic(prompt, system, max_tokens)
    if os.environ.get("OPENAI_API_KEY"):
        return _openai(prompt, system, max_tokens)
    return None


def provider() -> str:
    if os.environ.get("ANTHROPIC_API_KEY"):
        return f"Claude ({ANTHROPIC_MODEL})"
    if os.environ.get("OPENAI_API_KEY"):
        return f"GPT ({OPENAI_MODEL})"
    return "template mode (no API key set)"


def _post(url: str, headers: dict, body: dict) -> dict:
    req = urllib.request.Request(
        url, data=json.dumps(body).encode(), headers=headers, method="POST"
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read())


def _anthropic(prompt, system, max_tokens):
    data = _post(
        "https://api.anthropic.com/v1/messages",
        {
            "content-type": "application/json",
            "x-api-key": os.environ["ANTHROPIC_API_KEY"],
            "anthropic-version": "2023-06-01",
        },
        {
            "model": ANTHROPIC_MODEL,
            "max_tokens": max_tokens,
            "system": system or "You are a helpful assistant.",
            "messages": [{"role": "user", "content": prompt}],
        },
    )
    return "".join(b["text"] for b in data["content"] if b["type"] == "text")


def _openai(prompt, system, max_tokens):
    data = _post(
        "https://api.openai.com/v1/chat/completions",
        {
            "content-type": "application/json",
            "authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
        },
        {
            "model": OPENAI_MODEL,
            "max_tokens": max_tokens,
            "messages": [
                {"role": "system", "content": system or "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
        },
    )
    return data["choices"][0]["message"]["content"]
