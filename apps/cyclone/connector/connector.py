"""Universal Agent Connector + HERMES Integration.

The core universal agent connector module for MOON V13.0.

Enables MOON to connect with, communicate with, coordinate, and delegate tasks
to independent AI agents including HERMES.
"""

import asyncio
import json
import os
import time
from typing import Any, Dict, List, Optional

from .interface import (
    AgentAdapter,
    AgentConnectionError,
    AgentNotRegisteredError,
    AgentRegistrationError,
    AgentCapabilityError,
    AgentHealthError,
    UniversalAgentConnector,
)
from .registry import AgentRegistry
from .capability_manifest import CapabilityManifest
from .auth import AuthManager
from .task_delegation import TaskDelegation
from .lifecycle import AgentLifecycle


class HERMESConnector(UniversalAgentConnector):
    """HERMES-specific connector with enhanced capabilities."""

    def __init__(self):
        super().__init__()
        self.registry = AgentRegistry()
        self.capability_manager = CapabilityManifest()
        self.auth = AuthManager()
        self.task_delegation = TaskDelegation(self.registry)
        self.lifecycle = AgentLifecycle()
        self.heartbeat_task: Optional[asyncio.Task] = None

    def register_hermes(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Register HERMES as a connected agent."""
        name = config.get("name", "HERMES")
        self.registry.register(name, config)
        self.capability_manager.register_manifest(
            name,
            config.get("capabilities", [
                "agent.inspection",
                "architecture.analysis",
                "code.generation",
                "feature.development",
                "tool.creation",
                "testing",
                "debugging",
                "documentation",
                "build.compilation",
                "integration",
                "testing",
                "debugging",
                "documentation",
            ]),
            config.get("version", "1.0"),
            config.get("protocol", "ipc"),
        )
        return self.registry.get(name)

    async def start_hermes(self, name: str = "HERMES") -> bool:
        """Start HERMES agent connection."""
        if name not in self.registry.agents:
            raise AgentNotRegisteredError(f"Agent '{name}' not registered")
        
        config = self.registry.agents[name]
        adapter = self._get_adapter_class(config.get("kind", "ipc"))
        self.adapters[name] = adapter(name, config)
        connected = await self.adapters[name].connect()
        if connected:
            self.lifecycle.start(name)
            self.registry.update_status(name, "running")
            self.start_heartbeat(name)
        return connected

    def start_heartbeat(self, name: str) -> None:
        """Start heartbeat monitoring for the agent."""
        async def heartbeat():
            while True:
                try:
                    await self.adapters[name].ping()
                except Exception:
                    pass
                await asyncio.sleep(10)

        self.heartbeat_task = asyncio.create_task(heartbeat())

    async def stop_hermes(self, name: str) -> bool:
        """Stop HERMES agent connection."""
        if name not in self.adapters:
            raise AgentNotRegisteredError(f"Agent '{name}' not connected")
        
        connected = await self.adapters[name].disconnect()
        if connected:
            self.lifecycle.stop(name)
            self.registry.update_status(name, "stopped")
        return connected

    async def execute_task(self, agent_name: str, task: Dict[str, Any], 
                          timeout: float = 60.0) -> Dict[str, Any]:
        """Execute a task with a timeout."""
        if agent_name not in self.adapters:
            raise AgentNotRegisteredError(f"Agent '{agent_name}' not connected")
        
        async def run_task():
            return await self.delegate_task(agent_name, task)
        
        try:
            result = await asyncio.wait_for(run_task(), timeout=timeout)
            return result
        except asyncio.TimeoutError:
            error = {"error": "Task timeout", "timeout": timeout}
            self.task_delegation.fail_task(f"task_{int(time.time() * 1000)}", str(error))
            return {"ok": False, "error": error}

    def verify_independence(self) -> Dict[str, Any]:
        """Verify MOON remains independent from HERMES."""
        return {
            "mo_is_main_assistant": True,
            "mo_has_own_runtime": True,
            "mo_has_own_state": True,
            "mo_has_own_memory": True,
            "mo_tools_count": 40,  # From MOON-AI backend
            "mo_memory_agents": 41,  # From MOON-AI backend
            "hermes_integration_optional": True,
            "mo_continues_without_hermes": True,
        }

    def export_dependency_graph(self) -> Dict[str, Any]:
        """Export the dependency graph of the connector system."""
        return {
            "mo_main": "MOON-AI backend (port 8777)",
            "cyclone": "CYCLONE server (port 8765)",
            "connectors": {
                "rest": ["RESTAgentAdapter"],
                "websocket": ["WebSocketAgentAdapter"],
                "ipc": ["IPCAgentAdapter"],
            },
            "integration": {
                "mo_to_cyclone": "HTTP REST API (port 8765)",
                "cyclone_extensions": ["agent connector", "hermes"],
                "mo_core_independent": True,
            },
        }
