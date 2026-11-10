"""Phase 4: Quality Gate module.

Provides quality gate evaluation for CI/CD:
- Metrics collection
- Gate evaluation

Usage:
    from apps.cyclone.phase4.quality_gate import QualityGateImplementation

    gate = QualityGateImplementation("test coverage >= 80%", 0.8)
    passed = gate.evaluate({"test_coverage": 0.85})
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

from .interface import (
    QualityGate,
    Phase4Error,
)

logger = logging.getLogger(__name__)


@dataclass
class QualityMetrics:
    """Quality metrics container."""
    test_coverage: float = 0.0
    unit_test_pass_rate: float = 0.0
    integration_test_pass_rate: float = 0.0
    lint_errors: int = 0
    build_time_seconds: float = 0.0
    deployment_time_seconds: float = 0.0
    error_rate: float = 0.0
    response_time_p95: float = 0.0
    cpu_usage: float = 0.0
    memory_usage: float = 0.0


class QualityGateImplementation(QualityGate):
    """Implementation of a quality gate."""

    def __init__(self, name: str, threshold: float, threshold_units: str = "percentage") -> None:
        self._name = name
        self._threshold = threshold
        self._threshold_units = threshold_units

    @property
    def name(self) -> str:
        return self._name

    @property
    def threshold(self) -> float:
        return self._threshold

    @property
    def threshold_units(self) -> str:
        return self._threshold_units

    def evaluate(self, metrics: dict[str, Any]) -> bool:
        """Evaluate quality gate against metrics."""
        value = metrics.get("value", 0.0)

        if self._threshold_units == "percentage":
            return value >= self._threshold * 100
        elif self._threshold_units == "ratio":
            return value >= self._threshold
        else:
            return value >= self._threshold


__all__ = [
    "QualityMetrics",
    "QualityGateImplementation",
]
