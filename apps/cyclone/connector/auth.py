"""Authentication and Authorization for Agent Connections."""

import hashlib
import hmac
import json
import os
import secrets
import time
from typing import Any, Dict


class AuthManager:
    """Manages authentication and authorization for agent connections."""

    def __init__(self, auth_file: Optional[str] = None):
        self.auth_file = auth_file or os.path.expanduser("~/.hermes/agent_auth.json")
        self.agents: Dict[str, Dict[str, Any]] = {}
        self._load()

    def _load(self) -> None:
        """Load auth data from disk."""
        try:
            if os.path.exists(self.auth_file):
                with open(self.auth_file) as f:
                    self.agents = json.load(f)
        except Exception:
            self.agents = {}

    def _save(self) -> None:
        """Save auth data to disk."""
        with open(self.auth_file, "w") as f:
            json.dump(self.agents, f, indent=2)

    def generate_token(self, agent_name: str, scope: str = "network.agent") -> str:
        """Generate a secure token for an agent."""
        token = secrets.token_urlsafe(32)
        self.agents[agent_name] = {
            "token_hash": hashlib.sha256(token.encode()).hexdigest(),
            "scope": scope,
            "created_at": time.time(),
            "expires_at": time.time() + 3600,  # 1 hour
        }
        self._save()
        return token

    def validate_token(self, agent_name: str, token: str) -> bool:
        """Validate an agent token."""
        if agent_name not in self.agents:
            return False
        stored_hash = self.agents[agent_name].get("token_hash", "")
        return hmac.compare_digest(
            stored_hash, hashlib.sha256(token.encode()).hexdigest()
        )

    def check_scope(self, agent_name: str, required_scope: str) -> bool:
        """Check if agent has required scope."""
        if agent_name not in self.agents:
            return False
        return required_scope in self.agents[agent_name].get("scope", "")

    def check_permission(self, agent_name: str, action: str, resource: str) -> bool:
        """Check if agent has permission for action+resource."""
        allowed = {
            ("read", "config"): True,
            ("read", "memory"): True,
            ("write", "config"): False,
            ("execute", "task"): False,
        }
        return allowed.get((action, resource), False)
