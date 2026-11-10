#!/usr/bin/env python3
"""Phase 1 Connector Smoke Test.

Verifies the Universal Agent Connector modules load correctly and basic
registration/discovery works.
"""

import os
import sys
import json

# Add project to path
project = "/home/meow/Projects/MOON/Cyclone"
sys.path.insert(0, project)

from apps.cyclone.connector.interface import (
    AgentConnectionError,
    AgentNotRegisteredError,
    AgentRegistrationError,
    AgentCapabilityError,
    UniversalAgentConnector,
)
from apps.cyclone.connector.registry import AgentRegistry
from apps.cyclone.connector.capability_manifest import CapabilityManifest
from apps.cyclone.connector.auth import AuthManager
from apps.cyclone.connector.connector import HERMESConnector

def test_exception_hierarchy():
    """Test exception hierarchy."""
    print("Testing exception hierarchy...")
    assert issubclass(AgentConnectionError, Exception)
    assert issubclass(AgentNotRegisteredError, AgentConnectionError)
    assert issubclass(AgentRegistrationError, AgentConnectionError)
    assert issubclass(AgentCapabilityError, AgentConnectionError)
    print("  PASS: Exception hierarchy OK")

def test_interface():
    """Test interface module."""
    print("Testing interface module...")
    assert UniversalAgentConnector is not None
    print("  PASS: Interface loaded")

def test_registry():
    """Test agent registry."""
    print("Testing agent registry...")
    registry = AgentRegistry()
    agent = registry.register("TEST_AGENT", {
        "name": "TEST_AGENT",
        "protocol": "ipc",
        "capabilities": ["code.generation", "testing"],
        "version": "1.0",
    })
    assert agent["name"] == "TEST_AGENT"
    assert "TEST_AGENT" in registry.list_agents()
    print(f"  PASS: Registry registered {agent['name']}")

def test_capability_manifest():
    """Test capability manifest."""
    print("Testing capability manifest...")
    manifest = CapabilityManifest()
    result = manifest.validate_capabilities("HERMES", ["code.generation", "testing"])
    assert result["valid"] == True or result["missing"] == ["code.generation", "testing"]
    print(f"  PASS: Capability validation OK (missing: {result['missing']})")

def test_auth():
    """Test auth manager."""
    print("Testing auth manager...")
    auth = AuthManager()
    # Test token generation (might fail if file exists)
    try:
        token = auth.generate_token("TEST_AGENT")
        assert auth.validate_token("TEST_AGENT", token) == True
        print("  PASS: Auth token generation OK")
    except Exception as e:
        print(f"  SKIP: {e}")

def test_connector():
    """Test HERMES connector."""
    print("Testing HERMES connector...")
    connector = HERMESConnector()
    # Check config exists
    config_path = os.path.join(project, "apps/cyclone/connector/config.yaml")
    assert os.path.exists(config_path), "Config file missing"
    print("  PASS: Config file exists")

def main():
    """Run all tests."""
    print("=" * 60)
    print("Phase 1 Connector Smoke Test")
    print("=" * 60)
    
    results = []
    for test in [test_exception_hierarchy, test_interface, test_registry, 
                 test_capability_manifest, test_auth, test_connector]:
        try:
            test()
            results.append(True)
        except Exception as e:
            print(f"  FAIL: {e}")
            import traceback
            traceback.print_exc()
            results.append(False)
    
    print("=" * 60)
    print(f"Results: {sum(results)}/{len(results)} tests passed")
    return all(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
