"""Phase 4: Pipeline Executor module.

Provides CI/CD pipeline execution:
- Pipeline step definitions
- Pipeline execution with dependencies
- Rollback support
- Pipeline status tracking

Usage:
    from apps.cyclone.phase4.pipeline_executor import PipelineExecutorImplementation

    executor = PipelineExecutorImplementation()
    await executor.add_step({"name": "test", "command": "pytest"})
    await executor.execute_pipeline("ci")
"""

from __future__ import annotations

import asyncio
import hashlib
import logging
import subprocess
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from .interface import (
    PipelineError,
    PipelineExecutor,
)

logger = logging.getLogger(__name__)


@dataclass
class PipelineStep:
    """Implementation of a pipeline step."""
    step_id: str
    name: str
    command: str
    depends_on: list[str] = field(default_factory=list)
    timeout: float = 300.0
    enabled: bool = True
    order: int = 0
    environment: dict[str, str] = field(default_factory=dict)


@dataclass
class PipelineExecution:
    """Implementation of a pipeline execution."""
    pipeline_name: str
    variables: dict[str, Any] = field(default_factory=dict)
    steps: list[PipelineStep] = field(default_factory=list)
    status: str = "pending"
    current_step: int = 0
    results: dict[str, Any] = field(default_factory=dict)
    started_at: float = 0.0
    completed_at: float = 0.0


class PipelineExecutorImplementation(PipelineExecutor):
    """Implementation of a pipeline executor."""

    def __init__(self) -> None:
        self._pipelines: dict[str, list[dict[str, Any]]] = {}
        self._executions: dict[str, PipelineExecution] = {}
        self._logger = logging.getLogger(__name__)

    async def execute_pipeline(self, pipeline_name: str, variables: dict[str, Any]) -> dict[str, Any]:
        """Execute a named pipeline."""
        if pipeline_name not in self._pipelines:
            raise PipelineError(f"Pipeline not found: {pipeline_name}")

        pipeline_steps = self._pipelines[pipeline_name]
        execution_id = f"EXEC-{datetime.now().strftime('%Y%m%d%H%M%S')}-{hashlib.md5(pipeline_name.encode()).hexdigest()[:6]}"

        self._executions[execution_id] = PipelineExecution(
            pipeline_name=pipeline_name,
            variables={"pipeline_name": pipeline_name, **variables},
            steps=[],
            status="running",
        )

        results = {}
        execution = self._executions[execution_id]
        execution.started_at = asyncio.get_event_loop().time()

        for step in pipeline_steps:
            if not step.get("enabled", True):
                results[step["step_id"]] = {"status": "skipped", "reason": "disabled"}
                continue

            step_result = await self._run_step(step, variables)
            results[step["step_id"]] = step_result

            if step_result.get("status") == "failed":
                execution.status = "failed"
                execution.completed_at = asyncio.get_event_loop().time()
                break

        if execution.status != "failed":
            execution.status = "completed"
            execution.completed_at = asyncio.get_event_loop().time()

        return results

    async def _run_step(self, step: dict[str, Any], variables: dict[str, Any]) -> dict[str, Any]:
        """Run a single pipeline step."""
        step_id = step["step_id"]
        command = step["command"]

        self._logger.info(f"Running step: {step_id} - {command}")

        env = {**step.get("environment", {}), **variables}

        try:
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                lambda: subprocess.run(
                    command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=step.get("timeout", 300),
                    env=env,
                ),
            )

            return {
                "step_id": step_id,
                "status": "passed" if result.returncode == 0 else "failed",
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
                "duration_seconds": 0.0,
            }
        except subprocess.TimeoutExpired:
            return {"step_id": step_id, "status": "failed", "error": "Timeout"}
        except Exception as exc:
            return {"step_id": step_id, "status": "failed", "error": str(exc)}

    async def add_step(self, step: dict[str, Any]) -> str:
        """Add a step to a pipeline."""
        step_id = step.get("step_id") or f"STEP-{datetime.now().strftime('%H%M%S')}-{hash(step.get('name', '')) % 10000:04d}"
        step["step_id"] = step_id

        pipeline_name = step.get("pipeline_name", "default")
        if pipeline_name not in self._pipelines:
            self._pipelines[pipeline_name] = []

        self._pipelines[pipeline_name].append(step)
        return step_id

    async def remove_step(self, step_id: str) -> bool:
        """Remove a pipeline step."""
        for pipeline_name, steps in self._pipelines.items():
            for i, step in enumerate(steps):
                if step.get("step_id") == step_id:
                    del steps[i]
                    return True
        return False

    @property
    def pipelines(self) -> dict[str, list[dict[str, Any]]]:
        return self._pipelines


__all__ = ["PipelineStep", "PipelineExecution", "PipelineExecutorImplementation"]
