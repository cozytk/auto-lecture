---
id: screenshot-annotation-pipeline
name: Screenshot Annotation Pipeline
description: Playwright DOM coordinates + Pillow drawing for reliable web page screenshot annotations. CSS injection is unreliable - always use the hybrid approach.
source: conversation
triggers:
  - "스크린샷"
  - "screenshot"
  - "하이라이트"
  - "어노테이션"
  - "annotation"
  - "빨간 박스"
  - "교안 이미지"
  - "웹페이지 캡처"
quality: high
---

# Screenshot Annotation Pipeline

## The Insight

웹페이지 스크린샷에 어노테이션(박스, 밑줄, 텍스트)을 추가하는 방법은 두 가지가 있다:

1. **CSS 주입 (불안정)**: playwright로 `element.style.cssText`에 outline/background를 주입. 사이트의 기존 CSS(`overflow:hidden`, `z-index`, specificity)에 의해 **조용히 실패**한다.
2. **하이브리드 (안정)**: playwright로 DOM 요소의 bounding box 좌표를 얻고, Pillow로 이미지 위에 직접 그린다. DOM과 무관하게 **항상 동작**한다.

**원칙: 스크린샷 어노테이션은 항상 하이브리드 방식을 사용한다.**

## Why This Matters

CSS 주입 방식을 쓰면:
- 셀렉터가 맞아도 스타일이 적용 안 될 수 있다 (사이트 CSS가 override)
- 디버깅이 어렵다 (에러 없이 조용히 실패)
- 사이트마다 다른 DOM 구조에 매번 셀렉터를 조정해야 한다

하이브리드 방식은 좌표만 정확하면 어떤 사이트든 동작한다.

## Recognition Pattern

- 교안에 웹페이지 스크린샷을 넣어야 할 때
- 스크린샷의 특정 영역을 강조해야 할 때
- UI 튜토리얼에서 "여기를 클릭하세요" 류의 가이드를 만들 때

## The Approach

### 파이프라인

```
playwright (스크린샷 + bounding box 좌표)
    ↓
Pillow (박스/채우기/밑줄/텍스트/화살표)
    ↓
auto-lecture-assets repo (git push)
    ↓
raw.githubusercontent.com URL
    ↓
Notion API (이미지 삽입)
```

### 핵심 의사결정

1. **좌표 획득은 playwright**, 그리기는 Pillow — 역할을 분리
2. **뷰포트 밖 요소는 자동 스킵** — `box['y'] + box['height'] > viewport_height`이면 경고 출력 후 스킵
3. **한글 폰트** — macOS에서 `/System/Library/Fonts/AppleSDGothicNeo.ttc` 사용 (Helvetica는 한글 깨짐)
4. **Python 경로** — pyenv 환경에서 Pillow/playwright가 설치된 Python 경로를 명시적으로 사용: `/Library/Frameworks/Python.framework/Versions/3.13/bin/python3`
5. **이미지 호스팅** — `auto-lecture-assets` 별도 repo에 push → `raw.githubusercontent.com` URL

### 팝업/배너/쿠키 대응 규칙

외부 웹페이지 캡처 시 팝업·쿠키 배너·로그인 프롬프트가 콘텐츠를 가리는 경우가 많다. **스크린샷 전에 반드시 제거**한다.

**3단계 제거 전략** (순서대로 시도):

```python
# Step 1: 클릭으로 닫기 (가장 자연스러운 방법)
close_selectors = [
    'button:has-text("Accept")', 'button:has-text("Reject")',
    'button:has-text("OK")', 'button:has-text("Got it")',
    'button:has-text("Close")', 'button:has-text("Okay")',
    '#onetrust-accept-btn-handler',  # OneTrust (많은 사이트)
    '.cky-btn-accept',               # CookieYes
    '[aria-label="Close"]',
]
for sel in close_selectors:
    try:
        btn = page.query_selector(sel)
        if btn and btn.is_visible():
            btn.click()
            page.wait_for_timeout(500)
    except: pass

# Step 2: CSS로 숨기기 (클릭 실패 시)
page.evaluate('''
    document.querySelectorAll([
        '.cookie-banner', '.cookie-consent', '.cookie-notice',
        '[class*="cookie"]', '[class*="consent"]', '[class*="gdpr"]',
        '[class*="popup"]', '[class*="modal"]', '[class*="overlay"]',
        '[class*="sign-in"]', '[class*="signin"]',
        '.crayons-notice',  // DEV.to
        '#onetrust-banner-sdk',  // OneTrust
    ].join(',')).forEach(el => el.style.display = 'none')
''')

# Step 3: 고정 위치 요소 제거 (하단 배너 등)
page.evaluate('''
    document.querySelectorAll('*').forEach(el => {
        const style = getComputedStyle(el);
        if ((style.position === 'fixed' || style.position === 'sticky') &&
            el.offsetHeight < 200 &&
            (el.offsetTop > window.innerHeight * 0.7 || el.offsetTop < 50)) {
            el.style.display = 'none';
        }
    })
''')
```

**SPA/지연 로딩 사이트 대응**:
- `wait_until='domcontentloaded'` 후 `page.wait_for_timeout(3000~5000)`
- 본문이 히어로 섹션 아래에 있으면 `element.scroll_into_view_if_needed()` 사용
- Cloudflare/reCAPTCHA 차단 시 → 대체 소스(같은 내용의 다른 플랫폼) 사용

**Medium 등 봇 차단 사이트 대체 우선순위**:
1. DEV.to, The New Stack, Zilliz Blog 등 개발자 플랫폼
2. 원문의 Google 캐시 또는 archive.org
3. 해당 없으면 텍스트 인용 + 링크로 대체 (스크린샷 없이)

### 어노테이션 타입

| 타입 | 용도 | Pillow 메서드 |
|------|------|--------------|
| `box` | 빨간 테두리 + 라벨 | `draw.rectangle(outline=)` |
| `fill` | 반투명 색 채우기 | `draw.rectangle(fill=RGBA)` |
| `underline` | 밑줄 | `draw.line()` |
| `text` | 텍스트 메모 | `draw.text()` + 배경 |
| `arrow` | 방향 지시 | `draw.line()` + `draw.ellipse()` |

## Example

```python
# Step 1: playwright로 좌표 획득
with sync_playwright() as p:
    page = browser.new_page(viewport={'width': 1280, 'height': 800})
    page.goto(url, wait_until='networkidle')
    el = page.query_selector('h1')
    box = el.bounding_box()  # {'x': 352, 'y': 173, 'width': 210, 'height': 32}
    page.screenshot(path='raw.png')

# Step 2: Pillow로 그리기
img = Image.open('raw.png')
draw = ImageDraw.Draw(img, 'RGBA')
font = ImageFont.truetype('/System/Library/Fonts/AppleSDGothicNeo.ttc', 16)
coords = (int(box['x'])-4, int(box['y'])-4,
          int(box['x']+box['width'])+4, int(box['y']+box['height'])+4)
draw.rectangle(coords, fill=(220,30,30,60))  # 반투명 빨강
draw.rectangle(coords, outline='#DC1E1E', width=4)  # 테두리
draw.text((coords[2]+20, coords[1]), '← 핵심!', fill='#FF6666', font=font)
img.save('annotated.png')
```

### 관련 파일
- 스크립트: `tmp/annotate-v2.py` (하이브리드 어노테이션 도구)
- 이미지 저장소: `github.com/cozytk/auto-lecture-assets`
- 노션 레퍼런스: `.claude/skills/guide-writer/notion-markdown-ref.md`
