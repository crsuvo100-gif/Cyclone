"""Phase 2: Browser + Computer Use + Advanced Research interface.

Defines the contracts for:
- Browser automation (navigation, inspection, interaction)
- Screenshot and visual-state analysis
- Document retrieval and download management
- Action approval gates and recovery
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class Phase2Error(Exception):
    """Base exception for Phase 2 errors."""


class BrowserNavigationError(Phase2Error):
    """Raised when browser navigation fails."""


class PageLoadError(Phase2Error):
    """Raised when page load fails or times out."""


class InteractionError(Phase2Error):
    """Raised when interaction with page elements fails."""


class ComputerUseError(Phase2Error):
    """Raised when computer-use operation fails."""


class ApprovalRequiredError(Phase2Error):
    """Raised when a sensitive action requires user approval."""


class ResearchError(Phase2Error):
    """Raised when research workflow fails."""


class SourceVerificationError(Phase2Error):
    """Raised when source verification fails."""


class CitationError(Phase2Error):
    """Raised when citation tracking fails."""


class ActionPreview(ABC):
    """Abstract preview of an action before execution."""

    @property
    @abstractmethod
    def action_type(self) -> str:
        """Type of action (navigate, click, fill, screenshot, download)."""
        ...

    @property
    @abstractmethod
    def target(self) -> str:
        """Target description of the action."""
        ...

    @property
    @abstractmethod
    def requires_approval(self) -> bool:
        """Whether this action requires user approval."""
        ...

    @abstractmethod
    def to_dict(self) -> dict[str, Any]:
        """Serialize the action preview."""
        ...

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict[str, Any]) -> "ActionPreview":
        """Deserialize from dict."""
        ...


class BrowserSession(ABC):
    """Abstract browser session for navigation and inspection."""

    @abstractmethod
    async def navigate(self, url: str, timeout: float = 30.0) -> dict[str, Any]:
        """Navigate to a URL and return page metadata."""
        ...

    @abstractmethod
    async def get_content(self, selector: str = "body") -> str:
        """Extract text content from a CSS selector."""
        ...

    @abstractmethod
    async def get_screenshot(self, path: str | None = None) -> bytes:
        """Capture a screenshot of the current page."""
        ...

    @abstractmethod
    async def find_elements(self, selector: str) -> list[dict[str, Any]]:
        """Find elements matching a CSS selector."""
        ...

    @abstractmethod
    async def click_element(self, selector: str, index: int = 0) -> bool:
        """Click a matching element."""
        ...

    @abstractmethod
    async def fill_element(self, selector: str, text: str, index: int = 0) -> bool:
        """Fill a text input with the given text."""
        ...

    @abstractmethod
    async def evaluate(self, script: str) -> Any:
        """Execute JS in the page context and return result."""
        ...

    @abstractmethod
    async def close(self) -> None:
        """Close the browser session."""
        ...

    @property
    @abstractmethod
    def current_url(self) -> str:
        """Current page URL."""
        ...

    @property
    @abstractmethod
    def page_title(self) -> str:
        """Current page title."""
        ...


class ComputerSession(ABC):
    """Abstract computer-use session for window/screen operations."""

    @abstractmethod
    async def capture_screen(self, region: tuple[int, int, int, int] | None = None) -> bytes:
        """Capture the screen or a region as an image."""
        ...

    @abstractmethod
    async def find_on_screen(self, image_path: str) -> tuple[int, int] | None:
        """Find an image on screen and return its center coordinates."""
        ...

    @abstractmethod
    async def click(self, x: int, y: int, button: str = "left") -> bool:
        """Click at screen coordinates."""
        ...

    @abstractmethod
    async def type_text(self, text: str) -> bool:
        """Type text at the current cursor position."""
        ...

    @abstractmethod
    async def close(self) -> None:
        """Close the computer session."""
        ...


class ResearchWorkflow(ABC):
    """Abstract multi-source research workflow."""

    @abstractmethod
    async def search(self, query: str, max_results: int = 5) -> list[dict[str, Any]]:
        """Search for a query and return sources."""
        ...

    @abstractmethod
    async def fetch_source(self, url: str, depth: int = 0) -> dict[str, Any]:
        """Fetch and extract a source page."""
        ...

    @abstractmethod
    async def verify_source(self, url: str, snippet: str) -> dict[str, Any]:
        """Verify source credibility and extract citation info."""
        ...

    @abstractmethod
    async def generate_report(
        self,
        query: str,
        sources: list[dict[str, Any]],
        findings: list[dict[str, Any]],
    ) -> str:
        """Generate a research report from findings."""
        ...

    @property
    @abstractmethod
    def citation_tracker(self) -> "CitationTracker":
        """Get the citation tracker for this workflow."""
        ...


class CitationTracker(ABC):
    """Abstract citation tracking for research sources."""

    @abstractmethod
    def add_citation(self, url: str, title: str, snippet: str, source_type: str) -> str:
        """Add a citation and return a unique citation ID."""
        ...

    @abstractmethod
    def verify_citation(self, url: str) -> bool:
        """Verify a citation is still accessible and unchanged."""
        ...

    @abstractmethod
    def get_citations(self) -> list[dict[str, Any]]:
        """Get all tracked citations."""
        ...

    @property
    @abstractmethod
    def citation_count(self) -> int:
        """Number of tracked citations."""
        ...


class ApprovalGate(ABC):
    """Abstract approval gate for sensitive actions."""

    @abstractmethod
    async def request_approval(
        self,
        action: ActionPreview,
        context: str = "",
    ) -> bool:
        """Request approval for a sensitive action."""
        ...

    @property
    @abstractmethod
    def approval_state(self) -> dict[str, Any]:
        """Current approval state."""
        ...

    @abstractmethod
    def approve(self, action_id: str) -> None:
        """Approve a specific action."""
        ...

    @abstractmethod
    def deny(self, action_id: str) -> None:
        """Deny a specific action."""
        ...

    @property
    @abstractmethod
    def pending_approvals(self) -> list[str]:
        "List of pending approval IDs."
        ...
