"""Playwright + Pillow: 외부 웹사이트 캡처 + 바운딩박스 어노테이션"""
import time, os
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont

OUT = "lectures/screenshot-test/results/playwright"
URL = "https://github.com/anthropics/claude-code"
VIEWPORT = {"width": 1280, "height": 800}

def capture_and_annotate():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport=VIEWPORT, color_scheme="dark")

        # --- 1) 순수 캡처 ---
        t0 = time.time()
        page.goto(URL, wait_until="domcontentloaded")
        page.wait_for_timeout(3000)

        # 팝업/배너 제거
        page.evaluate('''
            document.querySelectorAll(
                '[class*="cookie"], [class*="consent"], [class*="banner"]'
            ).forEach(el => el.style.display = "none")
        ''')

        page.screenshot(path=os.path.join(OUT, "github-raw.png"))
        t_raw = time.time() - t0
        print(f"[PW] Raw screenshot: {t_raw:.2f}s")

        # --- 2) 바운딩박스 어노테이션 ---
        t1 = time.time()
        targets = [
            {"selector": "article h1, [data-testid='hero-heading'], h1.heading-element", "label": "Repo Title"},
            {"selector": "[aria-label='Star this repository'], .starring-container", "label": "Star Button"},
            {"selector": "nav[aria-label='Repository'] ul, .UnderlineNav-body", "label": "Tab Nav"},
        ]

        boxes = []
        for t in targets:
            el = page.query_selector(t["selector"])
            if el and el.is_visible():
                box = el.bounding_box()
                if box:
                    boxes.append({"box": box, "label": t["label"]})
                    print(f"  Found: {t['label']} at ({box['x']:.0f},{box['y']:.0f}) {box['width']:.0f}x{box['height']:.0f}")
            else:
                print(f"  Not found: {t['label']}")

        page.screenshot(path=os.path.join(OUT, "github-for-annotate.png"))
        t_box = time.time() - t1

        browser.close()

    # Pillow 어노테이션
    img = Image.open(os.path.join(OUT, "github-for-annotate.png"))
    draw = ImageDraw.Draw(img, "RGBA")
    try:
        font = ImageFont.truetype("/System/Library/Fonts/AppleSDGothicNeo.ttc", 18)
    except:
        font = ImageFont.load_default()

    colors = [
        ("#FF3333", (255, 51, 51, 40)),
        ("#33CC33", (51, 204, 51, 40)),
        ("#3399FF", (51, 153, 255, 40)),
    ]

    for i, item in enumerate(boxes):
        b = item["box"]
        color_outline, color_fill = colors[i % len(colors)]
        coords = (
            int(b["x"]) - 4, int(b["y"]) - 4,
            int(b["x"] + b["width"]) + 4, int(b["y"] + b["height"]) + 4,
        )
        draw.rectangle(coords, fill=color_fill)
        draw.rectangle(coords, outline=color_outline, width=3)
        # 라벨 배경
        label = f" {item['label']} "
        bbox = draw.textbbox((0, 0), label, font=font)
        lw, lh = bbox[2] - bbox[0], bbox[3] - bbox[1]
        lx, ly = coords[0], coords[1] - lh - 6
        draw.rectangle((lx, ly, lx + lw + 8, ly + lh + 4), fill=color_outline)
        draw.text((lx + 4, ly + 1), label, fill="white", font=font)

    img.save(os.path.join(OUT, "github-annotated.png"))
    os.remove(os.path.join(OUT, "github-for-annotate.png"))
    t_total = t_raw + t_box
    print(f"[PW] Annotated screenshot: {t_box:.2f}s  (total: {t_total:.2f}s)")
    print(f"[PW] Files: github-raw.png, github-annotated.png")

if __name__ == "__main__":
    capture_and_annotate()
