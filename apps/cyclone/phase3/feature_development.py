"""Phase 3: Feature Development module.

Provides structured feature development workflow with:
- Feature definitions and acceptance criteria
- Implementation plans with dependencies
- Task tracking and completion
- Plan execution and management
- Version management with semantic versioning
- Core system lifecycle management

Usage:
    from apps.cyclone.phase3.feature_development import (
        FeatureDefinition,
        ImplementationPlan,
        FeatureTracker,
        PlanExecutor,
        VersionManager,
    )
"""

from __future__ import annotations

import hashlib
import logging
import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from .interface import (
    FeatureDefinitionError,
    PlanExecutionError,
    Phase3Error,
    FeatureDefinition,
    ImplementationPlan,
    TaskDefinition,
)

logger = logging.getLogger(__name__)


@dataclass
class TaskDefinitionImplementation(TaskDefinition):
    """Implementation of a development task."""

    task_id: str = ""
    title: str = ""
    description: str = ""
    priority: int = 1
    status: str = "pending"
    created_at: float = field(default_factory=lambda: datetime.now().timestamp())
    assigned_to: str = ""
    tags: list[str] = field(default_factory=list)
    details: dict[str, Any] = field(default_factory=dict)
    parent_feature: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "status": self.status,
            "created_at": self.created_at,
            "assigned_to": self.assigned_to,
            "tags": self.tags,
            "details": self.details,
            "parent_feature": self.parent_feature,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TaskDefinitionImplementation":
        return cls(
            task_id=data.get("task_id", ""),
            title=data.get("title", ""),
            description=data.get("description", ""),
            priority=data.get("priority", 1),
            status=data.get("status", "pending"),
            created_at=data.get("created_at", 0.0),
            assigned_to=data.get("assigned_to", ""),
            tags=data.get("tags", []),
            details=data.get("details", {}),
            parent_feature=data.get("parent_feature", ""),
        )


@dataclass
class FeatureDefinitionImplementation(FeatureDefinition):
    """Implementation of a feature definition."""

    feature_id: str = ""
    name: str = ""
    description: str = ""
    acceptance_criteria: list[str] = field(default_factory=list)
    complexity: str = "medium"
    priority: int = 1
    status: str = "proposed"
    created_at: float = field(default_factory=lambda: datetime.now().timestamp())
    tags: list[str] = field(default_factory=list)
    details: dict[str, Any] = field(default_factory=dict)
    owner: str = "unassigned"

    def to_dict(self) -> dict[str, Any]:
        return {
            "feature_id": self.feature_id,
            "name": self.name,
            "description": self.description,
            "acceptance_criteria": self.acceptance_criteria,
            "complexity": self.complexity,
            "priority": self.priority,
            "status": self.status,
            "created_at": self.created_at,
            "tags": self.tags,
            "details": self.details,
            "owner": self.owner,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "FeatureDefinitionImplementation":
        return cls(
            feature_id=data.get("feature_id", ""),
            name=data.get("name", ""),
            description=data.get("description", ""),
            acceptance_criteria=data.get("acceptance_criteria", []),
            complexity=data.get("complexity", "medium"),
            priority=data.get("priority", 1),
            status=data.get("status", "proposed"),
            created_at=data.get("created_at", 0.0),
            tags=data.get("tags", []),
            details=data.get("details", {}),
            owner=data.get("owner", "unassigned"),
        )


@dataclass
class StepImplementation:
    """Implementation of an implementation plan step."""

    step_id: str
    description: str
    depends_on: list[str] = field(default_factory=list)
    estimated_hours: float = 1.0
    estimated_complexity: str = "medium"
    order: int = 0


@dataclass
class ImplementationPlanImplementation(ImplementationPlan):
    """Implementation of an implementation plan."""

    plan_id: str = ""
    feature_id: str = ""
    steps: list[dict[str, Any]] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)
    estimated_hours: float = 0.0
    status: str = "draft"
    created_at: float = field(default_factory=lambda: datetime.now().timestamp())
    updated_at: float = field(default_factory=lambda: datetime.now().timestamp())
    executed_at: float = 0.0
    results: dict[str, Any] = field(default_factory=dict)

    @property
    def steps_list(self) -> list[StepImplementation]:
        """Get parsed steps as StepImplementation objects."""
        result = []
        for i, step in enumerate(self.steps):
            result.append(StepImplementation(
                step_id=step.get("step_id", f"STEP{i+1:03d}"),
                description=step.get("description", ""),
                depends_on=step.get("depends_on", []),
                estimated_hours=step.get("estimated_hours", 1.0),
                estimated_complexity=step.get("estimated_complexity", "medium"),
                order=step.get("order", i),
            ))
        return result

    def to_dict(self) -> dict[str, Any]:
        return {
            "plan_id": self.plan_id,
            "feature_id": self.feature_id,
            "steps": self.steps,
            "dependencies": self.dependencies,
            "estimated_hours": self.estimated_hours,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "executed_at": self.executed_at,
            "results": self.results,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ImplementationPlanImplementation":
        return cls(
            plan_id=data.get("plan_id", ""),
            feature_id=data.get("feature_id", ""),
            steps=data.get("steps", []),
            dependencies=data.get("dependencies", []),
            estimated_hours=data.get("estimated_hours", 0.0),
            status=data.get("status", "draft"),
            created_at=data.get("created_at", 0.0),
            updated_at=data.get("updated_at", 0.0),
            executed_at=data.get("executed_at", 0.0),
            results=data.get("results", {}),
        )


class FeatureTrackerImplementation:
    """Implementation of feature tracking."""

    def __init__(self, storage_path: str = "~/.hermes/feature_tracker.json") -> None:
        self._storage_path = storage_path
        self._features: dict[str, FeatureDefinitionImplementation] = {}
        self._tasks: dict[str, TaskDefinitionImplementation] = {}
        self._plans: dict[str, ImplementationPlanImplementation] = {}

    async def register_feature(self, feature: FeatureDefinition) -> str:
        """Register a new feature."""
        feature_id = feature.feature_id or f"FEAT-{datetime.now().strftime('%Y%m%d%H%M%S')}-{hash(feature.name) % 10000:04d}"
        feature.feature_id = feature_id
        self._features[feature_id] = feature
        logger.info(f"Feature registered: {feature_id} - {feature.name}")
        return feature_id

    async def update_feature(self, feature_id: str, updates: dict[str, Any]) -> bool:
        """Update an existing feature."""
        if feature_id not in self._features:
            raise FeatureDefinitionError(f"Feature not found: {feature_id}")

        for key, value in updates.items():
            setattr(self._features[feature_id], key, value)

        self._features[feature_id].status = updates.get("status", self._features[feature_id].status)
        self._features[feature_id].updated_at = datetime.now().timestamp()
        return True

    async def remove_feature(self, feature_id: str) -> bool:
        """Remove a feature."""
        if feature_id in self._features:
            del self._features[feature_id]
            return True
        return False

    async def get_feature(self, feature_id: str) -> FeatureDefinitionImplementation | None:
        """Get a feature by ID."""
        return self._features.get(feature_id)

    async def list_features(self, status: str | None = None) -> list[FeatureDefinitionImplementation]:
        """List features, optionally filtered by status."""
        if status:
            return [f for f in self._features.values() if f.status == status]
        return list(self._features.values())

    async def track_task(self, task: TaskDefinition) -> str:
        """Track a development task."""
        task_id = task.task_id or f"TASK-{datetime.now().strftime('%H%M%S')}-{hash(task.title) % 10000:04d}"
        task.task_id = task_id
        self._tasks[task_id] = task
        return task_id

    async def complete_task(self, task_id: str, result: dict[str, Any]) -> bool:
        """Mark a task as completed."""
        if task_id not in self._tasks:
            raise FeatureDefinitionError(f"Task not found: {task_id}")

        task = self._tasks[task_id]
        task.status = "completed"
        task.details["result"] = result
        task.details["completed_at"] = datetime.now().timestamp()
        return True

    @property
    def feature_count(self) -> int:
        return len(self._features)

    @property
    def task_count(self) -> int:
        return len(self._tasks)

    def get_all_tasks(self) -> list[TaskDefinitionImplementation]:
        return list(self._tasks.values())


class PlanExecutorImplementation:
    """Implementation of implementation plan execution."""

    def __init__(self, tracker: FeatureTrackerImplementation | None = None) -> None:
        self._tracker = tracker
        self._execution_log: list[dict[str, Any]] = []
        self._active_plans: list[str] = []

    async def execute_plan(self, plan: ImplementationPlan) -> dict[str, Any]:
        """Execute an implementation plan."""
        if plan.status != "draft":
            raise PlanExecutionError(f"Plan is not in draft state (current: {plan.status})")

        plan.status = "in_progress"
        plan.updated_at = datetime.now().timestamp()

        self._active_plans.append(plan.plan_id)

        # Verify dependencies
        missing_deps = []
        for dep in plan.dependencies:
            if self._tracker and not await self._tracker.get_feature(dep):
                missing_deps.append(dep)

        if missing_deps:
            plan.status = "draft"
            raise FeatureDefinitionError(f"Missing dependencies: {missing_deps}")

        # Execute steps in order
        results = {}
        for step in plan.steps_list:
            try:
                # Simulate step execution
                step_result = {
                    "step_id": step.step_id,
                    "description": step.description,
                    "status": "completed",
                    "duration_seconds": 0.0,
                    "details": {},
                }

                # If actual implementation functions are provided, use them
                if hasattr(self, "_execute_step"):
                    step_result = await self._execute_step(step)

                results[step.step_id] = step_result
            except Exception as exc:
                step_result = {
                    "step_id": step.step_id,
                    "description": step.description,
                    "status": "failed",
                    "error": str(exc),
                }
                results[step.step_id] = step_result
                logger.error(f"Step failed: {step.step_id}: {exc}")
                raise

        # Compute totals
        total_hours = sum(s.get("estimated_hours", 1.0) for s in plan.steps)
        plan.executed_at = datetime.now().timestamp()
        plan.results = results
        plan.status = "completed"
        plan.updated_at = datetime.now().timestamp()

        log_entry = {
            "plan_id": plan.plan_id,
            "feature_id": plan.feature_id,
            "status": "completed",
            "total_hours": total_hours,
            "steps_executed": len(results),
            "timestamp": datetime.now().timestamp(),
        }
        self._execution_log.append(log_entry)

        return log_entry

    async def pause_plan(self, plan_id: str) -> bool:
        """Pause plan execution."""
        if plan_id in self._active_plans:
            self._active_plans.remove(plan_id)
            return True
        return False

    async def resume_plan(self, plan_id: str) -> bool:
        """Resume plan execution."""
        if plan_id not in self._active_plans:
            self._active_plans.append(plan_id)
            return True
        return False

    async def cancel_plan(self, plan_id: str) -> bool:
        """Cancel plan execution."""
        if plan_id in self._active_plans:
            self._active_plans.remove(plan_id)
            return True
        return False

    @property
    def active_plans(self) -> list[ImplementationPlan]:
        """Get active plans."""
        return [p for p in self._plans.values() if p.status == "in_progress"]


class VersionManagerImplementation:
    """Implementation of semantic version management."""

    _VERSION_PATTERN = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")

    def __init__(self, version: str = "1.0.0") -> None:
        if not self.validate_version(version):
            raise VersionError(f"Invalid version format: {version}")
        self._version = version

    def get_current_version(self) -> str:
        return self._version

    def bump_version(self, level: str = "patch") -> str:
        """Bump version and return new version."""
        match = self._VERSION_PATTERN.match(self._version)
        if not match:
            raise VersionError(f"Invalid version format: {self._version}")

        major, minor, patch = int(match.group(1)), int(match.group(2)), int(match.group(3))

        if level == "major":
            major += 1
            minor = 0
            patch = 0
        elif level == "minor":
            minor += 1
            patch = 0
        elif level == "patch":
            patch += 1
        else:
            raise VersionError(f"Invalid bump level: {level}")

        new_version = f"{major}.{minor}.{patch}"
        self._version = new_version
        return new_version

    def validate_version(self, version: str) -> bool:
        """Validate version string format."""
        return bool(self._VERSION_PATTERN.match(version))

    def generate_release_notes(self, version: str) -> str:
        """Generate release notes for a version."""
        return f"Release notes for version {version}"

    def parse_version(self) -> tuple[int, int, int]:
        """Parse version into tuple."""
        match = self._VERSION_PATTERN.match(self._version)
        if not match:
            return (0, 0, 0)
        return (int(match.group(1)), int(match.group(2)), int(match.group(3)))


__all__ = [
    "FeatureDefinitionImplementation",
    "TaskDefinitionImplementation",
    "ImplementationPlanImplementation",
    "FeatureTrackerImplementation",
    "PlanExecutorImplementation",
    "VersionManagerImplementation",
]

# Module-level aliases for package API compatibility
FeatureDefinition = FeatureDefinitionImplementation
TaskDefinition = TaskDefinitionImplementation
ImplementationPlan = ImplementationPlanImplementation
FeatureTracker = FeatureTrackerImplementation
PlanExecutor = PlanExecutorImplementation
VersionManager = VersionManagerImplementation
