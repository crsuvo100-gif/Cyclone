"""Capability Manifest - Capability Discovery and Validation."""

import json
import os
import time
from typing import Any, Dict, List
from pathlib import Path


class CapabilityManifest:
    """Manages capability manifests and compatibility validation."""

    def __init__(self, manifests_dir: Optional[str] = None):
        self.manifests_dir = manifests_dir or os.path.join(os.path.dirname(__file__), "manifests")
        self.manifests: Dict[str, Dict[str, Any]] = {}
        self._load()

    def _load(self) -> None:
        """Load manifests from disk."""
        try:
            path = Path(self.manifests_dir)
            if path.exists():
                for manifest_file in path.glob("*.json"):
                    with open(manifest_file) as f:
                        data = json.load(f)
                        self.manifests[data.get("id", manifest_file.stem)] = data
        except Exception:
            self.manifests = {}

    def get_manifest(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get agent capability manifest."""
        return self.manifests.get(agent_id)

    def validate_capabilities(self, agent_id: str, required: List[str]) -> Dict[str, Any]:
        """Validate agent capabilities against requirements."""
        manifest = self.get_manifest(agent_id)
        if not manifest:
            return {"valid": False, "missing": required}
        
        available = set(manifest.get("capabilities", []))
        missing = [cap for cap in required if cap not in available]
        
        return {
            "valid": len(missing) == 0,
            "available": sorted(available),
            "missing": missing,
            "required": required,
        }

    def register_manifest(self, agent_id: str, capabilities: List[str], 
                         version: str, protocol: str) -> Dict[str, Any]:
        """Register a new capability manifest."""
        manifest = {
            "id": agent_id,
            "capabilities": capabilities,
            "version": version,
            "protocol": protocol,
            "registered_at": time.time(),
        }
        self.manifests[agent_id] = manifest
        return manifest
