"""Phase 4: Release Manager module.

Provides release management:
- Release creation and publishing
- Version management

Usage:
    from apps.cyclone.phase4.release_manager import ReleaseManagerImplementation

    manager = ReleaseManagerImplementation()
    release = await manager.create_release("13.0")
"""

from __future__ import annotations

import hashlib
import logging
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from .interface import (
    Release,
    ReleaseManager,
    ReleaseError,
)

logger = logging.getLogger(__name__)


@dataclass
class ReleaseImplementation(Release):
    """Implementation of a release."""
    release_id: str = ""
    version: str = ""
    artifacts: list[dict[str, Any]] = field(default_factory=list)
    changes: list[str] = field(default_factory=list)
    status: str = "draft"
    created_at: float = 0.0
    published_at: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "release_id": self.release_id,
            "version": self.version,
            "artifacts": self.artifacts,
            "changes": self.changes,
            "status": self.status,
            "created_at": self.created_at,
            "published_at": self.published_at,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ReleaseImplementation":
        return cls(
            release_id=data.get("release_id", ""),
            version=data.get("version", ""),
            artifacts=data.get("artifacts", []),
            changes=data.get("changes", []),
            status=data.get("status", "draft"),
            created_at=data.get("created_at", 0.0),
            published_at=data.get("published_at", 0.0),
            metadata=data.get("metadata", {}),
        )


class ReleaseManagerImplementation(ReleaseManager):
    """Implementation of a release manager."""

    def __init__(self, releases_file: str = "~/.hermes/releases.json") -> None:
        self.releases_file = releases_file
        self._releases: list[ReleaseImplementation] = []
        self._current_version = "1.0.0"

    def _generate_release_id(self) -> str:
        return f"REL-{datetime.now().strftime('%Y%m%d%H%M%S')}-{hashlib.md5(self._current_version.encode()).hexdigest()[:6]}"

    async def create_release(self, version: str, changes: list[str]) -> Release:
        """Create a new release."""
        release = ReleaseImplementation(
            release_id=self._generate_release_id(),
            version=version,
            artifacts=[],
            changes=changes,
            status="draft",
            created_at=time.time(),
        )
        self._releases.append(release)
        return release

    async def publish_release(self, release: Release) -> dict[str, Any]:
        """Publish a release."""
        release_id = release.release_id
        release_obj = None
        for r in self._releases:
            if r.release_id == release_id:
                release_obj = r
                break

        if release_obj is None:
            raise ReleaseError(f"Release not found: {release_id}")

        if release_obj.status != "draft":
            raise ReleaseError(f"Release is not draft (current: {release_obj.status})")

        release_obj.status = "published"
        release_obj.published_at = time.time()

        logger.info(f"Published release: {release_obj.version}")

        return {
            "release_id": release_obj.release_id,
            "version": release_obj.version,
            "status": "published",
            "published_at": release_obj.published_at,
        }

    async def list_releases(self) -> list[Release]:
        """List releases."""
        return list(self._releases)

    @property
    def current_version(self) -> str:
        return self._current_version

    def set_current_version(self, version: str) -> None:
        """Set the current version."""
        if not self._validate_version(version):
            raise ReleaseError(f"Invalid version: {version}")
        self._current_version = version


__all__ = [
    "ReleaseImplementation",
    "ReleaseManagerImplementation",
]
