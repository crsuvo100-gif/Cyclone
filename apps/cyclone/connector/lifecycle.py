"""Agent Lifecycle Management."""

import time
from typing import Any, Dict


class AgentLifecycle:
    """Manages agent lifecycle (create, start, stop, delete)."""

    def __init__(self):
        self.agents: Dict[str, Dict[str, Any]] = {}

    def create(self, name: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new agent."""
        self.agents[name] = {
            **config,
            "name": name,
            "created_at": time.time(),
            "status": "created",
        }
        return self.agents[name]

    def start(self, name: str) -> Dict[str, Any]:
        """Start an agent."""
        if name not in self.agents:
            raise Exception(f"Agent '{name}' not found")
        self.agents[name]["status"] = "running"
        self.agents[name]["started_at"] = time.time()
        return self.agents[name]

    def stop(self, name: str) -> Dict[str, Any]:
        """Stop an agent."""
        if name not in self.agents:
            raise Exception(f"Agent '{name}' not found")
        self.agents[name]["status"] = "stopped"
        self.agents[name]["stopped_at"] = time.time()
        return self.agents[name]

    def delete(self, name: str) -> bool:
        """Delete an agent."""
        if name not in self.agents:
            return False
        del self.agents[name]
        return True

    def get_status(self, name: str) -> Dict[str, Any]:
        """Get agent status."""
        return self.agents.get(name, {})
