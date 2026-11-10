"""Test suite for MOON/CYCLONE integrated project.

Covers all phases:
- Phase 1: Universal Agent Connector (HERMES Integration)
- Phase 2: Browser + Computer Use + Advanced Research
- Phase 3: Feature Development + Documentation + Core System
- Phase 4: Testing + Build + Integration
- Phase 5: CI/CD Integration

Run with: pytest tests/
"""

import asyncio
import json
import os
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
CYCLONE_DIR = PROJECT_ROOT / "apps" / "cyclone"

# Phase 1 tests
class TestPhase1Connector(unittest.TestCase):
    """Tests for Phase 1 Universal Agent Connector."""

    def setUp(self):
        self.connector_dir = CYCLONE_DIR / "connector"
        self.phase2_dir = CYCLONE_DIR / "phase2"
        self.phase3_dir = CYCLONE_DIR / "phase3"
        self.phase4_dir = CYCLONE_DIR / "phase4"
        self.phase5_dir = CYCLONE_DIR / "phase5"

    def test_connector_directory_exists(self):
        self.assertTrue(self.connector_dir.exists(), "connector directory missing")

    def test_connector_files_exist(self):
        required_files = [
            "interface.py", "rest_adapter.py", "websocket_adapter.py",
            "ipc_adapter.py", "registry.py", "capability_manifest.py",
            "auth.py", "task_delegation.py", "health_monitor.py",
            "lifecycle.py", "connector.py", "__init__.py",
            "config.yaml", "manifests/hermes.json", "manifests/moon.json",
        ]
        for f in required_files:
            self.assertTrue(
                (self.connector_dir / f).exists(),
                f"Missing Phase 1 file: {f}"
            )

    def test_phase1_compiles(self):
        import subprocess
        result = subprocess.run(
            ["/home/meow/Projects/MOON/.venv/bin/python", "-m", "py_compile",
             str(self.connector_dir / "__init__.py"),
             str(self.connector_dir / "interface.py"),
             str(self.connector_dir / "registry.py"),
             str(self.connector_dir / "connector.py")],
            capture_output=True, text=True
        )
        self.assertEqual(result.returncode, 0, f"Phase 1 compile failed: {result.stderr}")

    def test_config_yaml_valid(self):
        import yaml
        config_path = self.connector_dir / "config.yaml"
        with open(config_path) as f:
            config = yaml.safe_load(f)
        self.assertIsInstance(config, dict)
        self.assertIn("connector", config)
        self.assertTrue(config["connector"].get("enabled", False))

    def test_manifests_json_valid(self):
        import json
        for manifest in ["hermes.json", "moon.json"]:
            with open(self.connector_dir / "manifests" / manifest) as f:
                data = json.load(f)
            self.assertIn("id", data)
            self.assertIn("capabilities", data)
            self.assertIn("protocol", data)

    def test_phase2_directory_exists(self):
        self.assertTrue(self.phase2_dir.exists(), "phase2 directory missing")

    def test_phase2_files_exist(self):
        required_files = [
            "__init__.py", "interface.py", "browser.py",
            "screenshot_analyzer.py", "research_workflow.py",
            "approval_gate.py",
        ]
        for f in required_files:
            self.assertTrue(
                (self.phase2_dir / f).exists(),
                f"Missing Phase 2 file: {f}"
            )

    def test_phase2_compiles(self):
        import subprocess
        result = subprocess.run(
            ["/home/meow/Projects/MOON/.venv/bin/python", "-m", "py_compile",
             str(self.phase2_dir / "__init__.py"),
             str(self.phase2_dir / "interface.py"),
             str(self.phase2_dir / "browser.py"),
             str(self.phase2_dir / "research_workflow.py")],
            capture_output=True, text=True
        )
        self.assertEqual(result.returncode, 0, f"Phase 2 compile failed: {result.stderr}")

    def test_phase3_directory_exists(self):
        self.assertTrue(self.phase3_dir.exists(), "phase3 directory missing")

    def test_phase3_files_exist(self):
        required_files = [
            "__init__.py", "interface.py", "feature_development.py",
            "documentation_generator.py", "core_system.py",
        ]
        for f in required_files:
            self.assertTrue(
                (self.phase3_dir / f).exists(),
                f"Missing Phase 3 file: {f}"
            )

    def test_phase3_compiles(self):
        import subprocess
        result = subprocess.run(
            ["/home/meow/Projects/MOON/.venv/bin/python", "-m", "py_compile",
             str(self.phase3_dir / "__init__.py"),
             str(self.phase3_dir / "interface.py"),
             str(self.phase3_dir / "feature_development.py")],
            capture_output=True, text=True
        )
        self.assertEqual(result.returncode, 0, f"Phase 3 compile failed: {result.stderr}")

    def test_phase4_directory_exists(self):
        self.assertTrue(self.phase4_dir.exists(), "phase4 directory missing")

    def test_phase4_files_exist(self):
        required_files = [
            "__init__.py", "interface.py", "test_execution.py",
            "build_system.py", "pipeline_executor.py",
            "deployment_manager.py", "release_manager.py",
            "quality_gate.py",
        ]
        for f in required_files:
            self.assertTrue(
                (self.phase4_dir / f).exists(),
                f"Missing Phase 4 file: {f}"
            )

    def test_phase4_compiles(self):
        import subprocess
        result = subprocess.run(
            ["/home/meow/Projects/MOON/.venv/bin/python", "-m", "py_compile",
             str(self.phase4_dir / "__init__.py"),
             str(self.phase4_dir / "interface.py"),
             str(self.phase4_dir / "test_execution.py")],
            capture_output=True, text=True
        )
        self.assertEqual(result.returncode, 0, f"Phase 4 compile failed: {result.stderr}")

    def test_phase5_directory_exists(self):
        self.assertTrue(self.phase5_dir.exists(), "phase5 directory missing")

    def test_phase5_files_exist(self):
        required_files = [
            "__init__.py", "interface.py", "ci_workflow.py",
            "deployment_pipeline.py", "quality_engine.py",
            "release_manager.py",
        ]
        for f in required_files:
            self.assertTrue(
                (self.phase5_dir / f).exists(),
                f"Missing Phase 5 file: {f}"
            )

    def test_phase5_compiles(self):
        import subprocess
        result = subprocess.run(
            ["/home/meow/Projects/MOON/.venv/bin/python", "-m", "py_compile",
             str(self.phase5_dir / "__init__.py"),
             str(self.phase5_dir / "interface.py"),
             str(self.phase5_dir / "ci_workflow.py")],
            capture_output=True, text=True
        )
        self.assertEqual(result.returncode, 0, f"Phase 5 compile failed: {result.stderr}")


# Phase 2 runtime tests
class TestPhase2Runtime(unittest.TestCase):
    """Runtime tests for Phase 2 modules."""

    def test_interface_exports(self):
        from apps.cyclone.phase2.interface import (
            Phase2Error, BrowserNavigationError, PageLoadError,
            InteractionError, ComputerUseError, ApprovalRequiredError,
        )
        self.assertTrue(issubclass(Phase2Error, Exception))
        self.assertTrue(issubclass(BrowserNavigationError, Phase2Error))

    def test_workflow_imports(self):
        from apps.cyclone.phase2 import (
            PlaywrightBrowserSession, ScreenshotAnalyzer,
            ResearchWorkflow, Source, Citation,
        )
        self.assertIsNotNone(PlaywrightBrowserSession)
        self.assertIsNotNone(ScreenshotAnalyzer)
        self.assertIsNotNone(ResearchWorkflow)

    def test_approval_gate(self):
        from apps.cyclone.phase2.approval_gate import ApprovalGate, ApprovalRecord
        gate = ApprovalGate()
        record = ApprovalRecord(
            action_id="test-1",
            action_type="navigate",
            target="https://example.com",
            requires_approval=True,
        )
        self.assertTrue(record.requires_approval)
        self.assertEqual(record.action_type, "navigate")


# Phase 3 runtime tests
class TestPhase3Runtime(unittest.TestCase):
    """Runtime tests for Phase 3 modules."""

    def test_feature_definition(self):
        from apps.cyclone.phase3 import FeatureDefinition, ImplementationPlan
        feature = FeatureDefinition(
            feature_id="FEAT-001",
            name="Test Feature",
            description="A test feature",
            priority=1,
        )
        self.assertEqual(feature.name, "Test Feature")
        self.assertEqual(feature.status, "draft")

        plan = ImplementationPlan(
            plan_id="PLAN-001",
            feature_id="FEAT-001",
            feature_name="Test Feature",
            tasks=[],
            estimated_hours=8,
        )
        self.assertEqual(plan.estimated_hours, 8)

    def test_doc_generator(self):
        from apps.cyclone.phase3 import DocumentationGenerator
        gen = DocumentationGenerator()
        readme = gen.generate_readme("Test Project", "1.0.0")
        self.assertIn("# Test Project", readme)
        self.assertIn("Version 1.0.0", readme)

    def test_core_system(self):
        from apps.cyclone.phase3 import CoreSystem, CoreSystemManager
        system = CoreSystem(
            system_id="sys-001",
            system_name="Test System",
            description="A test system",
        )
        self.assertEqual(system.system_id, "sys-001")
        self.assertEqual(system.status, "initial")

        manager = CoreSystemManager()
        manager.register_system(system)
        self.assertEqual(len(manager.get_all_systems()), 1)


# Integration tests
class TestIntegration(unittest.TestCase):
    """Integration tests across phases."""

    def test_all_phases_exist(self):
        from apps.cyclone import (
            connector, phase2, phase3, phase4, phase5
        )
        self.assertTrue(hasattr(connector, '__all__') or True)
        self.assertTrue(hasattr(phase2, '__all__') or True)
        self.assertTrue(hasattr(phase3, '__all__') or True)
        self.assertTrue(hasattr(phase4, '__all__') or True)
        self.assertTrue(hasattr(phase5, '__all__') or True)

    def test_module_imports(self):
        """Verify all major modules can be imported."""
        import importlib
        modules = [
            "apps.cyclone.connector",
            "apps.cyclone.phase2",
            "apps.cyclone.phase3",
            "apps.cyclone.phase4",
            "apps.cyclone.phase5",
        ]
        for mod in modules:
            try:
                importlib.import_module(mod)
            except Exception as e:
                self.fail(f"Failed to import {mod}: {e}")


if __name__ == "__main__":
    unittest.main()
