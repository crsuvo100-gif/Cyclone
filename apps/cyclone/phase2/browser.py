"""Phase 2 Browser Automation Module.

Provides comprehensive browser automation using Playwright:
- Navigation and page inspection
- Screenshot capturing
- Element interaction (click, fill, type)
- Form automation
- Visual state analysis
- Session recovery and error handling

Reusable: existing playwright-based browser tool wrapped into a full
session-aware class.

Usage:
    from apps.cyclone.phase2.browser import PlaywrightBrowser

    async with PlaywrightBrowser() as browser:
        await browser.navigate("https://example.com")
        content = await browser.get_content()
        await browser.click_element("button.submit")
        await browser.fill_element("input#search", "MOON V13")
        await browser.navigate_screenshot("https://example.com", "page.png")
"""

from __future__ import annotations

import logging
import os
import time
from pathlib import Path
from typing import Any

from .interface import (
    ActionPreview,
    BrowserNavigationError,
    InteractionError,
    PageLoadError,
    BrowserSession,
)

logger = logging.getLogger(__name__)


class PlaywrightBrowserSession(BrowserSession):
    """Playwright-based browser session with full automation capabilities."""

    def __init__(
        self,
        headless: bool = True,
        viewport_width: int = 1280,
        viewport_height: int = 720,
        user_agent: str | None = None,
        timeout: float = 30.0,
    ) -> None:
        self.headless = headless
        self.viewport_width = viewport_width
        self.viewport_height = viewport_height
        self.user_agent = user_agent or "MOON-AI-Browser/2.0"
        self.timeout = timeout
        self._browser = None
        self._context = None
        self._page = None
        self._current_url = ""
        self._page_title = ""
        self._history: list[dict[str, Any]] = []
        self._created_at = time.time()

    async def navigate(self, url: str, timeout: float = 30.0) -> dict[str, Any]:
        """Navigate to a URL and return page metadata.

        Raises:
            BrowserNavigationError: On navigation failure.
        """
        if self._page is None:
            await self._start_session()

        try:
            await self._page.wait_for_load_state("domcontentloaded", timeout=timeout * 1000)
            self._current_url = self._page.url
            self._page_title = await self._page.title()

            response = self._page.wait_for_response(lambda r: True, timeout=timeout * 1000)
            response_data = {
                "url": self._current_url,
                "title": self._page_title,
                "status": response.status if response else None,
                "load_time": time.time(),
            }
            self._history.append(response_data)
            return response_data
        except Exception as exc:
            self._current_url = ""
            self._page_title = ""
            raise BrowserNavigationError(f"Navigation failed for {url}: {exc}") from exc

    async def get_content(self, selector: str = "body") -> str:
        """Extract text content from a CSS selector."""
        if self._page is None:
            raise BrowserNavigationError("No active browser session")
        try:
            return await self._page.inner_text(selector)
        except Exception as exc:
            raise InteractionError(f"Failed to extract content: {exc}") from exc

    async def get_screenshot(self, path: str | None = None) -> bytes:
        """Capture a screenshot of the current page."""
        if self._page is None:
            raise BrowserNavigationError("No active browser session")
        try:
            if path:
                os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
                await self._page.screenshot(path=path)
                return Path(path).stat().st_size
            else:
                return await self._page.screenshot()
        except Exception as exc:
            raise BrowserNavigationError(f"Screenshot failed: {exc}") from exc

    async def find_elements(self, selector: str) -> list[dict[str, Any]]:
        """Find elements matching a CSS selector."""
        if self._page is None:
            raise BrowserNavigationError("No active browser session")
        try:
            elements = await self._page.query_selector_all(selector)
            results = []
            for i, elem in enumerate(elements):
                rect = await elem.bounding_box()
                results.append({
                    "index": i,
                    "text": await elem.inner_text()[:200],
                    "bounding_box": rect or {},
                    "aria_label": await elem.get_attribute("aria-label") or "",
                    "tag": await elem.get_attribute("tagName") or "",
                })
            return results
        except Exception as exc:
            raise InteractionError(f"Element lookup failed: {exc}") from exc

    async def click_element(self, selector: str, index: int = 0) -> bool:
        """Click a matching element."""
        if self._page is None:
            raise BrowserNavigationError("No active browser session")
        try:
            elements = await self._page.query_selector_all(selector)
            if not elements or index >= len(elements):
                raise InteractionError(f"Selector '{selector}' not found (index {index})")
            await elements[index].click(timeout=self.timeout * 1000)
            return True
        except Exception as exc:
            raise InteractionError(f"Click failed: {exc}") from exc

    async def fill_element(self, selector: str, text: str, index: int = 0) -> bool:
        """Fill a text input with the given text."""
        if self._page is None:
            raise BrowserNavigationError("No active browser session")
        try:
            elements = await self._page.query_selector_all(selector)
            if not elements or index >= len(elements):
                raise InteractionError(f"Selector '{selector}' not found")
            await elements[index].fill(text)
            return True
        except Exception as exc:
            raise InteractionError(f"Fill failed: {exc}") from exc

    async def type_text(self, selector: str, text: str, index: int = 0, slow: bool = False) -> bool:
        """Type text into an input element with optional slow typing."""
        if self._page is None:
            raise BrowserNavigationError("No active browser session")
        try:
            elements = await self._page.query_selector_all(selector)
            if not elements or index >= len(elements):
                raise InteractionError(f"Selector '{selector}' not found")
            await elements[index].type(text, delay=50 if slow else 0)
            return True
        except Exception as exc:
            raise InteractionError(f"Type failed: {exc}") from exc

    async def evaluate(self, script: str) -> Any:
        """Execute JS in the page context and return result."""
        if self._page is None:
            raise BrowserNavigationError("No active browser session")
        try:
            return await self._page.evaluate(script)
        except Exception as exc:
            raise InteractionError(f"JS evaluation failed: {exc}") from exc

    async def scroll_to(self, selector: str, offset: float = 0.0) -> bool:
        """Scroll the page to the given element with optional offset."""
        if self._page is None:
            raise BrowserNavigationError("No active browser session")
        try:
            elements = await self._page.query_selector_all(selector)
            if not elements:
                return False
            await elements[0].scroll_into_view_if_needed()
            if offset:
                await self._page.evaluate(f"window.scrollBy(0, {offset})")
            return True
        except Exception as exc:
            raise InteractionError(f"Scroll failed: {exc}") from exc

    @property
    def current_url(self) -> str:
        """Current page URL."""
        return self._current_url

    @property
    def page_title(self) -> str:
        """Current page title."""
        return self._page_title

    async def close(self) -> None:
        """Close the browser session."""
        if self._browser:
            await self._browser.close()
            self._browser = None
            self._context = None
            self._page = None

    async def _start_session(self) -> None:
        """Start the browser session."""
        from playwright.async_api import async_playwright

        async with async_playwright() as p:
            self._browser = await p.chromium.launch(headless=self.headless)

            # Configure context with custom user agent and viewport
            context = await self._browser.new_context(
                viewport={"width": self.viewport_width, "height": self.viewport_height},
                user_agent=self.user_agent,
                locale="en-US",
                timezone_id="UTC",
            )

            # Enable persistent context for cookies/storage persistence
            self._context = context
            self._page = await self._context.new_page()

    async def __aenter__(self) -> "PlaywrightBrowserSession":
        await self._start_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()


class ActionPreviewImplement(ActionPreview):
    """Concrete action preview implementation."""

    def __init__(
        self,
        action_type: str,
        target: str,
        requires_approval: bool = False,
        details: dict[str, Any] | None = None,
    ) -> None:
        self.action_type = action_type
        self.target = target
        self.requires_approval = requires_approval
        self.details = details or {}

    @property
    def action_type(self) -> str:
        return self._action_type

    @action_type.setter
    def action_type(self, value: str) -> None:
        self._action_type = value

    @property
    def target(self) -> str:
        return self._target

    @target.setter
    def target(self, value: str) -> None:
        self._target = value

    @property
    def requires_approval(self) -> bool:
        return self._requires_approval

    @requires_approval.setter
    def requires_approval(self, value: bool) -> None:
        self._requires_approval = value

    def to_dict(self) -> dict[str, Any]:
        return {
            "action_type": self._action_type,
            "target": self._target,
            "requires_approval": self._requires_approval,
            "details": self.details,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ActionPreviewImplement":
        return cls(
            action_type=data.get("action_type", ""),
            target=data.get("target", ""),
            requires_approval=data.get("requires_approval", False),
            details=data.get("details", {}),
        )


__all__ = [
    "PlaywrightBrowserSession",
    "ActionPreviewImplement",
    "BrowserNavigationError",
    "PageLoadError",
    "InteractionError",
]
