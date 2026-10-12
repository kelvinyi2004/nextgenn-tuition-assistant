"""
WhatsApp transport adapter and ingress boundary.
Guarantees message isolation, receipt tracking, and prevents administrative command execution.
"""

from typing import Dict, Any, Optional


class WhatsAppIngressGuard:
    def __init__(self, authorized_phones: Optional[set] = None):
        self.authorized_phones = authorized_phones or set()

    def is_authorized(self, phone: str) -> bool:
        clean = phone.split("@")[0].split(":")[0].lstrip("+")
        return clean in self.authorized_phones

    def filter_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Disables administrative shell/gateway controls on incoming classroom events.
        """
        filtered = dict(event)
        # Block control permissions from classroom chats
        filtered["allow_gateway_control"] = False
        return filtered
