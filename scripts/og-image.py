"""Social share preview (Open Graph) image: the top of the home page, 1200x630, written to site/public/og.png.

The hero as it is on the page (title, subtitle with "AI chatbot", the pile of worry scraps), without the menu, the
search box and everything below. Captured at 2x and scaled down, so the pencil lines stay crisp. Reads the tailnet
build, so run scripts/deploy.sh first when the home page changed.

  uv run --with playwright --with pillow python -I scripts/og-image.py [URL]
"""
import asyncio
import io
import sys
from pathlib import Path

from PIL import Image
from playwright.async_api import async_playwright

URL = sys.argv[1] if len(sys.argv) > 1 else "https://procsetoucim.internal.quxt.eu/"
OUT = Path(__file__).resolve().parent.parent / "site/public/og.png"
W, H = 1200, 630
CSS = """
.top, .hero-search, .hero ~ *, footer { display: none !important; }
main { padding-top: 0 !important; }
.hero { padding-top: 58px !important; margin-top: 0 !important; }
"""


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path="/usr/bin/chromium", args=["--no-sandbox"])
        # Reduced motion keeps the subtitle on "AI chatbot" instead of the changing tool word.
        ctx = await browser.new_context(viewport={"width": W, "height": H}, device_scale_factor=2, reduced_motion="reduce")
        page = await ctx.new_page()
        await page.goto(URL, wait_until="networkidle")
        await page.add_style_tag(content=CSS)
        await page.evaluate("document.fonts.ready")
        await page.wait_for_timeout(500)
        png = await page.screenshot()
        await browser.close()
    Image.open(io.BytesIO(png)).convert("RGB").resize((W, H), Image.LANCZOS).save(OUT, optimize=True)
    print(f"{OUT} ({OUT.stat().st_size // 1024} kB)")


asyncio.run(main())
