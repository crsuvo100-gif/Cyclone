"""Phase 4: Build System module.

Provides build and compilation infrastructure:
- Multi-target builds (Python, Node.js, Docker)
- Build artifact management
- Build cache
- Build configuration

Usage:
    from apps.cyclone.phase4.build_system import BuildManagerImplementation

    builder = BuildManagerImplementation()
    artifact = await builder.build("all")
"""

from __future__ import annotations

import hashlib
import logging
import os
import shutil
import subprocess
import tempfile
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from .interface import (
    BuildArtifact,
    BuildManager,
    BuildError,
)

logger = logging.getLogger(__name__)


@dataclass
class BuildArtifactImplementation(BuildArtifact):
    """Implementation of a build artifact."""

    artifact_id: str = ""
    artifact_type: str = ""
    target: str = ""
    path: str | None = None
    size: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "artifact_id": self.artifact_id,
            "artifact_type": self.artifact_type,
            "target": self.target,
            "path": self.path,
            "size": self.size,
            "metadata": self.metadata,
        }

    def exists(self) -> bool:
        if self.path:
            return os.path.exists(self.path)
        return False


class BuildManagerImplementation(BuildManager):
    """Implementation of a build manager."""

    def __init__(self, project_root: str = ".") -> None:
        self.project_root = Path(project_root).resolve()
        self._artifacts: list[BuildArtifactImplementation] = []
        self._cache: dict[str, Any] = {}
        self._build_dir = self.project_root / "build"

    async def build(self, target: str, config: dict[str, Any] | None = None) -> BuildArtifact:
        """Build a target."""
        config = config or {}
        target = target.lower().strip()

        artifact_id = f"BUILD-{datetime.now().strftime('%Y%m%d%H%M%S')}-{hashlib.md5(target.encode()).hexdigest()[:8]}"

        if target == "all":
            return await self._build_all(config)
        elif target == "python":
            return await self._build_python(config)
        elif target == "node":
            return await self._build_node(config)
        elif target == "docker":
            return await self._build_docker(config)
        elif target == "clean":
            return await self._clean(config)
        else:
            raise BuildError(f"Unknown build target: {target}")

    async def _build_all(self, config: dict[str, Any]) -> BuildArtifact:
        """Build all targets."""
        logger.info("Building all targets...")

        python_artifact = await self._build_python(config)
        node_artifact = await self._build_node(config)
        docker_artifact = await self._build_docker(config)

        self._artifacts.extend([python_artifact, node_artifact, docker_artifact])

        return BuildArtifactImplementation(
            artifact_id=artifact_id,
            artifact_type="all",
            target="all",
            metadata={"python": python_artifact.path, "node": node_artifact.path, "docker": docker_artifact.path},
        )

    async def _build_python(self, config: dict[str, Any]) -> BuildArtifact:
        """Build Python target."""
        logger.info("Building Python target...")

        with tempfile.NamedTemporaryFile(suffix=".log", delete=False) as f:
            log_path = f.name

        try:
            # In a real project, this would run: python -m build or pip install -e .
            cmd = [sys.executable, "-m", "compileall", "-q", str(self.project_root)]
            result = await self._run_subprocess(cmd, log_path)

            if result.returncode != 0:
                raise BuildError(f"Python build failed: {result.stderr}")

            artifact = BuildArtifactImplementation(
                artifact_id=artifact_id,
                artifact_type="python",
                target="python",
                path=str(self.project_root / "build" / "__pycache__"),
                metadata={"command": " ".join(cmd), "python_version": sys.version},
            )
            return artifact
        finally:
            if os.path.exists(log_path):
                os.unlink(log_path)

    async def _build_node(self, config: dict[str, Any]) -> BuildArtifact:
        """Build Node.js target."""
        logger.info("Building Node.js target...")

        with tempfile.NamedTemporaryFile(suffix=".log", delete=False) as f:
            log_path = f.name

        try:
            # Find the CYCLONE server directory
            server_dir = self.project_root
            cmd = ["npm", "run", "build", "--prefix", str(server_dir)]
            result = await self._run_subprocess(cmd, log_path)

            if result.returncode != 0:
                raise BuildError(f"Node build failed: {result.stderr}")

            artifact = BuildArtifactImplementation(
                artifact_id=artifact_id,
                artifact_type="node",
                target="node",
                path=str(server_dir / "dist"),
                metadata={"command": " ".join(cmd), "node_version": ""},
            )
            return artifact
        finally:
            if os.path.exists(log_path):
                os.unlink(log_path)

    async def _build_docker(self, config: dict[str, Any]) -> BuildArtifact:
        """Build Docker target."""
        logger.info("Building Docker target...")

        dockerfile = self.project_root / "Dockerfile"
        if not dockerfile.exists():
            # Try to find docker-compose
            compose = self.project_root / "docker-compose.yml"
            if not compose.exists():
                raise BuildError("No Dockerfile or docker-compose.yml found")

            cmd = ["docker-compose", "build"]
            with tempfile.NamedTemporaryFile(suffix=".log", delete=False) as f:
                log_path = f.name

            try:
                result = await self._run_subprocess(cmd, log_path)
                if result.returncode != 0:
                    raise BuildError(f"Docker build failed: {result.stderr}")
            finally:
                if os.path.exists(log_path):
                    os.unlink(log_path)

            return BuildArtifactImplementation(
                artifact_id=artifact_id,
                artifact_type="docker",
                target="docker",
                metadata={"command": " ".join(cmd)},
            )
        else:
            cmd = ["docker", "build", "-t", "moon-cyclone:dev", str(self.project_root)]
            with tempfile.NamedTemporaryFile(suffix=".log", delete=False) as f:
                log_path = f.name

            try:
                result = await self._run_subprocess(cmd, log_path)
                if result.returncode != 0:
                    raise BuildError(f"Docker build failed: {result.stderr}")
            finally:
                if os.path.exists(log_path):
                    os.unlink(log_path)

            return BuildArtifactImplementation(
                artifact_id=artifact_id,
                artifact_type="docker",
                target="docker",
                metadata={"command": " ".join(cmd), "image": "moon-cyclone:dev"},
            )

    async def _clean(self, config: dict[str, Any]) -> BuildArtifact:
        """Clean build artifacts."""
        logger.info("Cleaning build artifacts...")

        self._build_dir.mkdir(exist_ok=True)
        for item in self._build_dir.iterdir():
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()

        self._artifacts.clear()

        return BuildArtifactImplementation(
            artifact_id=artifact_id,
            artifact_type="clean",
            target="clean",
            metadata={"cleaned": True},
        )

    async def _run_subprocess(self, cmd: list[str], log_path: str) -> subprocess.CompletedProcess:
        """Run a subprocess asynchronously."""
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, lambda: subprocess.run(cmd, capture_output=True, text=True, timeout=300))
        with open(log_path, "w") as f:
            f.write(f"STDOUT:{result.stdout}\nSTDERR:{result.stderr}")
        return result

    @property
    def build_cache(self) -> dict[str, Any]:
        return self._cache

    async def list_artifacts(self) -> list[BuildArtifactImplementation]:
        """List all build artifacts."""
        return list(self._artifacts)


async def build_project(target: str = "all", config: dict[str, Any] | None = None) -> BuildArtifact:
    """Convenience function to build the project."""
    builder = BuildManagerImplementation()
    return await builder.build(target, config)
