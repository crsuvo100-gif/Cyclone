"""Phase 5: Quality Engine module.

Provides quality gates and metric enforcement for CI/CD:
- Metric thresholds and evaluation
- Quality gate enforcement
- Report generation

Usage:
    from apps.cyclone.phase5.quality_engine import QualityEngineImplementation

    engine = QualityEngineImplementation("ci-main")
    engine.register_metric("test_coverage", 0.80, "ratio")
    engine.register_metric("lint_errors", 0, "count")
    result = engine.evaluate({"test_coverage": 0.85, "lint_errors": 2})
"""

from __future__ import annotations

import hashlib
import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from .interface import QualityEngine, QualityGateError, Phase5Error

logger = logging.getLogger(__name__)


@dataclass
class MetricDefinition:
    """Definition of a quality metric."""
    metric_id: str
    name: str
    threshold: float
    unit: str
    operator: str = ">="


@dataclass
class QualityResult:
    """Result of a quality gate evaluation."""
    metric_id: str
    name: str
    value: float
    threshold: float
    passed: bool
    message: str
    timestamp: float = 0.0


class QualityEngineImplementation(QualityEngine):
    """Implementation of a quality gate engine."""

    def __init__(self, engine_id: str, engine_name: str = "Quality Engine") -> None:
        self._engine_id = engine_id
        self._engine_name = engine_name
        self._metrics: dict[str, MetricDefinition] = {}
        self._results: list[QualityResult] = []

    @property
    def engine_id(self) -> str:
        return self._engine_id

    @property
    def engine_name(self) -> str:
        return self._engine_name

    def register_metric(self, metric_name: str, threshold: float, unit: str) -> str:
        """Register a quality metric."""
        metric_id = f"MET-{self._engine_id}-{hashlib.md5(metric_name.encode()).hexdigest()[:6]}"
        self._metrics[metric_name] = MetricDefinition(
            metric_id=metric_id,
            name=metric_name,
            threshold=threshold,
            unit=unit,
        )
        self._results.append(QualityResult(
            metric_id=metric_id,
            name=metric_name,
            value=0.0,
            threshold=threshold,
            passed=False,
            message="Metric registered, awaiting evaluation",
            timestamp=datetime.now().timestamp(),
        ))
        return metric_id

    def evaluate(self, metrics: dict[str, Any]) -> dict[str, Any]:
        """Evaluate quality metrics."""
        results = []

        for name, definition in self._metrics.items():
            value = metrics.get(name, 0.0)
            passed = value >= definition.threshold

            result = QualityResult(
                metric_id=definition.metric_id,
                name=definition.name,
                value=float(value),
                threshold=definition.threshold,
                passed=passed,
                message="Passed" if passed else f"Below threshold ({value} < {definition.threshold})",
                timestamp=datetime.now().timestamp(),
            )
            results.append(result)

        self._results.extend(results)

        overall_passed = all(r.passed for r in results)
        return {
            "engine_id": self._engine_id,
            "evaluated_at": datetime.now().isoformat(),
            "metrics": [r.__dict__ for r in results],
            "overall_passed": overall_passed,
            "score": sum(1 for r in results if r.passed) / len(results) if results else 0,
        }

    @property
    def metrics(self) -> dict[str, Any]:
        return {name: m.__dict__ for name, m in self._metrics.items()}

    def get_results(self) -> list[dict[str, Any]]:
        return [r.__dict__ for r in self._results]
