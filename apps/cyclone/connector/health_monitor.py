"""Agent Health Monitor - Connection Monitoring."""

import asyncio
import time
from typing import Any, Dict, List


class HealthMonitor:
    """Monitors agent health and connection status."""

    def __init__(self, interval: float = 30.0):
        self.interval = interval
        self.monitors: Dict[str, Dict[str, Any]] = {}
        self._running = False
        self._task: asyncio.Task = None

    def start(self) -> None:
        """Start health monitoring."""
        if self._running:
            return
        self._running = True
        self._task = asyncio.create_task(self._monitor_loop())

    async def _monitor_loop(self) -> None:
        """Main monitoring loop."""
        while self._running:
            await self.check_all()
            await asyncio.sleep(self.interval)

    async def check_all(self) -> Dict[str, Any]:
        """Check health of all agents."""
        results = {}
        for name in self.monitors:
            try:
                healthy = await self._check_agent(name)
                results[name] = {"healthy": healthy, "last_check": time.time()}
            except Exception as e:
                results[name] = {"healthy": False, "error": str(e)}
        return results

    async def _check_agent(self, name: str) -> bool:
        """Check single agent health."""
        # Implementation depends on adapter
        return True

    def add_monitor(self, name: str, monitor: object) -> None:
        """Add a health monitor for an agent."""
        self.monitors[name] = {"monitor": monitor, "last_status": "unknown"}

    def stop(self) -> None:
        """Stop health monitoring."""
        self._running = False
        if self._task:
            self._task.cancel()
