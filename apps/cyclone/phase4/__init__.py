"""Phase 4: Testing + Build + Integration module.

Provides testing, build, CI/CD, deployment, and release management:
- Test execution (unit, integration, e2e)
- Build system (Python, Node.js, Docker)
- Pipeline execution for CI/CD
- Deployment management with rollback
- Release management with versioning

Usage:
    from apps.cyclone.phase4 import (
        TestExecutorImplementation,
        BuildManagerImplementation,
        PipelineExecutorImplementation,
        DeploymentManagerImplementation,
    )
"""

from .test_execution import (
    TestExecutorImplementation,
    TestCaseImplementation,
    TestSuiteImplementation,
    TestResultImplementation,
    CoverageReporter,
)

from .build_system import (
    BuildManagerImplementation,
    BuildArtifactImplementation,
)

from .pipeline_executor import (
    PipelineExecutorImplementation,
    PipelineStep,
    PipelineExecution,
)

from .deployment_manager import (
    DeploymentManagerImplementation,
    DeploymentTargetImplementation,
    DeploymentRecord,
)

from .release_manager import (
    ReleaseManagerImplementation,
    ReleaseImplementation,
)

from .quality_gate import (
    QualityGateImplementation,
    QualityMetrics,
    QualityGate,
)

__version__ = "1.0.0"

__all__ = [
    "TestExecutorImplementation",
    "TestCaseImplementation",
    "TestSuiteImplementation",
    "TestResultImplementation",
    "CoverageReporter",
    "BuildManagerImplementation",
    "BuildArtifactImplementation",
    "PipelineExecutorImplementation",
    "PipelineStep",
    "PipelineExecution",
    "DeploymentManagerImplementation",
    "DeploymentTargetImplementation",
    "DeploymentRecord",
    "ReleaseManagerImplementation",
    "ReleaseImplementation",
    "QualityGateImplementation",
    "QualityMetrics",
    "QualityGate",
    "__version__",
]
