"""Capture social-preview screenshots from the locally-served /og route.

Outputs (written to public/ for direct deploy):
  og-image.png       1200 x 630   Open Graph default (Facebook, LinkedIn unfurls, Slack)
  twitter-card.png   1200 x 675   Twitter summary_large_image, 16:9
  social-square.png  1080 x 1080  Instagram / LinkedIn square

Usage:
  1) npm run build
  2) npm run preview -- --port 4321 --host 127.0.0.1  (in another terminal)
  3) python3 scripts/screenshot_og.py

Optional environment overrides:
  PLAYSHIP_OG_URL       default http://127.0.0.1:4321/og/
  PLAYSHIP_OG_OUTDIR    default <repo>/public
  PLAYWRIGHT_CHROMIUM   path to chromium; falls back to bundled Playwright chromium
"""
from __future__ import annotations

import asyncio
import os
from pathlib import Path
from playwright.async_api import async_playwright

REPO_ROOT = Path(__file__).resolve().parents[1]
OG_URL = os.environ.get("PLAYSHIP_OG_URL", "http://127.0.0.1:4321/og/")
OUT_DIR = Path(os.environ.get("PLAYSHIP_OG_OUTDIR", REPO_ROOT / "public"))
CHROME = os.environ.get("PLAYWRIGHT_CHROMIUM")  # None => use bundled chromium

TARGETS = [
    # (filename, width, height)
    ("og-image.png", 1200, 630),
    ("twitter-card.png", 1200, 675),
    ("social-square.png", 1080, 1080),
]


async def capture(p, filename: str, width: int, height: int) -> None:
    launch_kwargs = {"args": ["--no-sandbox", "--disable-dev-shm-usage"]}
    if CHROME:
        launch_kwargs["executable_path"] = CHROME
    browser = await p.chromium.launch(**launch_kwargs)
    try:
        context = await browser.new_context(
            viewport={"width": width, "height": height},
            # device_scale_factor=1 yields exact output dimensions. OG/Twitter
            # specs target 1200x630; oversized files get downscaled with heavy
            # compression by sharing services. Keeps us under 200KB.
            device_scale_factor=1,
        )
        page = await context.new_page()

        # Force the rendered .og-frame to the exact target viewport so the
        # layout reflows for non-default aspect ratios (e.g. the 1:1 square).
        await page.add_init_script(
            f"""
            (() => {{
              const apply = () => {{
                const el = document.getElementById('og-frame');
                if (!el) return;
                el.style.width = '{width}px';
                el.style.height = '{height}px';
              }};
              if (document.readyState !== 'loading') apply();
              else document.addEventListener('DOMContentLoaded', apply);
            }})();
            """
        )

        await page.goto(OG_URL, wait_until="networkidle")
        try:
            await page.evaluate("document.fonts && document.fonts.ready")
        except Exception:
            pass
        await page.wait_for_timeout(800)

        frame = await page.query_selector("#og-frame")
        if frame is None:
            raise RuntimeError("#og-frame element not found at " + OG_URL)
        box = await frame.bounding_box()
        if box is None:
            raise RuntimeError("#og-frame bounding box unavailable")

        out_path = OUT_DIR / filename
        await page.screenshot(
            path=str(out_path),
            clip={
                "x": box["x"],
                "y": box["y"],
                "width": box["width"],
                "height": box["height"],
            },
        )
        print(f"wrote {out_path} ({width}x{height})")
    finally:
        await browser.close()


async def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        for filename, w, h in TARGETS:
            await capture(p, filename, w, h)


if __name__ == "__main__":
    asyncio.run(main())
