"""Phase 3: Feature Development + Documentation + Core System module.

Provides:
- Feature definition and implementation planning
- Task decomposition and tracking
- Documentation generation (README, CHANGELOG, CONTRIBUTING)
- Core system lifecycle management
- Version management

Usage:
    from apps.cyclone.phase3 import (
        FeatureDefinition,
        ImplementationPlan,
        DocumentationGenerator,
        CoreSystemManager,
    )
"""

from .interface import (
    Phase3Error,
    FeatureDefinitionError,
    PlanExecutionError,
    DocumentationError,
    VersionError,
    FeatureDefinition,
    ImplementationPlan,
    TaskDefinition,
    FeatureTracker,
    PlanExecutor,
    VersionManager,
)

from .feature_development import (
    FeatureDefinition,
    ImplementationPlan,
    TaskDefinition,
    FeatureTracker,
    PlanExecutor,
    VersionManager,
)

from .documentation_generator import DocumentationGeneratorImplementation as DocumentationGenerator

from .core_system import (
    CoreSystemImplementation as CoreSystem,
    CoreSystemManagerImplementation as CoreSystemManager,
)

__version__ = "1.0.0"

__all__ = [
    "Phase3Error",
    "FeatureDefinitionError",
    "PlanExecutionError",
    "DocumentationError",
    "VersionError",
    "FeatureDefinition",
    "ImplementationPlan",
    "TaskDefinition",
    "FeatureTracker",
    "PlanExecutor",
    "VersionManager",
    "DocumentationGenerator",
    "CoreSystem",
    "CoreSystemManager",
    "__version__",
]
