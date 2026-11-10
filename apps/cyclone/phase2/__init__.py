"""Phase 2: Browser + Computer Use + Advanced Research.

This module provides Phase 2 of the HERMES V13.0 universal agent protocol:
- Browser automation (navigation, inspection, interaction)
- Screenshot and visual-state analysis
- Multi-source research with citation tracking
- Action approval gates for sensitive operations
- Error handling and recovery

Usage:
    from apps.cyclone.phase2 import (
        PlaywrightBrowserSession,
        ScreenshotAnalyzer,
        ResearchWorkflow,
        ApprovalGate,
        Phase2Error,
    )
"""

from .interface import (
    Phase2Error,
    BrowserNavigationError,
    PageLoadError,
    InteractionError,
    ComputerUseError,
    ApprovalRequiredError,
    ResearchError,
    SourceVerificationError,
    CitationError,
)

from .browser import PlaywrightBrowserSession

from .screenshot_analyzer import ScreenshotAnalyzer

from .research_workflow import (
    ResearchWorkflow,
    Source,
    Citation,
    ResearchFinding,
)

from .approval_gate import (
    ApprovalGate,
    SmartApprovalGate,
    ApprovalRecord,
)

__version__ = "1.0.0"
__all__ = [
    "Phase2Error",
    "BrowserNavigationError",
    "PageLoadError",
    "InteractionError",
    "ComputerUseError",
    "ApprovalRequiredError",
    "ResearchError",
    "SourceVerificationError",
    "CitationError",
    "PlaywrightBrowserSession",
    "ScreenshotAnalyzer",
    "ResearchWorkflow",
    "Source",
    "Citation",
    "ResearchFinding",
    "ApprovalGate",
    "SmartApprovalGate",
    "ApprovalRecord",
]
