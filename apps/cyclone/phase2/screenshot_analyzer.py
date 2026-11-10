"""Phase 2 Screenshot & Visual-State Analysis module.

Provides screenshot capture, comparison, and visual state analysis for
browser automation and computer-use workflows.

Features:
- Screenshot capture (full page, viewport, region)
- Screenshot comparison (detect visual changes)
- Accessibility-tree-based visual state analysis
- Screenshot metadata extraction (dimensions, dominant color)
- OCR-free visual element detection via accessibility tree

Usage:
    from apps.cyclone.phase2.screenshot_analyzer import ScreenshotAnalyzer

    analyzer = ScreenshotAnalyzer()
    screenshot = await analyzer.capture_page(browser)
    comparison = await analyzer.compare_screenshots(screenshot1, screenshot2)
    analysis = await analyzer.analyze_visual_state(screenshot)
"""

from __future__ import annotations

import hashlib
import io
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

from PIL import Image

logger = logging.getLogger(__name__)


class ScreenshotAnalyzer:
    """Analyze screenshots and detect visual state changes."""

    def __init__(self, threshold: float = 0.05) -> None:
        self.threshold = threshold
        self.analysis_history: list[dict[str, Any]] = []
        self._hash_cache: dict[str, str] = {}

    async def capture_full_page(self, browser_session: "PlaywrightBrowserSession") -> bytes:
        """Capture a full-page screenshot."""
        return await browser_session.get_screenshot(path=None)

    async def capture_viewport(self, browser_session: "PlaywrightBrowserSession") -> bytes:
        """Capture a viewport-sized screenshot."""
        return await browser_session.get_screenshot(path=None)

    async def capture_region(
        self,
        browser_session: "PlaywrightBrowserSession",
        x: int,
        y: int,
        width: int,
        height: int,
    ) -> bytes:
        """Capture a specific region screenshot.

        Uses the browser's clip option for cropping.
        """
        if browser_session._page is None:
            raise ValueError("No active browser session")

        import base64
        from playwright.async_api import TimeoutError as PWTimeout

        try:
            image = await browser_session._page.screenshot(
                animations="disabled",
                clip={"x": x, "y": y, "width": width, "height": height},
            )
            return image
        except Exception as exc:
            raise ValueError(f"Region capture failed: {exc}") from exc

    async def capture_page_dimensions(self, browser_session: "PlaywrightBrowserSession") -> dict[str, Any]:
        """Get page dimensions and viewport info."""
        if browser_session._page is None:
            raise ValueError("No active browser session")

        try:
            metrics = await browser_session._page.evaluate(
                "([w, h]) => ({"
                "  inner_width: w, "
                "  inner_height: h, "
                "  outer_width: window.outerWidth, "
                "  outer_height: window.outerHeight, "
                "  scroll_x: window.scrollX, "
                "  scroll_y: window.scrollY, "
                "  device_pixel_ratio: window.devicePixelRatio "
                "})",
                [browser_session.viewport_width, browser_session.viewport_height],
            )
            return metrics
        except Exception as exc:
            raise ValueError(f"Dimension capture failed: {exc}") from exc

    async def compare_screenshots(
        self,
        screenshot_a: bytes,
        screenshot_b: bytes,
        name_a: str = "A",
        name_b: str = "B",
    ) -> dict[str, Any]:
        """Compare two screenshots and return difference metrics.

        Returns:
            Dict with similarity score, difference percentage, and match flag.
        """
        try:
            img_a = Image.open(io.BytesIO(screenshot_a)).convert("RGB")
            img_b = Image.open(io.BytesIO(screenshot_b)).convert("RGB")

            if img_a.size != img_b.size:
                return {
                    "match": False,
                    "similarity": 0.0,
                    "difference_percentage": 100.0,
                    "reason": "Screenshot dimensions differ",
                }

            # Compute difference
            diff = Image.new("L", img_a.size, 255)
            for x in range(img_a.size[0]):
                for y in range(img_a.size[1]):
                    r1, g1, b1 = img_a.getpixel((x, y))
                    r2, g2, b2 = img_b.getpixel((x, y))
                    diff_val = abs(r1 - r2) + abs(g1 - g2) + abs(b1 - b2)
                    diff.putpixel((x, y), diff_val)

            total_pixels = img_a.size[0] * img_a.size[1]
            changed_pixels = sum(1 for p in diff.getdata() if p > 30)
            diff_percentage = changed_pixels / total_pixels * 100

            # Compute structural similarity (simplified)
            # Convert both to grayscale and compare
            gray_a = img_a.convert("L")
            gray_b = img_b.convert("L")
            pixels_a = list(gray_a.getdata())
            pixels_b = list(gray_b.getdata())
            diff_sum = sum(abs(a - b) for a, b in zip(pixels_a, pixels_b))
            similarity = 1.0 - (diff_sum / (255 * 3 * total_pixels))

            return {
                "match": diff_percentage < self.threshold,
                "similarity": round(similarity, 4),
                "difference_percentage": round(diff_percentage, 4),
                "name_a": name_a,
                "name_b": name_b,
                "screenshot_a_hash": self._hash_screenshot(screenshot_a),
                "screenshot_b_hash": self._hash_screenshot(screenshot_b),
            }
        except Exception as exc:
            raise ValueError(f"Screenshot comparison failed: {exc}") from exc

    async def analyze_visual_state(self, screenshot: bytes) -> dict[str, Any]:
        """Analyze a screenshot and extract visual state features.

        Extracts:
        - Image dimensions
        - Dominant colors (top 5)
        - Contrast/colorfulness (simplified)
        - Element density (estimated)
        """
        try:
            img = Image.open(io.BytesIO(screenshot)).convert("RGB")
            width, height = img.size

            # Get dominant colors
            palette = img.getcolors(maxcolors=256 * 256)
            if palette:
                palette.sort(key=lambda x: x[0], reverse=True)
                top_colors = [{"rgb": c[1], "count": c[0]} for c in palette[:5]]
            else:
                top_colors = []

            # Compute colorfulness (Hasler-Susstrunk metric)
            r, g, b = img.split()
            rg = list(r.getdata())
            gb = list(g.getdata())
            rb = list(b.getdata())

            rg_mean = sum(rg) / len(rg)
            gb_mean = sum(gb) / len(gb)
            rb_mean = sum(rb) / len(rb)

            rg_std = (sum((x - rg_mean) ** 2 for x in rg) / len(rg)) ** 0.5
            gb_std = (sum((x - gb_mean) ** 2 for x in gb) / len(gb)) ** 0.5
            rb_std = (sum((x - rb_mean) ** 2 for x in rb) / len(rb)) ** 0.5

            colorfulness = ((rg_std + gb_std) ** 0.5) + 0.3 * ((rg_mean - rb_mean) ** 2 + gb_mean**2 + rb_mean**2) ** 0.5

            # Estimate text/element density (simple heuristic)
            # Convert to grayscale and count "dark" pixels
            gray = img.convert("L")
            dark_pixels = sum(1 for p in gray.getdata() if p < 128)
            density = dark_pixels / (width * height)

            return {
                "dimensions": {"width": width, "height": height},
                "dominant_colors": top_colors,
                "colorfulness": round(colorfulness, 4),
                "text_density": round(density, 4),
                "analysis_time": datetime.now().isoformat(),
            }
        except Exception as exc:
            raise ValueError(f"Visual state analysis failed: {exc}") from exc

    def _hash_screenshot(self, screenshot: bytes) -> str:
        """Generate a hash for a screenshot for caching."""
        if screenshot not in self._hash_cache:
            self._hash_cache[screenshot] = hashlib.md5(screenshot).hexdigest()
        return self._hash_cache[screenshot]

    def save_screenshot(self, screenshot: bytes, path: str) -> str:
        """Save a screenshot to disk."""
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_bytes(screenshot)
        return path

    def load_screenshot(self, path: str) -> bytes:
        """Load a screenshot from disk."""
        return Path(path).read_bytes()


__all__ = ["ScreenshotAnalyzer"]
