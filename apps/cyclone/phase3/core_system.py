"""Phase 3: Core System Management module.

Manages the lifecycle of the core MOON-AI system:
- Initialization with configuration
- Start/stop operations
- Health checks
- System registration and management

Usage:
    from apps.cyclone.phase3.core_system import CoreSystemManagerImplementation

    manager = CoreSystemManagerImplementation()
    system = await manager.create_system("MOON-AI", {"port": 8777})
    await system.start()
"""

from __future__ import annotations

import logging
import subprocess
import sys
import time
from typing import Any

from .interface import (
    CoreSystem,
    CoreSystemManager,
    CoreSystemError,
    CoreSystemInitializationError,
    CoreSystemOperationError,
)

logger = logging.getLogger(__name__)


class CoreSystemImplementation(CoreSystem):
    """Implementation of a core system."""

    def __init__(self, name: str, config: dict[str, Any]) -> None:
        self.name = name
        self.config = config
        self._running = False
        self._process: subprocess.Popen | None = None
        self._pid = 0
        self._startup_time = 0.0

    @property
    def version(self) -> str:
        return self.config.get("version", "1.0.0")

    @property
    def status(self) -> str:
        return "running" if self._running else "stopped"

    async def initialize(self, config: dict[str, Any]) -> dict[str, Any]:
        """Initialize the core system."""
        merged_config = {**self.config, **config}
        self.config = merged_config

        logger.info(f"Initializing core system: {self.name}")
        return {
            "status": "initialized",
            "name": self.name,
            "config": merged_config,
            "timestamp": time.time(),
        }

    async def start(self) -> dict[str, Any]:
        """Start the core system."""
        if self._running:
            raise CoreSystemOperationError("Core system is already running")

        try:
            logger.info(f"Starting core system: {self.name}")

            # In a real implementation, start the actual server process
            # For now, simulate startup
            await self._simulate_startup()
            self._running = True
            self._pid = 12345  # simulated PID
            self._startup_time = time.time()

            return {
                "status": "started",
                "name": self.name,
                "pid": self._pid,
                "timestamp": time.time(),
            }
        except Exception as exc:
            raise CoreSystemOperationError(f"Failed to start core system: {exc}") from exc

    async def stop(self) -> dict[str, Any]:
        """Stop the core system."""
        if not self._running:
            raise CoreSystemOperationError("Core system is not running")

        try:
            logger.info(f"Stopping core system: {self.name}")

            # In a real implementation, terminate the process
            await self._simulate_shutdown()
            self._running = False
            self._pid = 0

            return {
                "status": "stopped",
                "name": self.name,
                "timestamp": time.time(),
            }
        except Exception as exc:
            raise CoreSystemOperationError(f"Failed to stop core system: {exc}") from exc

    async def health_check(self) -> dict[str, Any]:
        """Perform a health check."""
        if not self._running:
            return {
                "status": "unhealthy",
                "name": self.name,
                "error": "System is not running",
            }

        return {
            "status": "healthy",
            "name": self.name,
            "version": self.version,
            "uptime_seconds": time.time() - self._startup_time,
        }

    async def _simulate_startup(self, timeout: float = 2.0) -> None:
        """Simulate system startup."""
        await asyncio.sleep(0.5)

    async def _simulate_shutdown(self, timeout: float = 1.0) -> None:
        """Simulate system shutdown."""
        await asyncio.sleep(0.2)


class CoreSystemManagerImplementation(CoreSystemManager):
    """Implementation of a core system manager."""

    def __init__(self) -> None:
        self._systems: dict[str, CoreSystem] = {}

    async def create_system(self, name: str, config: dict[str, Any]) -> CoreSystem:
        """Create a core system instance."""
        system = CoreSystemImplementation(name, config)
        return system

    async def register_system(self, system: CoreSystem) -> str:
        """Register a system."""
        system_id = system.name
        self._systems[system_id] = system
        logger.info(f"Core system registered: {system_id}")
        return system_id

    async def unregister_system(self, system_id: str) -> bool:
        """Unregister a system."""
        if system_id in self._systems:
            del self._systems[system_id]
            logger.info(f"Core system unregistered: {system_id}")
            return True
        return False

    async def get_system(self, system_id: str) -> CoreSystem | None:
        """Get a system by ID."""
        return self._systems.get(system_id)

    async def list_systems(self) -> list[CoreSystem]:
        """List all registered systems."""
        return list(self._systems.values())


async def initialize_core(config: dict[str, Any] | None = None) -> CoreSystem:
    """Initialize the core system."""
    manager = CoreSystemManagerImplementation()
    system = await manager.create_system("MOON-AI", {
        "version": "13.0",
        "port": 8777,
    })
    await manager.register_system(system)
    return system


__all__ = [
    "CoreSystemImplementation",
    "CoreSystemManagerImplementation",
    "initialize_core",
]
