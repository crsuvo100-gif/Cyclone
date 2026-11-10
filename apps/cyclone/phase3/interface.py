"""Phase 3: Feature Development + Documentation + Core System interface.

Defines contracts for:
- Feature development workflow with implementation plans
- Documentation generation (API docs, README, CHANGELOG, guides)
- Core system lifecycle management
- Task tracking for feature development
- Version management and changelog generation
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class Phase3Error(Exception):
    """Base exception for Phase 3 errors."""


class FeatureDefinitionError(Phase3Error):
    """Raised when feature definition is invalid."""


class PlanExecutionError(Phase3Error):
    """Raised when implementation plan execution fails."""


class DocumentationError(Phase3Error):
    """Raised when documentation generation fails."""


class VersionError(Phase3Error):
    """Raised when version handling fails."""


class CoreSystemError(Phase3Error):
    """Raised when core system operations fail."""


class TaskDefinition(ABC):
    """Abstract task definition for feature development."""

    @property
    @abstractmethod
    def task_id(self) -> str:
        """Unique task identifier."""
        ...

    @property
    @abstractmethod
    def title(self) -> str:
        """Task title."""
        ...

    @property
    @abstractmethod
    def description(self) -> str:
        """Task description."""
        ...

    @property
    @abstractmethod
    def priority(self) -> int:
        """Task priority (1 = highest)."""
        ...

    @property
    @abstractmethod
    def status(self) -> str:
        """Task status."""
        ...

    @abstractmethod
    def to_dict(self) -> dict[str, Any]:
        """Serialize to dict."""
        ...

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict[str, Any]) -> "TaskDefinition":
        """Deserialize from dict."""
        ...


class FeatureDefinition(ABC):
    """Abstract feature definition for structured feature development."""

    @property
    @abstractmethod
    def feature_id(self) -> str:
        """Unique feature identifier."""
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        """Feature name."""
        ...

    @property
    @abstractmethod
    def description(self) -> str:
        """Feature description."""
        ...

    @property
    @abstractmethod
    def acceptance_criteria(self) -> list[str]:
        """List of acceptance criteria."""
        ...

    @property
    @abstractmethod
    def complexity(self) -> str:
        """Feature complexity: low, medium, high."""
        ...

    @property
    @abstractmethod
    def priority(self) -> int:
        """Priority (1 = highest)."""
        ...

    @abstractmethod
    def to_dict(self) -> dict[str, Any]:
        """Serialize to dict."""
        ...

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict[str, Any]) -> "FeatureDefinition":
        """Deserialize from dict."""
        ...


class ImplementationPlan(ABC):
    """Abstract implementation plan for a feature."""

    @property
    @abstractmethod
    def plan_id(self) -> str:
        """Plan identifier."""
        ...

    @property
    @abstractmethod
    def feature_id(self) -> str:
        """Associated feature ID."""
        ...

    @property
    @abstractmethod
    def steps(self) -> list[dict[str, Any]]:
        """Ordered list of implementation steps."""
        ...

    @property
    @abstractmethod
    def dependencies(self) -> list[str]:
        """List of feature IDs this depends on."""
        ...

    @property
    @abstractmethod
    def estimated_hours(self) -> float:
        """Estimated implementation hours."""
        ...

    @abstractmethod
    def to_dict(self) -> dict[str, Any]:
        """Serialize to dict."""
        ...

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict[str, Any]) -> "ImplementationPlan":
        """Deserialize from dict."""
        ...


class DocumentationGenerator(ABC):
    """Abstract documentation generator base."""

    @abstractmethod
    async def generate_api_docs(self, features: list[FeatureDefinition]) -> str:
        """Generate API documentation for features."""
        ...

    @abstractmethod
    async def generate_readme(self, project_info: dict[str, Any]) -> str:
        """Generate README.md."""
        ...

    @abstractmethod
    async def generate_changelog(self, releases: list[dict[str, Any]]) -> str:
        """Generate CHANGELOG.md."""
        ...

    @abstractmethod
    async def generate_guidelines(self, project_name: str) -> str:
        """Generate CONTRIBUTING.md guidelines."""
        ...

    @abstractmethod
    async def generate_models(self, model_definitions: list[dict[str, Any]]) -> str:
        """Generate models/ directory documentation."""
        ...

    @property
    @abstractmethod
    def generate_examples(self, templates: list[str]) -> str:
        """Generate examples directory."""
        ...


class CoreSystem(ABC):
    """Abstract core system management."""

    @abstractmethod
    async def initialize(self, config: dict[str, Any]) -> dict[str, Any]:
        """Initialize the core system."""
        ...

    @abstractmethod
    async def start(self) -> dict[str, Any]:
        """Start the core system."""
        ...

    @abstractmethod
    async def stop(self) -> dict[str, Any]:
        """Stop the core system."""
        ...

    @abstractmethod
    async def health_check(self) -> dict[str, Any]:
        """Perform a health check."""
        ...

    @property
    @abstractmethod
    def version(self) -> str:
        """Core system version."""
        ...

    @property
    @abstractmethod
    def status(self) -> str:
        """Core system status."""
        ...


class CoreSystemManager(ABC):
    """Abstract core system manager for lifecycle coordination."""

    @abstractmethod
    async def create_system(self, name: str, config: dict[str, Any]) -> CoreSystem:
        """Create a core system instance."""
        ...

    @abstractmethod
    async def register_system(self, system: CoreSystem) -> str:
        """Register a system."""
        ...

    @abstractmethod
    async def unregister_system(self, system_id: str) -> bool:
        """Unregister a system."""
        ...

    @abstractmethod
    async def get_system(self, system_id: str) -> CoreSystem | None:
        """Get a system by ID."""
        ...

    @abstractmethod
    async def list_systems(self) -> list[CoreSystem]:
        """List all registered systems."""
        ...


class VersionManager(ABC):
    """Abstract version management."""

    @abstractmethod
    def get_current_version(self) -> str:
        """Get the current version string."""
        ...

    @abstractmethod
    def bump_version(self, level: str = "patch") -> str:
        """Bump version and return new version."""
        ...

    @abstractmethod
    def validate_version(self, version: str) -> bool:
        """Validate version string format."""
        ...

    @abstractmethod
    def generate_release_notes(self, version: str) -> str:
        """Generate release notes for a version."""
        ...


class FeatureTracker(ABC):
    """Abstract feature development tracker."""

    @abstractmethod
    async def register_feature(self, feature: FeatureDefinition) -> str:
        """Register a new feature."""
        ...

    @abstractmethod
    async def update_feature(self, feature_id: str, updates: dict[str, Any]) -> bool:
        """Update an existing feature."""
        ...

    @abstractmethod
    async def remove_feature(self, feature_id: str) -> bool:
        """Remove a feature."""
        ...

    @abstractmethod
    async def get_feature(self, feature_id: str) -> FeatureDefinition | None:
        """Get a feature by ID."""
        ...

    @abstractmethod
    async def list_features(self, status: str | None = None) -> list[FeatureDefinition]:
        """List features, optionally filtered by status."""
        ...

    @abstractmethod
    async def track_task(self, task: TaskDefinition) -> str:
        """Track a development task."""
        ...

    @abstractmethod
    async def complete_task(self, task_id: str, result: dict[str, Any]) -> bool:
        """Mark a task as completed."""
        ...

    @property
    @abstractmethod
    def feature_count(self) -> int:
        """Number of registered features."""
        ...


class PlanExecutor(ABC):
    """Abstract implementation plan executor."""

    @abstractmethod
    async def execute_plan(self, plan: ImplementationPlan) -> dict[str, Any]:
        """Execute an implementation plan."""
        ...

    @abstractmethod
    async def pause_plan(self, plan_id: str) -> bool:
        """Pause plan execution."""
        ...

    @abstractmethod
    async def resume_plan(self, plan_id: str) -> bool:
        """Resume plan execution."""
        ...

    @abstractmethod
    async def cancel_plan(self, plan_id: str) -> bool:
        """Cancel plan execution."""
        ...

    @property
    @abstractmethod
    def active_plans(self) -> list[ImplementationPlan]:
        """Get active plans."""
        ...
