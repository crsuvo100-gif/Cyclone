# Universal Agent Connector Architecture

## Overview
The Universal Agent Connector enables MOON to communicate with external AI agents through a pluggable adapter system.

## Architecture Diagram
```
MOON-AI (Main) ←→ UniversalAgentConnector ←→ Adapters
                              ↳ RESTAdapter
                              ↳ WebSocketAdapter
                              ↳ IPCAdapter
                              ↳ HERMESConnector
```

## Key Components

### 1. UniversalAgentConnector
Abstract base class defining the connector interface.

### 2. Adapter System
- **RESTAdapter**: HTTP REST API communication
- **WebSocketAdapter**: Bidirectional WebSocket communication
- **IPCAdapter**: Local process communication

### 3. Registry
- **AgentRegistry**: Manages agent registration and discovery
- **CapabilityManifest**: Validates agent capabilities
- **AuthManager**: Token-based authentication

### 4. Task System
- **TaskDelegation**: Structured task delegation
- **TaskTracking**: Task status monitoring

### 5. Lifecycle
- **AgentLifecycle**: Create, start, stop, delete agents

## Data Flow
1. Agent registers → Registry saves
2. Capability manifest validates → Compatibility check
3. Auth token issued → Secure communication
4. Task delegated → Task tracked
5. Health checked → Status reported

## Security
- Token-based authentication
- Permission scopes
- Approval required for sensitive actions
- No secrets in configuration files
