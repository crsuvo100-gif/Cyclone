"""Universal Agent Connector Interface.

Defines the contract for connecting to external AI agents and HERMES.
Supports REST API, WebSocket, and local IPC adapters.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
import asyncio
import time


class AgentConnectionError(Exception):
    """Raised when an agent connection fails."""
    pass


class AgentNotRegisteredError(AgentConnectionError):
    pass


class AgentRegistrationError(AgentConnectionError):
    pass


class AgentCapabilityError(AgentConnectionError):
    pass


class AgentHealthError(AgentConnectionError):
    pass


class AgentAdapter(ABC):
    """Abstract base class for agent adapters."""

    def __init__(self, name: str, config: Dict[str, Any]):
        self.name = name
        self.config = config
        self.enabled = True
        self.health_status = "unknown"
        self.last_check = None

    @abstractmethod
    async def connect(self) -> bool:
        """Establish connection to the agent."""
        pass

    @abstractmethod
    async def disconnect(self) -> bool:
        """Disconnect from the agent."""
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """Check agent health status."""
        pass

    @abstractmethod
    async def send_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Send a message to the agent."""
        pass

    @abstractmethod
    async def receive_message(self) -> Optional[Dict[str, Any]]:
        """Receive a message from the agent."""
        pass

    @abstractmethod
    async def ping(self) -> bool:
        """Ping the agent to verify connectivity."""
        pass

    def get_status(self) -> Dict[str, Any]:
        """Get the adapter status."""
        return {
            "name": self.name,
            "enabled": self.enabled,
            "health": self.health_status,
            "last_check": self.last_check,
            "config": {k: v for k, v in self.config.items() if k != "api_key"},
        }


class UniversalAgentConnector:
    """Universal connector for managing multiple agent connections."""

    def __init__(self):
        self.adapters: Dict[str, AgentAdapter] = {}
        self.registry: Dict[str, Dict[str, Any]] = {}
        self.task_tracking: Dict[str, Dict[str, Any]] = {}
        self.audit_log: List[Dict[str, Any]] = []

    def register_agent(self, name: str, config: Dict[str, Any]) -> None:
        """Register a new agent."""
        if name in self.registry:
            raise AgentRegistrationError(f"Agent '{name}' already registered")
        self.registry[name] = {
            **config,
            "registered_at": time.time(),
            "enabled": True,
            "last_seen": None,
        }
        self.audit_log.append({
            "event": "agent_registered",
            "name": name,
            "config": config,
            "timestamp": time.time(),
        })

    def unregister_agent(self, name: str) -> bool:
        """Unregister an agent."""
        if name not in self.registry:
            raise AgentNotRegisteredError(f"Agent '{name}' not registered")
        del self.registry[name]
        if name in self.adapters:
            del self.adapters[name]
        return True

    def get_agent(self, name: str) -> Optional[Dict[str, Any]]:
        """Get agent details."""
        return self.registry.get(name)

    def list_agents(self) -> List[Dict[str, Any]]:
        """List all registered agents."""
        return list(self.registry.values())

    def get_adapter(self, name: str) -> Optional[AgentAdapter]:
        """Get agent adapter by name."""
        return self.adapters.get(name)

    async def connect_agent(self, name: str) -> bool:
        """Connect to an agent."""
        if name not in self.registry:
            raise AgentNotRegisteredError(f"Agent '{name}' not registered")
        adapter_class = self._get_adapter_class(self.registry[name].get("kind", "rest"))
        adapter = adapter_class(name, self.registry[name])
        self.adapters[name] = adapter
        connected = await adapter.connect()
        if connected:
            self.registry[name]["enabled"] = True
            self.registry[name]["last_seen"] = time.time()
        return connected

    async def disconnect_agent(self, name: str) -> bool:
        """Disconnect from an agent."""
        if name not in self.adapters:
            raise AgentNotRegisteredError(f"Agent '{name}' not connected")
        connected = await self.adapters[name].disconnect()
        if connected:
            self.registry[name]["enabled"] = False
            self.registry[name]["last_seen"] = time.time()
        return connected

    async def health_check_all(self) -> Dict[str, Any]:
        """Check health of all connected agents."""
        results = {}
        for name, adapter in self.adapters.items():
            try:
                healthy = await adapter.health_check()
                results[name] = {
                    "healthy": healthy,
                    "status": adapter.health_status,
                    "last_check": adapter.last_check,
                }
            except Exception as e:
                results[name] = {"healthy": False, "error": str(e)}
        return results

    async def delegate_task(self, agent_name: str, task: Dict[str, Any]) -> Dict[str, Any]:
        """Delegate a task to an agent."""
        if agent_name not in self.adapters:
            raise AgentNotRegisteredError(f"Agent '{agent_name}' not connected")
        task_id = f"task_{int(time.time() * 1000)}"
        self.task_tracking[task_id] = {
            "agent": agent_name,
            "task": task,
            "status": "pending",
            "created_at": time.time(),
            "result": None,
        }
        try:
            result = await self.adapters[agent_name].send_message({
                "type": "task",
                "task_id": task_id,
                "task": task,
            })
            self.task_tracking[task_id]["status"] = "completed"
            self.task_tracking[task_id]["result"] = result
            return {"ok": True, "task_id": task_id, "result": result}
        except Exception as e:
            self.task_tracking[task_id]["status"] = "failed"
            self.task_tracking[task_id]["result"] = {"error": str(e)}
            return {"ok": False, "task_id": task_id, "error": str(e)}

    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get task status."""
        return self.task_tracking.get(task_id)

    def list_tasks(self) -> List[Dict[str, Any]]:
        """List all tasks."""
        return list(self.task_tracking.values())

    def get_audit_log(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get audit log."""
        return self.audit_log[-limit:]

    def _get_adapter_class(self, kind: str):
        """Get adapter class by kind."""
        adapters = {
            "rest": RESTAgentAdapter,
            "websocket": WebSocketAgentAdapter,
            "ipc": IPCAgentAdapter,
        }
        return adapters.get(kind, RESTAgentAdapter)
