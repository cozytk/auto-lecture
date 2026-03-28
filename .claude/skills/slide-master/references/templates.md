# 슬라이드 템플릿 모음

slide-master가 자주 사용하는 슬라이드 패턴과 코드 템플릿.

## Q&A 슬라이드 템플릿

```markdown
---
transition: slide-left
---

# ❓ Q&A

<div class="mt-4 space-y-6">
  <div>
    <div class="text-xl font-bold text-blue-400">Q. {질문}</div>
    <v-click>
      <div class="mt-2 pl-4 border-l-3 border-blue-500 text-gray-300">
        A. {핵심 답변 — 3줄 이내}
      </div>
    </v-click>
  </div>
  <div v-click>
    <div class="text-xl font-bold text-green-400">Q. {질문}</div>
    <v-click>
      <div class="mt-2 pl-4 border-l-3 border-green-500 text-gray-300">
        A. {핵심 답변 — 3줄 이내}
      </div>
    </v-click>
  </div>
</div>
```

## 비교 슬라이드 (긍정/부정 대비)

`two-cols-header` 레이아웃은 다크모드에서 원치 않는 배경색이 추가되므로 사용 금지. `default` + `grid grid-cols-2` 사용:

```html
<div class="grid grid-cols-2 gap-6 mt-4">
  <div>
    <h3 class="text-lg font-bold mb-3">JavaScript</h3>
    <ul class="space-y-2 text-sm">
      <li><span class="text-red-400 font-bold">런타임</span>에서 오류 발견</li>
    </ul>
  </div>
  <div>
    <h3 class="text-lg font-bold mb-3">TypeScript</h3>
    <ul class="space-y-2 text-sm">
      <li><span class="text-green-400 font-bold">컴파일 타임</span>에 오류 검출</li>
    </ul>
  </div>
</div>
```

핵심: 배경색이 아닌 **키워드 텍스트 색상**으로 긍정(`text-green-400`)/부정(`text-red-400`) 대비. 전체 텍스트를 색칠하지 않고 주요 용어만 강조.

## 외부 소스 인용 슬라이드

### 스크린샷 캡처 파이프라인 (screenshot-annotation 스킬 연동)

```bash
# Step 1: Playwright로 웹페이지 캡처 + 핵심 요소 좌표 획득
# Step 2: Pillow로 바운딩 박스 + 한글 어노테이션 그리기
# Step 3: assets/ 에 저장
# Step 4: 슬라이드에 삽입
```

구체적 구현:
```python
# Playwright: 스크린샷 + bounding box
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1280, 'height': 800})
    page.goto(url, wait_until='networkidle')
    el = page.query_selector('h1')  # 또는 관련 CSS 셀렉터
    box = el.bounding_box()
    page.screenshot(path='assets/source-raw.png')

# Pillow: 어노테이션
from PIL import Image, ImageDraw, ImageFont
img = Image.open('assets/source-raw.png')
draw = ImageDraw.Draw(img, 'RGBA')
font = ImageFont.truetype('/System/Library/Fonts/AppleSDGothicNeo.ttc', 18)
# 바운딩 박스 (빨간 테두리)
coords = (box['x']-4, box['y']-4, box['x']+box['width']+4, box['y']+box['height']+4)
draw.rectangle(coords, outline='#DC1E1E', width=3)
# 한글 어노테이션
draw.text((coords[2]+10, coords[1]), '← 핵심 주장', fill='#FF6666', font=font)
img.save('assets/source-annotated.png')
```

### 슬라이드 삽입 패턴

```html
<!-- 외부 소스 인용 슬라이드 -->
# {한글 요약 제목}

<img src="/assets/{source-annotated}.png" class="max-h-[340px] rounded-lg shadow-lg" />

<div class="mt-2 text-xs opacity-50">
  출처: <a href="{URL}" target="_blank">{원문 제목}</a>
</div>
```

> **리서치 브리프에 URL이 있는 핵심 소스는 반드시 스크린샷을 캡처한다.** 텍스트만으로 인용하지 않는다.

## 스크린샷 삽입 패턴

```html
<!-- 전체 너비 -->
<img src="/assets/{name}.png" class="max-h-[400px] rounded-lg shadow-lg mx-auto" />
<p class="text-xs opacity-40 text-center mt-2">캡션</p>

<!-- 좌측 이미지 + 우측 설명 -->
<div class="flex gap-6 items-start mt-4">
  <img src="/assets/{name}.png" class="max-h-[350px] rounded-lg shadow-lg flex-shrink-0" />
  <div class="flex-1">
    <h3>제목</h3>
    <p class="text-sm opacity-70">설명</p>
  </div>
</div>

<!-- 좌우 이미지 나란히 -->
<div class="grid grid-cols-2 gap-6 mt-4">
  <div class="text-center">
    <img src="/assets/{name1}.png" class="max-h-[380px] rounded-lg shadow-md" />
    <p class="text-xs opacity-50 mt-1">캡션 1</p>
  </div>
  <div class="text-center">
    <img src="/assets/{name2}.png" class="max-h-[380px] rounded-lg shadow-md" />
    <p class="text-xs opacity-50 mt-1">캡션 2</p>
  </div>
</div>
```

## 이미지 삽입 패턴

```html
<!-- 로컬 이미지 (flex 레이아웃) -->
<div class="flex gap-8 items-center mt-4">
  <img src="/assets/{name}.png" class="max-h-[300px] rounded-lg" />
  <div>
    <h3>설명 제목</h3>
    <p class="text-sm opacity-70">부가 설명</p>
  </div>
</div>

<!-- 플레이스홀더 (수동 교체용) -->
<div class="border-2 border-dashed border-gray-500 rounded-lg p-8 flex items-center justify-center max-h-[300px] mt-4">
  <div class="text-center">
    <div class="text-4xl mb-4">🖼️</div>
    <p class="text-lg font-bold">{이미지 설명}</p>
    <p class="text-sm opacity-50">TODO: {추가 안내}</p>
    <p class="text-xs opacity-30 mt-2">권장 크기: 800x450px / PNG or WebP</p>
  </div>
</div>
<!-- IMAGE: {상세 설명}. 검색: "{검색 쿼리}" -->
```
