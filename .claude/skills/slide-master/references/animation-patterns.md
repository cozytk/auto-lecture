# 애니메이션 패턴

## $clicks 다이어그램 단계별 집중 패턴

HTML/CSS 다이어그램에서 클릭할 때마다 특정 단계에 집중시키는 패턴. `$clicks` 변수 + opacity/ring 조합.

### `clicks: N` 프론트매터 필수

`v-click` 없이 `$clicks`만 사용하는 슬라이드는 반드시 프론트매터에 `clicks: N`을 선언한다. 선언하지 않으면 Slidev가 클릭 수를 0으로 인식하여 스페이스바가 동작하지 않는다.

```markdown
---
clicks: 4
---
## 제목
<div :class="$clicks >= 1 ? '...' : '...'">...</div>
```

`v-click`과 혼용하는 경우에는 `v-click` 수가 자동으로 총 클릭 수를 결정하므로 `clicks:` 선언 불필요.

### 단계별 포커스

```html
<!-- 현재 단계: ring + scale-105, 나머지: opacity-40 -->
<div class="... transition-all duration-300"
     :class="$clicks === 0 ? 'ring-2 ring-blue-300 scale-105' : 'opacity-40'">
  <div>단계 1</div>
</div>
<div class="... transition-all duration-300"
     :class="$clicks === 1 ? 'ring-2 ring-green-300 scale-105' : 'opacity-40'">
  <div>단계 2</div>
</div>
<!-- 마지막 단계: $clicks >= N 으로 최종 상태 유지 -->
<div class="... transition-all duration-300"
     :class="$clicks >= 2 ? 'ring-2 ring-amber-300 scale-105' : 'opacity-40'">
  <div>단계 3</div>
</div>
```

### 핵심 규칙

- `transition-all duration-300` 필수 — 부드러운 전환
- 현재 단계: `ring-2 ring-{color}-300 scale-105` — 테두리 + 약간 확대
- 비활성 단계: `opacity-40` — 흐리게
- 마지막 단계는 `$clicks >= N`으로 최종 상태 유지
- 화살표(`→`)는 항상 `opacity-30`으로 고정
- **도형-텍스트 동기화**: 도형 개수와 설명 텍스트가 항상 호응해야 한다

### 단계별 설명 전환 (다이어그램 아래)

다이어그램 아래에 각 단계의 설명 텍스트를 `$clicks` 조건으로 전환한다. 도형만 포커스하고 설명이 없으면 학생이 무엇을 봐야 하는지 모른다.

```html
<div class="mt-4 bg-slate-800/50 rounded-lg p-4 text-center min-h-16 relative overflow-hidden">
  <div class="text-lg transition-all duration-300 absolute inset-0 flex items-center justify-center"
       :class="$clicks === 0 ? 'opacity-50' : 'opacity-0 pointer-events-none'">클릭하여 설명 확인</div>
  <div class="text-lg transition-all duration-300 absolute inset-0 flex items-center justify-center"
       :class="$clicks === 1 ? 'opacity-100' : 'opacity-0 pointer-events-none'">
    <strong>단계 1</strong>: 이 단계의 설명
  </div>
  <div class="text-lg transition-all duration-300 absolute inset-0 flex items-center justify-center"
       :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0 pointer-events-none'">
    <strong>단계 2</strong>: 이 단계의 설명 (마지막은 >= 사용)
  </div>
  <div class="invisible text-lg">placeholder</div>
</div>
```

**구현 노트**:
- 모든 설명 div는 `absolute inset-0 flex items-center justify-center`로 겹쳐 놓는다
- 활성: `opacity-100`, 비활성: `opacity-0 pointer-events-none`
- 마지막 div의 `invisible` placeholder가 컨테이너 높이를 확보한다
- 마지막 단계는 `$clicks >= N`으로 최종 상태를 유지한다
