"""IPC Agent Adapter."""

import asyncio
import json
from typing import Any, Dict, Optional
from .interface import AgentAdapter


class IPCAgentAdapter(AgentAdapter):
    """IPC agent adapter (local process communication)."""

    def __init__(self, name: str, config: Dict[str, Any]):
        super().__init__(name, config)
        self.command = config.get("command", "")
        self.args = config.get("args", [])
        self.process: Optional[asyncio.subprocess.Process] = None

    async def connect(self) -> bool:
        """Establish IPC connection."""
        try:
            self.process = await asyncio.subprocess.create_subprocess_exec(
                self.command, *self.args,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            self.health_status = "connected"
            self.last_check = time.time()
            return True
        except Exception as e:
            self.health_status = "error"
            self.last_check = time.time()
            raise AgentConnectionError(f"IPC connection failed: {e}")

    async def disconnect(self) -> bool:
        """Disconnect IPC."""
        if self.process:
            self.process.terminate()
            try:
                await self.process.wait(timeout=5)
            except asyncio.TimeoutError:
                self.process.kill()
            self.process = None
        return True

    async def health_check(self) -> bool:
        """Check IPC health."""
        try:
            if not self.process:
                self.connect()
            self.health_status = "healthy"
            self.last_check = time.time()
            return True
        except Exception as e:
            self.health_status = "unhealthy"
            self.last_check = time.time()
            raise AgentHealthError(f"Health check failed: {e}")

    async def send_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Send IPC message."""
        if not self.process:
            self.connect()
        self.process.stdin.write(json.dumps(message).encode() + b"\n")
        await self.process.stdin.drain()
        return {"status": "sent"}

    async def receive_message(self) -> Optional[Dict[str, Any]]:
        """Receive IPC message."""
        if not self.process:
            return None
        line = await self.process.stdout.readline()
        if line:
            return json.loads(line.decode())
        return None

    async def ping(self) -> bool:
        """Ping IPC agent."""
        try:
            if not self.process:
                self.connect()
            self.process.stdin.write(json.dumps({"type": "ping"}).encode() + b"\n")
            await self.process.stdin.drain()
            return True
        except Exception:
            return False
