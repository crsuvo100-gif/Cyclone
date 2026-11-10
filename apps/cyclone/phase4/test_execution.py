"""Phase 4: Test Execution module.

Provides test execution infrastructure:
- Unit test runner
- Integration test runner
- End-to-end test runner
- Test result collection and reporting
- Test coverage reporting

Usage:
    from apps.cyclone.phase4.test_execution import TestExecutorImplementation

    executor = TestExecutorImplementation()
    results = await executor.run_tests(suites)
"""

from __future__ import annotations

import asyncio
import hashlib
import logging
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from .interface import (
    TestCase,
    TestResult,
    TestSuite,
    TestError,
    TestExecutor,
)

logger = logging.getLogger(__name__)


@dataclass
class TestCaseImplementation(TestCase):
    """Implementation of a test case."""

    test_id: str = ""
    test_name: str = ""
    description: str = ""
    category: str = "unit"
    priority: int = 1
    timeout: float = 30.0
    test_func: Any = None
    setup_func: Any = None
    teardown_func: Any = None
    enabled: bool = True
    tags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "test_id": self.test_id,
            "test_name": self.test_name,
            "description": self.description,
            "category": self.category,
            "priority": self.priority,
            "timeout": self.timeout,
            "enabled": self.enabled,
            "tags": self.tags,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TestCaseImplementation":
        return cls(
            test_id=data.get("test_id", ""),
            test_name=data.get("test_name", ""),
            description=data.get("description", ""),
            category=data.get("category", "unit"),
            priority=data.get("priority", 1),
            timeout=data.get("timeout", 30.0),
            enabled=data.get("enabled", True),
            tags=data.get("tags", []),
        )


@dataclass
class TestSuiteImplementation(TestSuite):
    """Implementation of a test suite."""

    suite_id: str = ""
    suite_name: str = ""
    tests: list[TestCaseImplementation] = field(default_factory=list)
    description: str = ""
    enabled: bool = True

    def to_dict(self) -> dict[str, Any]:
        return {
            "suite_id": self.suite_id,
            "suite_name": self.suite_name,
            "description": self.description,
            "enabled": self.enabled,
            "tests": [t.to_dict() for t in self.tests],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TestSuiteImplementation":
        tests = [TestCaseImplementation.from_dict(t) for t in data.get("tests", [])]
        return cls(
            suite_id=data.get("suite_id", ""),
            suite_name=data.get("suite_name", ""),
            tests=tests,
            description=data.get("description", ""),
            enabled=data.get("enabled", True),
        )


@dataclass
class TestResultImplementation(TestResult):
    """Implementation of a test result."""

    test_id: str = ""
    status: str = "pending"
    duration: float = 0.0
    output: str = ""
    error: str | None = None
    start_time: float = 0.0
    end_time: float = 0.0
    meta: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "test_id": self.test_id,
            "status": self.status,
            "duration": self.duration,
            "output": self.output,
            "error": self.error,
            "meta": self.meta,
        }


class TestExecutorImplementation(TestExecutor):
    """Implementation of a test executor."""

    def __init__(self, report_dir: str = "test-reports") -> None:
        self.report_dir = report_dir
        self._results: list[TestResultImplementation] = []
        self._executing = False
        self._run_count = 0

    async def run_tests(self, suites: list[TestSuite]) -> list[TestResult]:
        """Run a suite of tests."""
        self._run_count += 1
        self._executing = True

        all_results = []

        for suite in suites:
            if not suite.enabled:
                continue

            for test in suite.tests:
                result = await self.run_single_test(test)
                all_results.append(result)

        self._results = all_results
        self._executing = False

        return all_results

    async def run_single_test(self, test: TestCase) -> TestResultImplementation:
        """Run a single test case."""
        result = TestResultImplementation(
            test_id=test.test_id,
            test_name=test.test_name,
        )

        try:
            result.start_time = time.time()
            result.status = "running"

            if test.setup_func:
                await test.setup_func()

            import time as _time
            test_start = _time.perf_counter()

            if test.test_func:
                await test.test_func()
                result.status = "passed"
            else:
                result.status = "skipped"
                result.error = "No test function provided"

            test_duration = _time.perf_counter() - test_start
            result.duration = test_duration

            result.end_time = time.time()

            if result.status != "passed":
                result.error = f"Test {result.status}: {test.test_name}"

            logger.info(f"Test complete: {test.test_id} - {result.status}")
        except Exception as exc:
            result.status = "failed"
            result.error = str(exc)
            result.duration = time.time() - result.start_time
            result.end_time = time.time()
            logger.error(f"Test failed: {test.test_id}: {exc}")

        self._results.append(result)
        return result

    async def get_test_results(self, test_id: str) -> TestResultImplementation | None:
        """Get test results by ID."""
        for result in self._results:
            if result.test_id == test_id:
                return result
        return None

    @property
    def results(self) -> list[TestResult]:
        return list(self._results)

    def generate_summary(self) -> dict[str, Any]:
        """Generate a test summary."""
        total = len(self._results)
        passed = sum(1 for r in self._results if r.status == "passed")
        failed = sum(1 for r in self._results if r.status == "failed")
        skipped = sum(1 for r in self._results if r.status == "skipped")

        return {
            "run_id": self._run_count,
            "total": total,
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "pass_rate": passed / total if total > 0 else 0,
            "timestamp": datetime.now().isoformat(),
        }


class CoverageReporter:
    """Simple code coverage reporter."""

    def __init__(self, report_file: str = "coverage_report.md") -> None:
        self.report_file = report_file
        self._coverage: dict[str, int] = {}

    def add_file_coverage(self, file_path: str, coverage: int) -> None:
        """Add coverage for a file."""
        self._coverage[file_path] = coverage

    def generate_report(self) -> str:
        """Generate coverage report."""
        if not self._coverage:
            return "# Coverage Report\n\nNo coverage data available."

        total = sum(self._coverage.values())
        count = len(self._coverage)
        avg = total / count

        lines = []
        lines.append("# Code Coverage Report")
        lines.append("")
        lines.append(f"Generated: {datetime.now().isoformat()}")
        lines.append("")
        lines.append(f"Files measured: {count}")
        lines.append(f"Average coverage: {avg:.1f}%")
        lines.append(f"Total coverage: {total}%")
        lines.append("")
        lines.append("## File Breakdown")
        lines.append("")
        lines.append("| File | Coverage |")
        lines.append("|------|----------|")
        for file, cov in sorted(self._coverage.items(), key=lambda x: x[1]):
            lines.append(f"| {file} | {cov}% |")
        lines.append("")

        return "\n".join(lines)


__all__ = [
    "TestCaseImplementation",
    "TestSuiteImplementation",
    "TestResultImplementation",
    "TestExecutorImplementation",
    "CoverageReporter",
]
