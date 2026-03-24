---

name: slide-master

description: 강의 가이드(guide/)를 slidev 슬라이드(slides.md)로 변환하여 교육용 프레젠테이션을 처음부터 생성한다. 이 스킬은 slidev 스킬보다 우선한다 — 사용자가 슬라이드를 "만들어줘", "생성해줘", "작성해줘" 또는 가이드를 "프레젠테이션으로 변환"하거나, "장표 작업", "슬라이드 장표", lectures/ 디렉토리 기반의 교육 슬라이드 제작을 언급하면 반드시 이 스킬을 사용한다. 슬라이드를 새로 만드는 모든 요청에 사용하고, 기존 슬라이드 수정이나 Slidev 기술 문제에는 사용하지 않는다.

model: sonnet

context: fork

disable-model-invocation: true

allowed-tools: Read, Write, Edit, Grep, Glob, Bash, WebSearch, WebFetch

argument-hint: "[topic]"

---

# 슬라이드 마스터

강의 가이드를 slidev 프레젠테이션으로 변환한다. 가이드의 요약이 아니라 **발표의 시각적 보조 도구**를 만든다.

> **역할 분리**: 이 스킬(slide-master)은 **교수법적 설계** — 무엇을 넣을지, 어떤 순서로 보여줄지, 어떻게 학생의 이해를 돕는지 — 에 집중한다. Slidev 프레임워크의 구체적인 **구현 패턴** — `$clicks` 다이어그램 애니메이션, 코드+설명 동기화, v-motion, v-mark 사용법 — 은 `slidev` 스킬(`/slidev`)의 `references/advanced-patterns.md`를 반드시 참조한다. 특히 다이어그램 애니메이션과 코드 설명 동기화 패턴은 slidev 스킬에 검증된 구현이 있으므로 직접 만들지 말고 참조한다.

## 입력 및 산출물

- 입력: `lectures/{topic}/guide/` 디렉토리 (없으면 에러 출력 후 중단)
- 산출물: `lectures/{topic}/slides/slides.md`, `lectures/{topic}/slides/assets/`

---

## 작업 순서 (2단계 생성)

슬라이드 생성을 아웃라인과 상세 작성으로 분리하여 방향 오류를 조기에 발견한다.

### Phase 1: 아웃라인

1. 가이드 전체 파일 읽기 → 구조 분석
2. **슬라이드 아웃라인** 생성 — 각 슬라이드의 제목, 핵심 메시지, 레이아웃 유형, 시각 요소 유형(Mermaid/HTML 다이어그램/이미지/코드)을 1줄씩 나열
3. 아웃라인 검증:
   - 텍스트 전용 슬라이드가 3장 연속되는 구간이 없는지 확인 (Rule 9)
   - 가이드의 핵심 개념이 빠짐없이 포함되었는지 확인
   - Q&A 슬라이드가 각 섹션 끝에 배치되었는지 확인
4. 아웃라인을 사용자에게 제시하고 피드백 대기 (HITL 모드일 때)

### Phase 2: 상세 작성

1. 아웃라인에 따라 slides.md 전체 작성
2. WebSearch로 이미지 검색 → assets 저장
3. 자가 검증 → Playwright 시각 검증 → 완료 보고

> **Full-Auto 모드**: HITL이 아니면 Phase 1 검증 후 바로 Phase 2로 진행한다. 다만 아웃라인은 내부적으로 반드시 생성하고, 시각 밀도 검증을 통과한 후에만 상세 작성에 들어간다.

---

## 핵심 원칙

### 슬라이드 구조

1. **한 슬라이드 = 하나의 메시지.** 두 가지 이상의 개념을 한 장에 넣지 않는다. 슬라이드는 많을수록 좋다 — 압축하지 말고 분할한다.

2. **넘침 금지.** 캔버스는 980×552px 고정이다. 넘칠 것 같으면 분할한다. 불릿 최대 5개, 코드 블록 최대 15줄, 본문 300자. 약간 넘칠 때는 `zoom: 0.9`(0.8 미만 금지). 하단 잘림에 주의한다.

3. **제목은 한 줄.** 한글 20자/영문 40자 초과 금지. 개념/섹션 제목은 `1. {제목}` 형식. `개념 1: {제목}` 금지.

4. **전환·휴식 슬라이드**(점심시간, 쉬는 시간 등)는 간결하게. 불릿이나 배경 박스 없이 제목 + 시간 + 간단한 안내만.

5. **정보 밀도가 높은 개념은 여러 슬라이드로 분할한다.** 연구 결과, 통계, 그래프, 도표를 나열하는 슬라이드는 하나에 다 넣지 않는다. 각 데이터 포인트를 별도 슬라이드로 만들어 다이어그램·차트·애니메이션으로 시각화한다.

6. **핵심 정리 슬라이드는 통일된 스타일로.** 세션/교시 마무리 정리 슬라이드에서 항목마다 다른 배경색을 쓰지 않는다. 모든 항목을 동일한 중립 배경(`bg-slate-800/50`)으로 통일하고 `font-bold`로 강조한다.

### 시각 설계

7. **v-click으로 점진적 공개.** 불릿, 카드, 코드 설명은 한 번에 보여주지 않는다. `<div>` 내부에서 `<v-clicks>`를 쓸 때는 전후에 빈 줄 필요.

8. **가이드의 "왜"를 슬라이드의 "무엇"으로.** 자세한 설명은 발표자 노트에, 슬라이드엔 키워드와 코드만.

9. **볼드가 기본, 색상은 의미 있는 대비에만.** 강조에는 `<strong>` 또는 `font-bold`를 우선 사용한다. 색상은 다음 경우에**만** 허용한다:
    - **개념 대비**: 긍정(`text-green-400`) vs 부정(`text-red-400`) 같은 의미 있는 대비
    - **그룹화**: 같은 색상으로 동일 범주 항목을 묶을 때
    - **절대 금지**: 한 슬라이드에서 3색 이상 사용. 리스트 항목마다 다른 색상 부여.
    - 배경 박스(`bg-{color}-50 rounded-lg`)는 슬라이드당 최대 1개, 코드 블록 공존 금지.

10. **시각적 위계와 폰트 크기 유동 적용.** 여백이 충분하면 적정 크기(`text-lg`~`text-xl`)로 키우고, 부족하면 최소(`text-sm`)까지만 줄인다. `text-xs`는 캡션/출처에만 사용. 내용이 넘치면 폰트를 줄이지 말고 **슬라이드를 분할**한다. 다이어그램/코드 아래 설명 텍스트는 남은 여백을 적극 활용하여 `text-lg` 이상으로 키운다. 빈 공간보다 큰 텍스트가 낫다. slidev 스킬의 Font Size Guidelines 참조.

11. **하단 정리 박스(callout)는 크고 선명하게.** `text-lg` 이상 + `text-center` + `font-bold`. `opacity` 클래스 사용 금지. 배경: `bg-slate-800/50` 또는 `bg-gray-50 dark:bg-gray-800`. 위 콘텐츠와 충분한 간격(`mt-6` 이상).

12. **시각 자료를 적극 삽입한다 (3장 연속 텍스트 금지).** 텍스트 전용 슬라이드가 3장 연속되면 반드시 Mermaid, HTML/CSS 다이어그램, 이미지, 또는 플레이스홀더를 삽입한다. 아웃라인 단계에서 미리 시각 요소 배치를 계획하고, 상세 작성 시 누락 없이 반영한다. 다이어그램 유형 선택은 `references/diagram-guide.md`의 결정 트리를 따른다.

13. **비교 슬라이드는 좌우 색상을 다르게.** 대비되는 개념은 동일 크기·위치로 배치하되 다른 색상 계열로 구분한다. 비교 슬라이드가 심심하면 카드 형태로 좌우를 감싸거나, 핵심 수치를 `text-5xl font-bold`로 강조한다.

### 좌우 분할 레이아웃 제한

14. **좌우 분할(`grid`, `two-cols`)은 직접 비교 전용.** 다음 경우에만 사용한다:
    - 두 개념의 **직접적 대비** (장점 vs 단점, Before vs After)
    - 왼쪽 설명과 오른쪽 시각 자료가 **반드시 동시에** 보여야 하는 경우

    다음 경우에는 **별도 슬라이드로 분리**한다:
    - 왼쪽과 오른쪽이 독립적인 정보인 경우
    - 각 영역이 충분한 공간을 필요로 하는 경우
    - 한쪽이 중앙 정렬이 더 효과적인 경우

### 외부 소스 인용 규칙

15. **외부 소스 인용 시 출처를 접근 가능하게 제공한다.**
    - **URL 날조 금지** — WebSearch로 실제 URL을 찾고 WebFetch로 200 OK 검증 후에만 삽입. 검증 실패 시 텍스트 출처만 표기하거나 상위 도메인으로 대체.
    - 인용문/통계에는 반드시 클릭 가능한 링크 포함
    - 핵심 소스는 웹페이지 스크린샷을 캡처하여 이미지로 삽입 (상세: `references/templates.md`)
    - 영문 소스는 핵심 문장을 한글로 요약/번역
    - 하나의 소스 = 하나의 슬라이드

### Mermaid 다이어그램 제약

16. **Mermaid `subgraph`는 PDF export에서 렌더링되지 않는다.** `subgraph`를 사용한 다이어그램은 PDF에서 빈 화면으로 출력된다. 대안: HTML/CSS `<div>` + UnoCSS로 동일한 레이아웃을 구현한다. 단순 `flowchart LR` (subgraph 없음)은 정상 동작한다.

17. **Mermaid `flowchart`에서 노드가 5개를 초과하거나 세로(TD) 방향이면 하단이 잘린다.** 가로(`LR`) 방향을 기본으로 사용하고, 노드가 많으면 HTML/CSS 다이어그램으로 대체한다.

### Slidev 렌더링 제약 (기술적 필수)

18. **HTML 태그 내부에서 `**bold**` 금지.** `<div>`, `<v-click>` 등 HTML/Vue 태그 안에서는 `<strong>` 또는 UnoCSS(`font-bold`)를 사용한다.

19. **Markdown 번호 목록(`1.`, `2.`)을 슬라이드 본문에 쓰지 않는다.** Slidev에서 부제목처럼 렌더링된다. `<v-clicks>` + 불릿(`-`)이나 원기호(①②③)를 사용하되, 혼용하지 않는다.

20. **발표자 노트의 `[click]` 수 = 슬라이드의 v-click 단계 수.** 반드시 영어 `[click]`을 사용한다(`[클릭]` 금지).

### 코드 블록

21. **라인 하이라이트 범위는 논리적 코드 단위와 일치시킨다.** 각 `|` 단계가 함수, 객체, 블록의 중간에서 끊기면 안 된다. 작성 후 줄 번호를 세어 검증한다.

22. **15줄 초과 코드 블록은 분할하거나 `{maxHeight:'380px'}`를 추가한다.** 라인 하이라이트와 결합 시: `{1-10|12-20}{maxHeight:'380px'}` (공백 없이).

### Q&A 슬라이드

23. **Q&A는 독립된 전용 슬라이드로.** 개념 슬라이드에 끼워넣지 않는다. 각 섹션 마지막(퀴즈 직전)에 Q&A 1~2장 배치. 슬라이드당 최대 2문항. 답변이 긴 문항은 1문항 = 1슬라이드.

24. **Q&A 선별 기준**: ① 흔한 오해 → ② 수강생 배경 질문 → ③ 자주 묻는 질문. 전부 넣을 필요 없다. 나머지는 발표자 노트에 남긴다.

25. **Q&A 형식**: 질문을 먼저 보여주고 v-click으로 답변 공개. 답변 3줄(약 120자) 이내. 상세 템플릿은 `references/templates.md` 참조.

### 퀴즈

26. **퀴즈 정답을 시각적으로 노출하지 않는다.** 모든 선택지를 동일 배경색으로 초기 표시하고 v-click으로 정답 공개. `v-click-hide` 문법은 Context7로 확인.

---

## 최신성 규칙

- 시간 민감한 모델명, 통계, 날짜는 현재 연도(2026년) 기준으로 갱신한다.
- 과거 사례는 시점을 명시하고 최신 대안과 구분한다.
- 확신할 수 없는 연도/버전은 검증 후 사용한다.

---

## 폰트 지침 (Freesentation)

`lectures/{topic}/slides/style.css`에 Freesentation 폰트를 적용한다. 없으면 생성.

- `assets/fonts/`에 ttf 파일이 없으면 시스템 폰트(`~/Library/Fonts/Freesentation*.ttf`)에서 복사
- 9개 웨이트(100~900) 전체를 `@font-face`로 등록

| 요소 | Weight | 용도 |
|------|--------|------|
| `h1` | 900 (Black) | 표지/섹션 제목 |
| `h2` | 800 (ExtraBold) | 슬라이드 제목 |
| `h3` | 700 (Bold) | 부제목 |
| `h4`~`h6` | 600 (SemiBold) | 소제목 |
| 본문 | 400 (Regular) | 일반 텍스트 |
| `strong`, `b` | 800 (ExtraBold) | 강조 텍스트 |
| `.text-sm`, `.text-xs` | 300 (Light) | 캡션, 출처 |
| `blockquote` | 200 (ExtraLight) | 인용문, 부제 |

---

## 스타일링 빠른 참조

UnoCSS(Tailwind 호환) 내장. 전체 문법은 slidev 스킬 references 참조.

### 필수 패턴
- 이미지: `max-h-[380px]`(전체) / `max-h-[320px]`(two-cols 내), 반드시 `rounded-lg shadow-lg` 추가
- 넘침 방지: 본문 컨테이너에 `overflow-hidden`
- 하단 고정 정보: `absolute bottom-6 left-14 text-xs opacity-50`
- 강조(기본): `<strong>` 또는 `font-bold` — 색상은 의미 있는 대비에만 (Rule 9)
- 배경 박스: `bg-slate-800/50 rounded-lg p-4` — 슬라이드당 최대 1개, 코드 블록 공존 금지
- 하단 정리 박스: `bg-slate-800/50 rounded-lg p-4 text-center text-lg` — opacity 금지
- 비교 슬라이드: `default` + `grid grid-cols-2` (**`two-cols-header` 금지**) → 상세 템플릿은 `references/templates.md`

### 이미지·스크린샷 삽입 패턴

상세 코드 패턴은 `references/templates.md` 참조. 핵심 규칙만:
- 모든 이미지에 `max-h` 클래스 필수
- 이미지에는 반드시 `rounded-lg shadow-lg` 추가
- 이미지 검색 실패 시 플레이스홀더로 대체 (빈 슬라이드 금지)
- `<!-- IMAGE: -->` 주석은 slide-reviewer가 탐지

---

## 다이어그램 전략

시각 자료는 선택이 아니라 필수다. 다이어그램 유형 선택과 상세 구현 패턴은 `references/diagram-guide.md` 참조.

### 핵심 결정 기준

| 조건 | 선택 |
|------|------|
| 애니메이션 필요 | HTML/CSS (Mermaid는 v-click 불가) |
| 노드 5+ 복잡한 관계 | Mermaid (자동 레이아웃) |
| 단순 선형 흐름 (2~4노드) | HTML/CSS (flex로 충분) |
| 정밀 크기/색상 제어 | HTML/CSS |
| 그 외 | Mermaid (기본) |

### 이미지 소스 우선순위

| 순위 | 소스 | 삽입 방법 |
|------|------|---------|
| 1 | Mermaid 다이어그램 | ` ```mermaid {scale: 0.7} ` 코드 블록 |
| 2 | 로컬 이미지 (`assets/`) | `<img src="/assets/{name}" class="max-h-[380px]" />` |
| 3 | GitHub 호스팅 이미지 | `<img src="https://raw.githubusercontent.com/cozytk/auto-lecture-assets/main/..." />` |
| 4 | SVG 벡터 | `<img src="/assets/{name}.svg" />` |
| 5 | 플레이스홀더 | 플레이스홀더 패턴 (templates.md 참조) |

### 필수 규칙
- **텍스트 3장 연속 금지** — 중간에 시각 요소 삽입
- 이미지에는 반드시 `max-h` 클래스 지정
- Mermaid: `setup/mermaid.ts` 다크 테마 필수, `.mermaid svg { max-width: 100% }` in style.css

---

## 애니메이션 지침

**구현 패턴은 slidev 스킬의 `references/advanced-patterns.md`를 반드시 읽고 따른다.** 아래는 교수법적 판단 기준만 정리한다.

| 콘텐츠 | 애니메이션 | slidev 스킬 참조 |
|---------|-----------|------------------|
| 불릿 리스트 | `v-clicks` 순차 공개 | core-animations |
| 코드 블록 | 라인 하이라이트 + **설명 동기화** | **advanced-patterns §3** |
| 코드 진화 과정 | Magic Move | code-magic-move |
| 핵심 수치·카드 | `v-motion` 슬라이드인 | **advanced-patterns §4** |
| 키워드 강조 | `v-mark` | **advanced-patterns §5** |
| HTML/CSS 다이어그램 | `$clicks` + opacity/ring | **advanced-patterns §1-2** |
| Before/After 비교 | `v-switch` | **advanced-patterns §6** |
| 카드 순차 등장 | `forward:delay-*` | **advanced-patterns §7** |

### 교수법적 원칙

- **코드 설명**: 한 줄 포커스 → 바로 설명. "전체 포커스 후 전체 설명"은 금지. slidev 스킬의 코드+설명 동기화 패턴을 사용.
- **다이어그램**: 구성요소를 하나씩 하이라이트하며 각 요소의 역할을 설명. 요소를 새로 만들지 않고 기존 요소에 opacity/ring으로 집중. slidev 스킬의 $clicks 다이어그램 패턴을 사용.
- **전환**: cover/section은 `fade`, 일반은 `slide-left`
- 모션 딜레이 최대 400ms, 한 슬라이드에 v-click + v-motion + v-mark 동시 사용 금지
- **$clicks 필수 주의**: `v-click` 없이 `$clicks`만 사용하는 슬라이드는 반드시 프론트매터에 `clicks: N` 선언

---

## 레이아웃 선택 기준

전체 레이아웃 목록은 slidev 스킬 references 참조.

| 콘텐츠 유형 | 레이아웃 |
|---|---|
| 표지/마무리 | `cover` / `end` |
| 섹션 구분 | `section` |
| 일반 콘텐츠 | `default` |
| 코드+설명, 비교 | `default` + `grid grid-cols-2` (**`two-cols-header` 금지**) |
| 다이어그램+설명 | `image-left` / `image-right` |
| 수치 강조 | `fact` / `statement` |
| 인용문 | `quote` |
| Q&A | `default` (Q&A 전용 템플릿) |
| 전체 화면 이미지 | `image` |
| 외부 콘텐츠 임베드 | `iframe` / `iframe-left` / `iframe-right` |

---

## 발표자 노트

> **발표자 대본(스크립트)은 `script-writer` 스킬이 담당한다.** slide-master는 발표자 대본을 작성하지 않는다.

slide-master는 슬라이드 장표의 시각적 레이아웃에 집중한다. 대본은 비워두거나 최소한의 구조 힌트만 남긴다:

```markdown
<!--
[스크립트 — script-writer가 작성 예정]
-->
```

script-writer가 대본을 작성할 때 v-click 단계를 파악할 수 있도록, **슬라이드의 v-click 구조는 명확하게** 작성한다.

---

## 자가 검증

작성 완료 후 모든 슬라이드를 순회하며 확인한다:

### 구조 검증
1. **오버플로**: 넘침·하단 잘림 없는가? 이미지에 `max-h` 있는가? (Rule 2)
2. **시각 밀도**: 텍스트 전용 슬라이드가 3장 연속되지 않는가? (Rule 12)
3. **Q&A 분리**: 개념 슬라이드에 Q&A가 끼워넣어지지 않았는가? 슬라이드당 2문항 이하인가? (Rule 21~23)
4. **퀴즈**: 정답이 초기 상태에서 색상으로 노출되지 않는가? (Rule 24)

### 스타일 검증
5. **애니메이션**: v-click 또는 라인 하이라이트가 사용되었는가? (Rule 7)
6. **HTML 내 볼드**: `**...**`가 HTML/Vue 태그 안에서 쓰이지 않았는가? (Rule 16)
7. **배경 박스**: 슬라이드당 1개 이하이고, 코드 블록과 공존하지 않는가? (Rule 9)
8. **색상 남용**: 한 슬라이드에 3색 이상 사용하지 않았는가? (Rule 9)
9. **최소 폰트**: 본문에 `text-xs`를 사용하지 않았는가? (Rule 10)
10. **하단 정리 박스**: opacity 미사용, `text-lg` 이상, `text-center`인가? (Rule 11)
11. **코드 하이라이트**: 범위가 논리적 코드 단위의 경계와 일치하는가? (Rule 19)

### 기술 검증
12. **$clicks 프론트매터**: `$clicks`를 사용하는 모든 슬라이드에 `clicks: N`이 선언되었는가?
13. **폰트**: `style.css`에 Freesentation 폰트 설정이 있는가?
14. **Mermaid 설정**: `setup/mermaid.ts` 다크 테마 파일이 존재하는가?
15. **URL 검증**: 모든 외부 링크를 WebFetch로 접근 확인했는가? (Rule 15)

### 스크립트-슬라이드 싱크 검증 (script-writer 연동용)
16. 모든 `v-click` 단계에 대응하는 `[click]`이 필요함을 인지
17. 스크립트에서 언급할 시각 요소가 실제 슬라이드에 존재하는지 확인
18. `시간: X분` 대비 1분당 약 200자 기준으로 스크립트 길이 점검 가능하도록 슬라이드 구조 명확화

### Playwright 시각 검증

> **스크린샷 캡처**: `scripts/capture-slide.mjs`가 서버 시작→캡처→종료를 단일 프로세스에서 처리한다.

```bash
# 스크린샷 캡처 (서버 자동 관리)
node scripts/capture-slide.mjs lectures/{topic}/slides

# 인터랙티브 미리보기 (사용자가 브라우저로 확인)
scripts/slidev-serve.sh start lectures/{topic}/slides slides.md --port 3030
# → http://localhost:3030
scripts/slidev-serve.sh stop
```

Slidev를 렌더링한 뒤 Playwright로 시각 검증을 수행한다. 잘림, 오버플로, 겹침, 누락된 이미지를 우선 확인한다.

> **Slidev 실행 상세**: TTY 제약, 포트 관리, exit code 등 기술 상세는 `slidev-execution-guide.md` 참조.

---

## 완료 보고

위반 항목은 수정 후 완료 보고:

```
슬라이드 생성 완료: lectures/{topic}/slides/slides.md
- 총 슬라이드 수: N장
- 시각 요소: Mermaid N개, HTML/CSS 다이어그램 N개, 이미지 N개 (placeholder: N개)
- 애니메이션: v-click N / v-motion N / magic-move N
- 텍스트 연속 최대: N장 (3장 이하 확인)
- 발표자 대본: script-writer 실행 필요
```
