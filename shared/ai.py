"""Thin AI wrapper used by all prototypes.

Priority: ANTHROPIC_API_KEY (Claude API) -> OPENAI_API_KEY (GPT) ->
Claude Code CLI (`claude -p`, e.g. Bedrock-hosted) -> None.
When no provider is available, prototypes fall back to deterministic
templates and label the output "[template mode]" — the same pattern I use in
internal automations so the pipeline degrades gracefully instead of failing.
Stdlib only; no packages to install.
"""
import json
import os
import shutil
import subprocess
import urllib.request

ANTHROPIC_MODEL = os.environ.get("AI_MODEL", "claude-sonnet-4-5")
OPENAI_MODEL = os.environ.get("AI_MODEL", "gpt-4o")


def generate(prompt: str, system: str = "", max_tokens: int = 1200) -> str | None:
    """Return AI text, or None if no provider is available."""
    if os.environ.get("ANTHROPIC_API_KEY"):
        return _anthropic(prompt, system, max_tokens)
    if os.environ.get("OPENAI_API_KEY"):
        return _openai(prompt, system, max_tokens)
    if shutil.which("claude"):
        return _claude_cli(prompt, system)
    return None


def provider() -> str:
    if os.environ.get("ANTHROPIC_API_KEY"):
        return f"Claude API ({ANTHROPIC_MODEL})"
    if os.environ.get("OPENAI_API_KEY"):
        return f"GPT ({OPENAI_MODEL})"
    if shutil.which("claude"):
        return "Claude Code CLI (print mode)"
    return "template mode (no AI provider available)"


def _claude_cli(prompt: str, system: str) -> str | None:
    """Generate via the locally installed Claude Code CLI in print mode.

    Uses whatever backend the CLI is configured for (Anthropic account or
    AWS Bedrock) — handy when the machine has Claude Code but no raw API key.
    """
    cmd = ["claude", "-p", "--output-format", "text"]
    if system:
        cmd += ["--system-prompt", system]
    try:
        result = subprocess.run(
            cmd, input=prompt, capture_output=True, text=True, timeout=300
        )
    except (subprocess.TimeoutExpired, OSError):
        return None
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


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
