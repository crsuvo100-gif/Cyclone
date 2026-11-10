"""Agent Registry - Discovery and Management."""

import json
import os
import time
from typing import Any, Dict, List, Optional
from pathlib import Path


class AgentRegistry:
    """Manages agent registration and discovery."""

    def __init__(self, registry_path: Optional[str] = None):
        self.registry_path = registry_path or os.path.expanduser("~/.hermes/agent_registry.json")
        self.agents: Dict[str, Dict[str, Any]] = {}
        self._load()

    def _load(self) -> None:
        """Load registry from disk."""
        try:
            path = Path(self.registry_path)
            if path.exists():
                with open(path) as f:
                    data = json.load(f)
                    self.agents = data.get("agents", {})
        except Exception:
            self.agents = {}

    def _save(self) -> None:
        """Save registry to disk."""
        try:
            path = Path(self.registry_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, "w") as f:
                json.dump({"agents": self.agents}, f, indent=2)
        except Exception as e:
            raise Exception(f"Failed to save registry: {e}")

    def register(self, name: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Register a new agent."""
        if name in self.agents:
            raise Exception(f"Agent '{name}' already registered")
        record = {
            **config,
            "name": name,
            "registered_at": time.time(),
            "enabled": True,
            "last_seen": None,
        }
        self.agents[name] = record
        self._save()
        return record

    def unregister(self, name: str) -> bool:
        """Unregister an agent."""
        if name not in self.agents:
            return False
        del self.agents[name]
        self._save()
        return True

    def get(self, name: str) -> Optional[Dict[str, Any]]:
        """Get agent details."""
        return self.agents.get(name)

    def list_agents(self) -> List[Dict[str, Any]]:
        """List all registered agents."""
        return list(self.agents.values())

    def find_by_capability(self, capability: str) -> List[str]:
        """Find agents that support a capability."""
        return [
            name for name, agent in self.agents.items()
            if capability in agent.get("capabilities", [])
        ]

    def update_status(self, name: str, status: str) -> None:
        """Update agent status."""
        if name in self.agents:
            self.agents[name]["last_seen"] = time.time()
            self.agents[name]["status"] = status
            self._save()
