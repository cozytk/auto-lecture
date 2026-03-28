---
theme: default
title: "Playwright vs Agent-Browser 스크린샷 비교"
---

# Playwright vs Agent-Browser
## 외부 웹사이트 스크린샷 비교 테스트

대상: `github.com/anthropics/claude-code` (다크모드)

---

## 순수 캡처 비교 — Playwright

<img src="/assets/compare/pw-raw.png" class="w-full rounded shadow" />

<div class="text-sm mt-2 text-gray-400">

`1280x800` · 195KB · 다크모드 완벽 · 4.84초

</div>

---

## 순수 캡처 비교 — Agent-Browser

<img src="/assets/compare/ab-raw.png" class="w-full rounded shadow" />

<div class="text-sm mt-2 text-gray-400">

`1280x633` · 139KB · 뷰포트 높이 800→633 잘림 · ~5초

</div>

---
layout: two-cols-header
---

## 순수 캡처 나란히 비교

::left::

### Playwright
<img src="/assets/compare/pw-raw.png" class="rounded shadow" />

- 1280x800 (정확)
- 195KB

::right::

### Agent-Browser
<img src="/assets/compare/ab-raw.png" class="rounded shadow" />

- 1280x633 (높이 잘림)
- 139KB

---

## 어노테이션 비교 — Playwright + Pillow

<img src="/assets/compare/pw-annotated.png" class="w-full rounded shadow" />

<div class="text-sm mt-2 text-gray-400">

CSS 셀렉터로 원하는 요소만 선택 → Pillow로 커스텀 박스/라벨 · 204KB

</div>

---

## 어노테이션 비교 — Agent-Browser `--annotate`

<img src="/assets/compare/ab-annotated.png" class="w-full rounded shadow" />

<div class="text-sm mt-2 text-gray-400">

모든 interactive 요소에 빨간 번호 라벨 자동 부착 (232개) · 174KB · 노이즈 과다

</div>

---
layout: two-cols-header
---

## 어노테이션 나란히 비교

::left::

### Playwright + Pillow
<img src="/assets/compare/pw-annotated.png" class="rounded shadow" />

- 원하는 요소만 선택적 강조
- 색상/라벨/화살표 자유 커스텀

::right::

### Agent-Browser --annotate
<img src="/assets/compare/ab-annotated.png" class="rounded shadow" />

- 232개 요소 전체 자동 라벨링
- AI 탐색용 (교육용 부적합)

---

## 정량 비교

| 항목 | Playwright | Agent-Browser |
|------|-----------|--------------|
| **뷰포트 정확도** | 1280x800 (정확) | 1280x633 (높이 잘림) |
| **캡처 시간** | 4.84초 | ~5초 |
| **파일 크기 (raw)** | 195KB | 139KB |
| **다크모드** | colorScheme API (완벽) | --color-scheme (CSS만) |
| **바운딩박스 획득** | `el.bounding_box()` 직접 | `eval` + `getBoundingClientRect` |
| **어노테이션 방식** | Pillow 커스텀 그래픽 | --annotate (전체 자동) |
| **교육용 적합도** | 높음 | 낮음 (노이즈) |

---

## 결론

<div class="grid grid-cols-2 gap-8 mt-4">
<div class="p-4 rounded bg-green-900/30 border border-green-500/50">

### Playwright + Pillow 선택

- 교육용 어노테이션 (선택적 강조)
- 정확한 뷰포트 제어 필요 시
- 배치 캡처 파이프라인
- 슬라이드 삽입용 이미지

</div>
<div class="p-4 rounded bg-blue-900/30 border border-blue-500/50">

### Agent-Browser 선택

- 외부 사이트 인터랙션 (로그인, 클릭)
- AI가 페이지 구조 파악 (snapshot)
- 쿠키 배너 처리 + 캡처
- 빠른 1회성 캡처

</div>
</div>
