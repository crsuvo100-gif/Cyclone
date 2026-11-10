"""Task Delegation - Structured Task Delegation."""

import asyncio
import secrets
import time
from typing import Any, Dict, List, Optional


class TaskDelegation:
    """Manages structured task delegation to agents."""

    def __init__(self, registry: object):
        self.registry = registry
        self.tasks: Dict[str, Dict[str, Any]] = {}
        self.results: Dict[str, Dict[str, Any]] = {}

    def delegate(self, agent_name: str, task: Dict[str, Any]) -> str:
        """Delegate a task to an agent."""
        if agent_name not in self.registry.agents:
            raise Exception(f"Agent '{agent_name}' not registered")
        
        task_id = f"task_{int(time.time() * 1000)}_{secrets.token_hex(8)}"
        self.tasks[task_id] = {
            "agent": agent_name,
            "task": task,
            "status": "pending",
            "created_at": time.time(),
            "updated_at": None,
            "result": None,
        }
        return task_id

    async def delegate_async(self, agent_name: str, task: Dict[str, Any]) -> str:
        """Asynchronously delegate a task."""
        task_id = self.delegate(agent_name, task)
        await asyncio.sleep(0.1)
        return task_id

    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get task status."""
        return self.tasks.get(task_id)

    def list_tasks(self) -> List[Dict[str, Any]]:
        """List all tasks."""
        return list(self.tasks.values())

    def complete_task(self, task_id: str, result: Dict[str, Any]) -> bool:
        """Mark task as completed."""
        if task_id not in self.tasks:
            return False
        self.tasks[task_id]["status"] = "completed"
        self.tasks[task_id]["result"] = result
        self.tasks[task_id]["updated_at"] = time.time()
        self.results[task_id] = result
        return True

    def fail_task(self, task_id: str, error: str) -> bool:
        """Mark task as failed."""
        if task_id not in self.tasks:
            return False
        self.tasks[task_id]["status"] = "failed"
        self.tasks[task_id]["result"] = {"error": error}
        self.tasks[task_id]["updated_at"] = time.time()
        return True
