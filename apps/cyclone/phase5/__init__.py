"""Phase 5: CI/CD Integration module.

Provides continuous integration and delivery features:
- CI workflows with triggers
- Deployment pipelines with rollback
- Quality engines for metric enforcement
- Release management

Usage:
    from apps.cyclone.phase5 import (
        CIWorkflowImplementation,
        DeploymentPipelineImplementation,
        QualityEngineImplementation,
        ReleaseManagerImplementation,
    )
"""

from .interface import (
    CIWorkflow,
    DeploymentPipeline,
    QualityEngine,
    ReleaseManager,
    Phase5Error,
    CIError,
    DeploymentError,
    QualityGateError,
    ReleaseError,
)

from .ci_workflow import (
    CIWorkflowImplementation,
    CIWorkflowExecutor,
)

from .deployment_pipeline import (
    DeploymentPipelineImplementation,
    DeploymentPipelineExecutor,
    DeploymentRecord,
)

from .quality_engine import (
    QualityEngineImplementation,
    MetricDefinition,
    QualityResult,
)

from .release_manager import (
    ReleaseManagerImplementation,
    Release,
)

__version__ = "1.0.0"

__all__ = [
    "CIWorkflow",
    "DeploymentPipeline",
    "QualityEngine",
    "ReleaseManager",
    "Phase5Error",
    "CIError",
    "DeploymentError",
    "QualityGateError",
    "ReleaseError",
    "CIWorkflowImplementation",
    "CIWorkflowExecutor",
    "DeploymentPipelineImplementation",
    "DeploymentPipelineExecutor",
    "DeploymentRecord",
    "MetricDefinition",
    "QualityResult",
    "ReleaseManagerImplementation",
    "Release",
    "__version__",
]
