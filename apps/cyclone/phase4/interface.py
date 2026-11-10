"""Phase 4: Testing + Build + Integration contracts.

Defines contracts for:
- Test execution (unit, integration, end-to-end)
- CI/CD pipeline steps
- Build and compilation
- Deployment workflows
- Release management

Usage:
    from apps.cyclone.phase4 import (
        TestExecutor,
        PipelineExecutor,
        BuildManager,
        DeploymentManager,
    )
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class Phase4Error(Exception):
    """Base exception for Phase 4 errors."""


class TestError(Phase4Error):
    """Raised when test execution fails."""


class BuildError(Phase4Error):
    """Raised when build fails."""


class DeploymentError(Phase4Error):
    """Raised when deployment fails."""


class PipelineError(Phase4Error):
    """Raised when a pipeline step fails."""


class ReleaseError(Phase4Error):
    """Raised when a release operation fails."""


class TestCase(ABC):
    """Abstract test case definition."""

    @property
    @abstractmethod
    def test_id(self) -> str:
        """Unique test case identifier."""
        ...

    @property
    @abstractmethod
    def test_name(self) -> str:
        """Test case name."""
        ...

    @property
    @abstractmethod
    def description(self) -> str:
        """Test description."""
        ...

    @property
    @abstractmethod
    def category(self) -> str:
        """Test category (unit, integration, e2e)."""
        ...

    @property
    @abstractmethod
    def priority(self) -> int:
        """Test priority (1 = highest)."""
        ...

    @property
    @abstractmethod
    def timeout(self) -> float:
        """Test timeout in seconds."""
        ...

    @abstractmethod
    def to_dict(self) -> dict[str, Any]:
        """Serialize to dict."""
        ...

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict[str, Any]) -> "TestCase":
        """Deserialize from dict."""
        ...


class TestSuite(ABC):
    """Abstract test suite definition."""

    @property
    @abstractmethod
    def suite_id(self) -> str:
        """Suite identifier."""
        ...

    @property
    @abstractmethod
    def suite_name(self) -> str:
        """Suite name."""
        ...

    @property
    @abstractmethod
    def tests(self) -> list[TestCase]:
        """Test cases in the suite."""
        ...

    @property
    @abstractmethod
    def description(self) -> str:
        """Suite description."""
        ...

    @abstractmethod
    def to_dict(self) -> dict[str, Any]:
        """Serialize to dict."""
        ...

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict[str, Any]) -> "TestSuite":
        """Deserialize from dict."""
        ...


class TestResult(ABC):
    """Abstract test result."""

    @property
    @abstractmethod
    def test_id(self) -> str:
        """Test case ID."""
        ...

    @property
    @abstractmethod
    def status(self) -> str:
        """Test status (passed, failed, skipped)."""
        ...

    @property
    @abstractmethod
    def duration(self) -> float:
        """Test duration in seconds."""
        ...

    @property
    @abstractmethod
    def output(self) -> str:
        """Test output."""
        ...

    @property
    @abstractmethod
    def error(self) -> str | None:
        """Error message if failed."""
        ...

    @abstractmethod
    def to_dict(self) -> dict[str, Any]:
        """Serialize to dict."""
        ...


class BuildArtifact(ABC):
    """Abstract build artifact."""

    @property
    @abstractmethod
    def artifact_id(self) -> str:
        """Artifact identifier."""
        ...

    @property
    @abstractmethod
    def artifact_type(self) -> str:
        """Artifact type."""
        ...

    @property
    @abstractmethod
    def target(self) -> str:
        """Build target."""
        ...

    @property
    @abstractmethod
    def path(self) -> str | None:
        """Path to artifact."""
        ...

    @property
    @abstractmethod
    def size(self) -> int:
        """Artifact size in bytes."""
        ...

    @abstractmethod
    def to_dict(self) -> dict[str, Any]:
        """Serialize to dict."""
        ...


class DeploymentTarget(ABC):
    """Abstract deployment target."""

    @property
    @abstractmethod
    def target_id(self) -> str:
        """Deployment target ID."""
        ...

    @property
    @abstractmethod
    def target_name(self) -> str:
        """Deployment target name."""
        ...

    @property
    @abstractmethod
    def environment(self) -> str:
        """Deployment environment (dev, staging, prod)."""
        ...

    @property
    @abstractmethod
    def credentials(self) -> dict[str, Any] | None:
        """Deployment credentials."""
        ...

    @abstractmethod
    def to_dict(self) -> dict[str, Any]:
        """Serialize to dict."""
        ...


class Release(ABC):
    """Abstract release definition."""

    @property
    @abstractmethod
    def release_id(self) -> str:
        """Release identifier."""
        ...

    @property
    @abstractmethod
    def version(self) -> str:
        """Release version."""
        ...

    @property
    @abstractmethod
    def artifacts(self) -> list[BuildArtifact]:
        """Build artifacts."""
        ...

    @property
    @abstractmethod
    def changes(self) -> list[str]:
        """List of changes in this release."""
        ...

    @property
    @abstractmethod
    def status(self) -> str:
        """Release status (draft, pending, released, failed)."""
        ...

    @abstractmethod
    def to_dict(self) -> dict[str, Any]:
        """Serialize to dict."""
        ...


class TestExecutor(ABC):
    """Abstract test executor."""

    @abstractmethod
    async def run_tests(self, suites: list[TestSuite]) -> list[TestResult]:
        """Run a suite of tests."""
        ...

    @abstractmethod
    async def run_single_test(self, test: TestCase) -> TestResult:
        """Run a single test case."""
        ...

    @abstractmethod
    async def get_test_results(self, test_id: str) -> TestResult | None:
        """Get test results by ID."""
        ...

    @property
    @abstractmethod
    def results(self) -> list[TestResult]:
        """Get all test results."""
        ...


class PipelineExecutor(ABC):
    """Abstract pipeline executor."""

    @abstractmethod
    async def execute_pipeline(self, pipeline_name: str, variables: dict[str, Any]) -> dict[str, Any]:
        """Execute a named pipeline."""
        ...

    @abstractmethod
    async def add_step(self, step: dict[str, Any]) -> str:
        """Add a step to a pipeline."""
        ...

    @abstractmethod
    async def remove_step(self, step_id: str) -> bool:
        """Remove a pipeline step."""
        ...

    @property
    @abstractmethod
    def pipelines(self) -> dict[str, list[dict[str, Any]]]:
        """Get all pipeline definitions."""
        ...


class BuildManager(ABC):
    """Abstract build manager."""

    @abstractmethod
    async def build(self, target: str, config: dict[str, Any]) -> BuildArtifact:
        """Build a target."""
        ...

    @abstractmethod
    async def clean(self, target: str) -> bool:
        """Clean build artifacts."""
        ...

    @abstractmethod
    async def list_artifacts(self) -> list[BuildArtifact]:
        """List all build artifacts."""
        ...

    @property
    @abstractmethod
    def build_cache(self) -> dict[str, Any]:
        """Get build cache state."""
        ...


class DeploymentManager(ABC):
    """Abstract deployment manager."""

    @abstractmethod
    async def deploy(self, target: DeploymentTarget, artifact: BuildArtifact, config: dict[str, Any]) -> dict[str, Any]:
        """Deploy to a target."""
        ...

    @abstractmethod
    async def rollback(self, target: DeploymentTarget) -> dict[str, Any]:
        """Rollback a deployment."""
        ...

    @abstractmethod
    async def list_deployments(self) -> list[dict[str, Any]]:
        """List deployment history."""
        ...

    @property
    @abstractmethod
    def active_deployments(self) -> list[DeploymentTarget]:
        """Get active deployments."""
        ...


class ReleaseManager(ABC):
    """Abstract release manager."""

    @abstractmethod
    async def create_release(self, version: str, changes: list[str]) -> Release:
        """Create a new release."""
        ...

    @abstractmethod
    async def publish_release(self, release: Release) -> dict[str, Any]:
        """Publish a release."""
        ...

    @abstractmethod
    async def list_releases(self) -> list[Release]:
        """List releases."""
        ...

    @property
    @abstractmethod
    def current_version(self) -> str:
        """Get current version."""
        ...


class QualityGate(ABC):
    """Abstract quality gate."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Quality gate name."""
        ...

    @property
    @abstractmethod
    def threshold(self) -> float:
        """Quality gate threshold."""
        ...

    @abstractmethod
    def evaluate(self, metrics: dict[str, Any]) -> bool:
        """Evaluate quality gate."""
        ...

    @property
    @abstractmethod
    def threshold_units(self) -> str:
        """Threshold units."""
        ...
