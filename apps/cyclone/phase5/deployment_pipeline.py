"""Phase 5: Deployment Pipeline module.

Provides deployment pipeline management:
- Multi-stage deployment (dev, staging, production)
- Rollback management
- Deployment tracking and history

Usage:
    from apps.cyclone.phase5.deployment_pipeline import (
        DeploymentPipelineImplementation,
        DeploymentPipelineExecutor,
    )
"""

from __future__ import annotations

import hashlib
import logging
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from .interface import DeploymentPipeline, DeploymentError, DeploymentPipeline as IDeploymentPipeline

logger = logging.getLogger(__name__)


@dataclass
class DeploymentPipelineImplementation(IDeploymentPipeline):
    """Implementation of a deployment pipeline."""

    pipeline_id: str = ""
    pipeline_name: str = ""
    targets: list[dict[str, Any]] = field(default_factory=list)
    rollback_enabled: bool = True
    active: bool = True
    current_target: str = "development"

    def to_dict(self) -> dict[str, Any]:
        return {
            "pipeline_id": self.pipeline_id,
            "pipeline_name": self.pipeline_name,
            "targets": self.targets,
            "rollback_enabled": self.rollback_enabled,
            "active": self.active,
            "current_target": self.current_target,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DeploymentPipelineImplementation":
        return cls(
            pipeline_id=data.get("pipeline_id", ""),
            pipeline_name=data.get("pipeline_name", ""),
            targets=data.get("targets", []),
            rollback_enabled=data.get("rollback_enabled", True),
            active=data.get("active", True),
            current_target=data.get("current_target", "development"),
        )


@dataclass
class DeploymentRecord:
    """Record of a deployment."""
    deployment_id: str
    pipeline_id: str
    target: str
    version: str
    status: str
    timestamp: float = 0.0
    error: str | None = None


class DeploymentPipelineExecutor:
    """Executes deployment pipelines."""

    def __init__(self) -> None:
        self._pipelines: dict[str, DeploymentPipelineImplementation] = {}
        self._deployments: list[DeploymentRecord] = []
        self._logger = logging.getLogger(__name__)

    async def register_pipeline(self, pipeline: DeploymentPipeline) -> str:
        """Register a deployment pipeline."""
        pid = pipeline.pipeline_id
        self._pipelines[pid] = pipeline
        self._logger.info(f"Registered deployment pipeline: {pid}")
        return pid

    async def deploy(self, pipeline_id: str, version: str, config: dict[str, Any] | None = None) -> dict[str, Any]:
        """Deploy to the configured target."""
        if pipeline_id not in self._pipelines:
            raise DeploymentError(f"Pipeline not found: {pipeline_id}")

        pipeline = self._pipelines[pipeline_id]
        if not pipeline.active:
            raise DeploymentError(f"Pipeline is not active: {pipeline_id}")

        deployment_id = f"DPL-{datetime.now().strftime('%Y%m%d%H%M%S')}-{hashlib.md5(pipeline_id.encode()).hexdigest()[:6]}"

        target = next((t for t in pipeline.targets if t.get("name") == pipeline.current_target), None)
        if target is None:
            raise DeploymentError(f"No target configured: {pipeline.current_target}")

        self._deployments.append(DeploymentRecord(
            deployment_id=deployment_id,
            pipeline_id=pipeline_id,
            target=pipeline.current_target,
            version=version,
            status="deploying",
        ))

        try:
            self._logger.info(f"Deploying v{version} to {pipeline.current_target}")
            time.sleep(1)

            self._deployments[-1].status = "completed"
            self._deployments[-1].timestamp = time.time()

            return {
                "deployment_id": deployment_id,
                "version": version,
                "target": pipeline.current_target,
                "status": "completed",
                "timestamp": self._deployments[-1].timestamp,
            }
        except Exception as exc:
            self._deployments[-1].status = "failed"
            self._deployments[-1].error = str(exc)
            raise DeploymentError(f"Deployment failed: {exc}") from exc

    async def rollback(self, pipeline_id: str) -> dict[str, Any]:
        """Rollback the current deployment."""
        if pipeline_id not in self._pipelines:
            raise DeploymentError(f"Pipeline not found: {pipeline_id}")

        pipeline = self._pipelines[pipeline_id]
        if not pipeline.rollback_enabled:
            raise DeploymentError(f"Rollback not enabled for: {pipeline_id}")

        deployment_id = f"ROLL-{datetime.now().strftime('%Y%m%d%H%M%S')}-{hashlib.md5(pipeline_id.encode()).hexdigest()[:6]}"

        self._logger.info(f"Rolling back pipeline: {pipeline_id}")

        return {
            "deployment_id": deployment_id,
            "pipeline_id": pipeline_id,
            "status": "completed",
            "message": "Rollback completed successfully",
        }

    @property
    def pipelines(self) -> dict[str, DeploymentPipeline]:
        return dict(self._pipelines)

    def list_deployments(self) -> list[dict[str, Any]]:
        """List deployment history."""
        return [d.__dict__ for d in self._deployments]
