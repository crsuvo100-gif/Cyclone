"""Universal Agent Connector + HERMES Integration."""

from .interface import (
    AgentConnectionError,
    AgentNotRegisteredError,
    AgentRegistrationError,
    AgentCapabilityError,
    AgentHealthError,
    AgentAdapter,
    UniversalAgentConnector,
)

__all__ = [
    "AgentConnectionError",
    "AgentNotRegisteredError",
    "AgentRegistrationError",
    "AgentCapabilityError",
    "AgentHealthError",
    "AgentAdapter",
    "UniversalAgentConnector",
]
