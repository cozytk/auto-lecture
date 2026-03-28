# 다이어그램 가이드

## 선택 결정 트리

```
다이어그램이 필요한가?
├─ 애니메이션(v-click/$clicks)이 필요한가?
│   ├─ YES → HTML/CSS 다이어그램 (Mermaid는 v-click/CSS 애니메이션 불가)
│   └─ NO → 아래 계속
├─ 노드 5개 이상 + 복잡한 관계?
│   ├─ YES → Mermaid (자동 레이아웃이 수동보다 나음)
│   └─ NO → 아래 계속
├─ 크기/색상/간격을 정밀 제어?
│   ├─ YES → HTML/CSS
│   └─ NO → Mermaid (간단하고 유지보수 쉬움)
└─ 단순 선형 흐름 (A→B→C, 노드 2~4개)?
    └─ HTML/CSS (flex로 충분)
```

**요약**: Mermaid가 기본, 애니메이션이 필요하거나 정밀 제어가 필요하면 HTML/CSS.

## Mermaid 다이어그램 규칙

### 필수 설정

`setup/mermaid.ts` 다크 테마 파일이 있어야 한다. 없으면 `lectures/{topic}/slides/setup/mermaid.ts`에 생성. `style.css`에 `.mermaid svg { max-width: 100% }` 포함 필수.

### 방향 선택

| 방향 | 사용 시점 |
|------|----------|
| `graph TB` (위→아래) | **기본 선택**. 전체 너비 자연스럽게 활용 |
| `graph LR` (좌→우) | 노드 4개 이상일 때만. 적으면 너비를 못 채움 |
| `sequenceDiagram` | 참여자 수에 비례하여 너비 자동 확장 |

### 스타일

- `setup/mermaid.ts`의 테마가 적용되므로 `style` 지시어는 기본 불필요
- 특별한 색상 강조가 필요한 노드만 `style` 지시어 사용
- 노드 10개 이하
- `scale` 파라미터는 넘침 위험이 있을 때만 사용 (기본: 생략)

### Mermaid 애니메이션 제약 (테스트 검증 완료)

- `v-click-hide` + Mermaid 교체: 다이어그램이 사라지지 않고 누적됨
- CSS `.node` 타겟팅: SVG 내부에 외부 CSS 침투 불가
- **결론: 애니메이션이 필요한 다이어그램은 반드시 HTML/CSS로 제작**

## HTML/CSS 다이어그램 제작 원칙

HTML/CSS 다이어그램은 클래스, 시퀀스, 컴포넌트, 상태 등 **모든 유형의 다이어그램을 표현**할 수 있다.

### 기본 구성 요소

| 요소 | UnoCSS 패턴 | 용도 |
|------|-----------|------|
| 노드 (박스) | `bg-{color}-600 text-white px-5 py-3 rounded-xl font-bold shadow-lg` | 클래스, 컴포넌트, 상태, 참여자 |
| 카드 (구조체) | `bg-slate-800 rounded-xl border border-{color}-500 p-4` | 클래스(속성/메서드), 패키지(파일 목록) |
| 연결 화살표 | `text-xl opacity-50` + `→`, `↓`, `↕`, `◁——` | 관계, 흐름, 상속 |
| 타원 (유스케이스) | `border-2 border-{color}-500 rounded-full px-6 py-2` | 유스케이스, 상태 |
| 라벨 | `text-xs opacity-50` 또는 `text-sm font-bold text-{color}-400` | 관계 설명, 단계 번호 |
| 그룹/영역 | `bg-slate-800/50 border border-slate-600 rounded-2xl p-6` | 시스템 경계, subgraph |

### 레이아웃 조합

- 수평 흐름: `flex items-center justify-center gap-3`
- 수직 흐름: `flex flex-col items-center gap-4`
- 트리 구조: 상위 `flex justify-center` → 하위 `flex gap-4`
- 그리드: `grid grid-cols-3 gap-4`

### 카드형 다이어그램 (내부 구조가 있는 경우)

```html
<div class="bg-slate-800 rounded-xl border border-blue-500 w-56 shadow-lg">
  <div class="bg-blue-600 text-white px-4 py-2 rounded-t-xl font-bold text-center text-sm">클래스명</div>
  <div class="px-4 py-2 text-xs border-b border-slate-600 space-y-1">
    <div><span class="text-green-400">+</span> 속성: 타입</div>
  </div>
  <div class="px-4 py-2 text-xs space-y-1">
    <div><span class="text-green-400">+</span> 메서드(): 반환</div>
  </div>
</div>
```

### 선형 흐름 다이어그램

```html
<div class="flex items-center justify-center gap-2 mt-8">
  <div class="bg-blue-600 text-white px-6 py-4 rounded-xl text-center font-bold shadow-lg">
    <div class="text-sm opacity-70">단계 1</div>
    <div>이름</div>
  </div>
  <div class="text-2xl opacity-50">→</div>
  <div class="bg-green-600 text-white px-6 py-4 rounded-xl text-center font-bold shadow-lg">
    <div class="text-sm opacity-70">단계 2</div>
    <div>이름</div>
  </div>
</div>
```

### 애니메이션 적용

모든 HTML/CSS 다이어그램은 `$clicks` 또는 `v-click`으로 점진적 빌드업이 가능하다. Mermaid와 달리 개별 요소 단위로 등장/포커스/흐려짐을 제어할 수 있다. 상세 패턴은 `animation-patterns.md` 참조.

## two-cols 비교 슬라이드 원칙

**절대 `layout: two-cols-header` 사용 금지** — 다크모드에서 Slidev 테마가 자동으로 빨강/파랑 배경색을 추가하여 눈이 아프다.

대신 `default` 레이아웃 + `grid grid-cols-2`:

```html
<div class="grid grid-cols-2 gap-6 mt-4">
  <div><!-- 좌측 --></div>
  <div><!-- 우측 --></div>
</div>
```

긍정/부정 대비는 배경색이 아닌 **텍스트 색상**으로:
- 긍정: `<span class="text-green-400 font-bold">키워드</span>`
- 부정: `<span class="text-red-400 font-bold">키워드</span>`
