#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.13/bin/python3
"""외부 소스 스크린샷 캡처 + 어노테이션 스크립트"""
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont
import os

ASSETS_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_PATH = "/System/Library/Fonts/AppleSDGothicNeo.ttc"

SOURCES = [
    {
        "name": "hn-mcp-is-a-fad",
        "url": "https://news.ycombinator.com/item?id=46552254",
        "selector": ".athing .titleline",
        "annotation": "← 'MCP는 유행일 뿐' 토론",
        "title_ko": "Hacker News: MCP is a fad",
    },
    {
        "name": "cli-beating-mcp",
        "url": "https://jannikreinhard.com/2026/02/22/why-cli-tools-are-beating-mcp-for-ai-agents/",
        "selector": "h1",
        "annotation": "← CLI가 MCP를 이기는 이유",
        "title_ko": "Why CLI Tools Are Beating MCP",
    },
    {
        "name": "mcp-wrong-fight",
        "url": "https://medium.com/@tobias_pfuetze/the-mcp-vs-cli-debate-is-the-wrong-fight-a87f1b4c8006",
        "selector": "h1",
        "annotation": "← '이 논쟁 자체가 잘못됐다'",
        "title_ko": "The MCP vs CLI Debate Is the Wrong Fight",
    },
]


def capture_and_annotate(source):
    name = source["name"]
    raw_path = os.path.join(ASSETS_DIR, f"{name}-raw.png")
    out_path = os.path.join(ASSETS_DIR, f"{name}.png")

    print(f"[{name}] Capturing {source['url']}...")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 800})
        try:
            page.goto(source["url"], wait_until="domcontentloaded", timeout=15000)
            page.wait_for_timeout(3000)  # extra wait for rendering
        except Exception as e:
            print(f"[{name}] Navigation warning: {e}")

        # Get bounding box of target element
        box = None
        try:
            el = page.query_selector(source["selector"])
            if el:
                box = el.bounding_box()
        except Exception:
            pass

        page.screenshot(path=raw_path)
        browser.close()

    print(f"[{name}] Raw screenshot saved: {raw_path}")

    # Annotate with Pillow
    img = Image.open(raw_path)
    draw = ImageDraw.Draw(img, "RGBA")

    try:
        font = ImageFont.truetype(FONT_PATH, 20, index=0)
        font_small = ImageFont.truetype(FONT_PATH, 16, index=0)
    except Exception:
        font = ImageFont.load_default()
        font_small = font

    if box:
        x1 = int(box["x"]) - 6
        y1 = int(box["y"]) - 6
        x2 = int(box["x"] + box["width"]) + 6
        y2 = int(box["y"] + box["height"]) + 6

        # Semi-transparent red fill
        draw.rectangle((x1, y1, x2, y2), fill=(220, 30, 30, 40))
        # Red border
        draw.rectangle((x1, y1, x2, y2), outline="#DC1E1E", width=3)

        # Annotation text with background
        text = source["annotation"]
        text_x = min(x2 + 12, img.width - 300)
        text_y = y1 + 2

        # Text background
        bbox = font.getbbox(text)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        draw.rectangle(
            (text_x - 4, text_y - 2, text_x + tw + 8, text_y + th + 6),
            fill=(30, 30, 30, 200),
        )
        draw.text((text_x, text_y), text, fill="#FF6666", font=font)

    # Remove raw file
    os.remove(raw_path)

    img.save(out_path, quality=90)
    print(f"[{name}] Annotated screenshot saved: {out_path}")
    return out_path


if __name__ == "__main__":
    for src in SOURCES:
        try:
            capture_and_annotate(src)
        except Exception as e:
            print(f"[{src['name']}] FAILED: {e}")

    print("\nDone! Captured files:")
    for f in os.listdir(ASSETS_DIR):
        if f.endswith(".png") and not f.endswith("-raw.png"):
            print(f"  {f}")
