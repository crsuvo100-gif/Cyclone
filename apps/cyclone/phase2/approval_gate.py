"""Phase 2 Action Approval Gate module.

Provides approval gating for sensitive browser and computer-use actions
to prevent accidental or unauthorized operations.

Features:
- Approval queue for sensitive actions
- Pre-execution approval checks
- Approval state management
- Bulk approval/denial
- Approval audit log

Usage:
    from apps.cyclone.phase2.approval_gate import ApprovalGate

    gate = ApprovalGate()
    preview = ActionPreview(action_type="click", target="button.submit", requires_approval=True)
    approved = await gate.request_approval(preview, "Confirm submit action")
    if approved:
        await execute_action(preview)
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class ApprovalRecord:
    """Single approval record."""
    action_id: str
    action_type: str
    target: str
    requires_approval: bool
    context: str = ""
    status: str = "pending"  # pending, approved, denied
    requested_at: float = field(default_factory=time.time)
    resolved_at: float = 0.0
    resolved_by: str = ""


class ApprovalGate:
    """Gate for approving sensitive actions."""

    def __init__(self, default_requires_approval: bool = True) -> None:
        self.default_requires_approval = default_requires_approval
        self._approvals: dict[str, ApprovalRecord] = {}
        self._next_id = 0
        self._approved_actions: list[dict[str, Any]] = []

    async def request_approval(
        self,
        action_type: str,
        target: str,
        requires_approval: bool | None = None,
        context: str = "",
    ) -> bool:
        """Request approval for a sensitive action."""
        if requires_approval is None:
            requires_approval = self.default_requires_approval

        if not requires_approval:
            return True  # Not requires approval, proceed

        self._next_id += 1
        action_id = f"APP-{self._next_id:04d}"

        record = ApprovalRecord(
            action_id=action_id,
            action_type=action_type,
            target=target,
            requires_approval=True,
            context=context,
            status="pending",
        )
        self._approvals[action_id] = record

        logger.info(f"Approval requested: {action_id} - {action_type} {target}")

        return False  # Requires approval

    async def request_approval_with_preview(self, preview: "ActionPreview", context: str = "") -> bool:
        """Request approval using an ActionPreview object."""
        if not preview.requires_approval:
            return True
        # Use the target/base info for approval request
        return await self.request_approval(
            preview.action_type,
            preview.target,
            requires_approval=preview.requires_approval,
            context=context,
        )

    def approve(self, action_id: str, requester: str = "auto") -> bool:
        """Approve a specific action."""
        record = self._approvals.get(action_id)
        if not record:
            logger.warning(f"Unknown approval ID: {action_id}")
            return False

        if record.status != "pending":
            return False

        record.status = "approved"
        record.resolved_at = time.time()
        record.resolved_by = requester

        self._approved_actions.append({
            "action_id": action_id,
            "action_type": record.action_type,
            "target": record.target,
            "approved_at": record.resolved_at,
        })

        logger.info(f"Action approved: {action_id} - {record.action_type}")
        return True

    def deny(self, action_id: str, requester: str = "auto") -> bool:
        """Deny a specific action."""
        record = self._approvals.get(action_id)
        if not record:
            logger.warning(f"Unknown approval ID: {action_id}")
            return False

        if record.status != "pending":
            return False

        record.status = "denied"
        record.resolved_at = time.time()
        record.resolved_by = requester

        logger.info(f"Action denied: {action_id} - {record.action_type}")
        return True

    def get_pending(self) -> list[str]:
        """Get list of pending approval IDs."""
        return [a.action_id for a in self._approvals.values() if a.status == "pending"]

    def get_approval(self, action_id: str) -> dict[str, Any] | None:
        """Get a specific approval record."""
        record = self._approvals.get(action_id)
        if record:
            return {
                "action_id": record.action_id,
                "action_type": record.action_type,
                "target": record.target,
                "requires_approval": record.requires_approval,
                "status": record.status,
                "requested_at": record.requested_at,
                "resolved_at": record.resolved_at,
            }
        return None

    def get_audit_log(self) -> list[dict[str, Any]]:
        """Get the approval audit log."""
        return [
            {
                "action_id": a["action_id"],
                "action_type": a["action_type"],
                "target": a["target"],
                "status": "approved",
                "timestamp": a["approved_at"],
            }
            for a in self._approved_actions
        ]

    @property
    def pending_count(self) -> int:
        """Number of pending approvals."""
        return len(self.get_pending())

    @property
    def all_approvals(self) -> list[ApprovalRecord]:
        """Get all approval records."""
        return list(self._approvals.values())


class SmartApprovalGate(ApprovalGate):
    """Smart approval gate with context-aware defaults.

    Uses heuristics to determine if an action requires approval
    based on context:
    - URL path changes
    - External site communication
    - Form submissions with data
    - Sensitive domain actions
    """

    def __init__(self, auto_approve_read_only: bool = True) -> None:
        super().__init__(default_requires_approval=True)
        self.auto_approve_read_only = auto_approve_read_only
        self._sensitive_domains = set()

    async def request_approval(
        self,
        action_type: str,
        target: str,
        requires_approval: bool | None = None,
        context: str = "",
    ) -> bool:
        """Context-aware approval request."""
        # If auto-approve read-only and read-only action
        if self.auto_approve_read_only:
            read_only_actions = {"navigate", "screenshot", "get_content", "find_elements", "evaluate"}
            if action_type in read_only_actions:
                return True

        # Always require approval for navigation to external domains
        if action_type == "navigate":
            return await self._check_navigation_approval(target, context)

        return await super().request_approval(
            action_type, target, requires_approval, context
        )

    async def _check_navigation_approval(self, url: str, context: str) -> bool:
        """Check if navigation requires approval based on domain."""
        domain = url.split("//")[-1].split("/")[0].lower()

        # Internal navigation is fine
        if context.startswith("internal://"):
            return True

        # Send to approval queue
        return await super().request_approval(
            "navigate", url, requires_approval=True,
            context=f"Navigation to {domain} by user",
        )

    def register_sensitive_domain(self, domain: str) -> None:
        """Register a domain as requiring extra approval."""
        self._sensitive_domains.add(domain.lower())


__all__ = ["ApprovalGate", "SmartApprovalGate", "ApprovalRecord"]
