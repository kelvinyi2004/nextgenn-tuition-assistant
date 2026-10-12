"""
Security and sanitization engine for Tuition Assistant.
Enforces strict redaction of credentials, server paths, and injection commands.
"""

import re

# Detect API keys, tokens, JWTs, and private keys
PRIVATE_MATERIAL = re.compile(
    r"\b(?:sk-(?:proj-|ant-)?[A-Za-z0-9_-]{12,}|AIza[A-Za-z0-9_-]{20,}|gh[pousr]_[A-Za-z0-9]{12,})\b"
    r"|\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\b"
    r"|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"
    r"|\bBearer\s+[A-Za-z0-9._~+/-]{8,}"
    r"|[\"']?\b(?:api[_ -]?key|access[_ -]?token|refresh[_ -]?token|client[_ -]?secret|password|session[_ -]?cookie)[\"']?\s*[:=]\s*[\"']?\S{4,}",
    re.I,
)

# Detect internal file system paths and localhost URLs
PRIVATE_PATH = re.compile(
    r"(?:/Users/|/home/|~?/\.hermes/|(?<![A-Za-z0-9])(?:config\.yaml|creds\.json|\.env)(?![A-Za-z0-9])|(?:https?://)?(?:127\.0\.0\.1|localhost)(?::\d+)?)",
    re.I,
)

# Detect command injection mentions
COMMAND_MENTION = re.compile(r"(?<![\w/])[/／][a-zA-Z][a-zA-Z0-9_-]*")


def contains_sensitive_data(text: str) -> bool:
    """Returns True if text contains private credentials or local path disclosures."""
    if not text:
        return False
    return bool(PRIVATE_MATERIAL.search(text) or PRIVATE_PATH.search(text))


def sanitize_text(text: str) -> str:
    """Replaces sensitive tokens and server paths with redacted placeholders."""
    if not text:
        return ""
    cleaned = PRIVATE_MATERIAL.sub("[REDACTED_CREDENTIAL]", text)
    cleaned = PRIVATE_PATH.sub("[REDACTED_PATH]", cleaned)
    return cleaned


def has_command_injection(text: str) -> bool:
    """Checks whether the text attempts to invoke bot/system slash commands."""
    if not text:
        return False
    return bool(COMMAND_MENTION.search(text))
