"""Phase 5: CI/CD Integration Contracts.

Defines contracts for:
- Continuous integration and delivery
- Automated testing pipelines
- Production deployment workflows
- Quality gates and enforcement
- Release management

Usage:
    from apps.cyclone.phase5 import (
        CIWorkflow,
        DeploymentPipeline,
        QualityEngine,
    )
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class Phase5Error(Exception):
    """Base exception for Phase 5 errors."""


class CIError(Phase5Error):
    """Raised when CI operations fail."""


class DeploymentError(Phase5Error):
    """Raised when deployment operations fail."""


class QualityGateError(Phase5Error):
    """Raised when quality gates fail."""


class ReleaseError(Phase5Error):
    """Raised when release operations fail."""


class CIWorkflow(ABC):
    """Abstract CI workflow definition."""

    @property
    @abstractmethod
    def workflow_id(self) -> str:
        """Workflow identifier."""
        ...

    @property
    @abstractmethod
    def workflow_name(self) -> str:
        """Workflow name."""
        ...

    @property
    @abstractmethod
    def trigger(self) -> str:
        """Workflow trigger (push, pull_request, schedule)."""
        ...

    @property
    @abstractmethod
    def steps(self) -> list[dict[str, Any]]:
        """Workflow steps."""
        ...

    @abstractmethod
    def to_dict(self) -> dict[str, Any]:
        """Serialize to dict."""
        ...

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict[str, Any]) -> "CIWorkflow":
        """Deserialize from dict."""
        ...


class DeploymentPipeline(ABC):
    """Abstract deployment pipeline definition."""

    @property
    @abstractmethod
    def pipeline_id(self) -> str:
        """Pipeline identifier."""
        ...

    @property
    @abstractmethod
    def pipeline_name(self) -> str:
        """Pipeline name."""
        ...

    @property
    @abstractmethod
    def targets(self) -> list[dict[str, Any]]:
        """Deployment targets."""
        ...

    @property
    @abstractmethod
    def rollback_enabled(self) -> bool:
        """Whether rollback is enabled."""
        ...

    @abstractmethod
    def to_dict(self) -> dict[str, Any]:
        """Serialize to dict."""
        ...

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict[str, Any]) -> "DeploymentPipeline":
        """Deserialize from dict."""
        ...


class QualityEngine(ABC):
    """Abstract quality engine for CI gates."""

    @property
    @abstractmethod
    def engine_id(self) -> str:
        """Engine identifier."""
        ...

    @property
    @abstractmethod
    def engine_name(self) -> str:
        """Engine name."""
        ...

    @abstractmethod
    def evaluate(self, metrics: dict[str, Any]) -> dict[str, Any]:
        """Evaluate quality metrics."""
        ...

    @abstractmethod
    def register_metric(self, metric_name: str, threshold: float, unit: str) -> str:
        """Register a quality metric."""
        ...

    @property
    @abstractmethod
    def metrics(self) -> dict[str, Any]:
        """Get registered metrics."""
        ...


class ReleaseManager(ABC):
    """Abstract release manager."""

    @property
    @abstractmethod
    def manager_id(self) -> str:
        """Manager identifier."""
        ...

    @property
    @abstractmethod
    def manager_name(self) -> str:
        """Manager name."""
        ...

    @abstractmethod
    async def create_release(self, version: str, changes: list[str]) -> dict[str, Any]:
        """Create a new release."""
        ...

    @abstractmethod
    async def publish_release(self, release_id: str) -> dict[str, Any]:
        """Publish a release."""
        ...

    @abstractmethod
    async def list_releases(self) -> list[dict[str, Any]]:
        """List all releases."""
        ...

    @property
    @abstractmethod
    def current_release(self) -> dict[str, Any] | None:
        """Get the current release."""
        ...


class GitIntegration(ABC):
    """Abstract Git integration for version control."""

    @property
    @abstractmethod
    def git_id(self) -> str:
        """Git integration identifier."""
        ...

    @property
    @abstractmethod
    def git_url(self) -> str:
        """Git repository URL."""
        ...

    @abstractmethod
    def get_branch(self) -> str:
        """Get current branch."""
        ...

    @abstractmethod
    def get_commit(self) -> str:
        """Get latest commit hash."""
        ...

    @abstractmethod
    def create_tag(self, tag_name: str, message: str) -> dict[str, Any]:
        """Create a version tag."""
        ...

    @abstractmethod
    def push(self, branch: str) -> dict[str, Any]:
        """Push branch to remote."""
        ...

    @property
    @abstractmethod
    def branches(self) -> list[str]:
        """List all branches."""
        ...
