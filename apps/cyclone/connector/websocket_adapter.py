"""WebSocket Agent Adapter."""

import aiohttp
import asyncio
import json
from typing import Any, Dict, Optional
from .interface import AgentAdapter


class WebSocketAgentAdapter(AgentAdapter):
    """WebSocket agent adapter."""

    def __init__(self, name: str, config: Dict[str, Any]):
        super().__init__(name, config)
        self.base_url = config.get("url", "")
        self.api_key = config.get("api_key", "")
        self.session: Optional[aiohttp.ClientSession] = None
        self.ws: Optional[aiohttp.ClientWebSocketResponse] = None

    async def connect(self) -> bool:
        """Establish WebSocket connection."""
        try:
            self.session = aiohttp.ClientSession()
            self.ws = await self.session.ws_connect(
                self.base_url,
                headers={"Authorization": f"Bearer {self.api_key}"} if self.api_key else None,
                timeout=aiohttp.ClientTimeout(total=10),
            )
            self.health_status = "connected"
            self.last_check = time.time()
            return True
        except Exception as e:
            self.health_status = "error"
            self.last_check = time.time()
            raise AgentConnectionError(f"WebSocket connection failed: {e}")

    async def disconnect(self) -> bool:
        """Disconnect WebSocket."""
        if self.ws:
            await self.ws.close()
            self.ws = None
        if self.session:
            await self.session.close()
            self.session = None
        return True

    async def health_check(self) -> bool:
        """Check WebSocket health."""
        try:
            if not self.ws:
                self.ws = await self.session.ws_connect(
                    self.base_url,
                    headers={"Authorization": f"Bearer {self.api_key}"} if self.api_key else None,
                )
            self.health_status = "healthy"
            self.last_check = time.time()
            return True
        except Exception as e:
            self.health_status = "unhealthy"
            self.last_check = time.time()
            raise AgentHealthError(f"Health check failed: {e}")

    async def send_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Send WebSocket message."""
        if not self.ws:
            self.connect()
        self.ws.send_json(message)
        return {"status": "sent"}

    async def receive_message(self) -> Optional[Dict[str, Any]]:
        """Receive WebSocket message."""
        if not self.ws:
            return None
        msg = await self.ws.receive()
        if msg.type == aiohttp.WSMsgType.TEXT:
            return json.loads(msg.data)
        elif msg.type == aiohttp.WSMsgType.ERROR:
            return None
        return None

    async def ping(self) -> bool:
        """Ping WebSocket agent."""
        try:
            if not self.ws:
                self.connect()
            self.ws.send_json({"type": "ping"})
            return True
        except Exception:
            return False
