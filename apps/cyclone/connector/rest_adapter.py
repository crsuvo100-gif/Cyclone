"""REST API Agent Adapter."""

import aiohttp
import asyncio
from typing import Any, Dict, Optional
from .interface import AgentAdapter


class RESTAgentAdapter(AgentAdapter):
    """REST API agent adapter."""

    def __init__(self, name: str, config: Dict[str, Any]):
        super().__init__(name, config)
        self.base_url = config.get("url", "")
        self.api_key = config.get("api_key", "")
        self.session: Optional[aiohttp.ClientSession] = None
        self.async_session = None

    async def connect(self) -> bool:
        """Establish REST connection."""
        try:
            self.session = aiohttp.ClientSession()
            # Test connection
            async with self.session.get(f"{self.base_url}/health", timeout=aiohttp.ClientTimeout(total=5)) as r:
                if r.status == 200:
                    self.health_status = "healthy"
                    self.last_check = time.time()
                    return True
        except Exception as e:
            self.health_status = "unhealthy"
            self.last_check = time.time()
            raise AgentConnectionError(f"REST connection failed: {e}")
        return False

    async def disconnect(self) -> bool:
        """Disconnect REST session."""
        if self.session:
            await self.session.close()
            self.session = None
        return True

    async def health_check(self) -> bool:
        """Check REST health."""
        try:
            if not self.session:
                self.session = aiohttp.ClientSession()
            async with self.session.get(f"{self.base_url}/health", timeout=aiohttp.ClientTimeout(total=5)) as r:
                self.health_status = "healthy" if r.status == 200 else "unhealthy"
                self.last_check = time.time()
                return self.health_status == "healthy"
        except Exception as e:
            self.health_status = "unhealthy"
            self.last_check = time.time()
            raise AgentHealthError(f"Health check failed: {e}")

    async def send_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Send REST message."""
        if not self.session:
            self.session = aiohttp.ClientSession()
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        async with self.session.post(
            f"{self.base_url}/messages",
            json=message,
            headers=headers,
            timeout=aiohttp.ClientTimeout(total=30),
        ) as r:
            return await r.json()

    async def receive_message(self) -> Optional[Dict[str, Any]]:
        """Receive REST message."""
        # REST is request/response, so return None for receive
        return None

    async def ping(self) -> bool:
        """Ping REST agent."""
        try:
            if not self.session:
                self.session = aiohttp.ClientSession()
            async with self.session.get(f"{self.base_url}/ping", timeout=aiohttp.ClientTimeout(total=5)) as r:
                return r.status == 200
        except Exception:
            return False
