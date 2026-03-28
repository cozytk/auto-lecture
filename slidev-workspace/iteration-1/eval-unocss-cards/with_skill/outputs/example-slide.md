---
theme: default
title: UnoCSS Card Layout Examples
transition: fade
---

# 카드 레이아웃 패턴

다크 배경 위에 v-click으로 순차 등장하는 카드 예시

---

# 패턴 1: 3열 카드 그리드

<div class="grid grid-cols-3 gap-4 mt-6">

<div v-click class="bg-slate-800/80 rounded-xl p-5 shadow-xl border border-gray-700 transition forward:delay-100">

<div class="text-3xl mb-3 text-blue-400 font-bold">01</div>

**설계 단계**

요구사항을 분석하고 시스템 아키텍처를 설계한다

</div>

<div v-click class="bg-slate-800/80 rounded-xl p-5 shadow-xl border border-gray-700 transition forward:delay-200">

<div class="text-3xl mb-3 text-green-400 font-bold">02</div>

**구현 단계**

코드를 작성하고 단위 테스트를 실행한다

</div>

<div v-click class="bg-slate-800/80 rounded-xl p-5 shadow-xl border border-gray-700 transition forward:delay-300">

<div class="text-3xl mb-3 text-orange-400 font-bold">03</div>

**배포 단계**

CI/CD 파이프라인을 통해 프로덕션에 배포한다

</div>

</div>

<!--
클릭할 때마다 카드가 하나씩 나타납니다.
forward:delay를 줘서 앞으로 넘길 때 시차 효과가 있고,
뒤로 돌아갈 때는 딜레이 없이 바로 사라집니다.
-->

---

# 패턴 2: 2열 카드 + 포인트 컬러 테두리

<div class="grid grid-cols-2 gap-5 mt-4">

<div v-click class="bg-slate-800/80 rounded-xl p-6 shadow-xl border-l-4 border-blue-400">

**컨테이너 격리**

각 서비스가 독립적인 환경에서 실행되어 의존성 충돌이 없다

</div>

<div v-click class="bg-slate-800/80 rounded-xl p-6 shadow-xl border-l-4 border-green-400">

**빠른 배포**

이미지 빌드 후 수 초 만에 새 버전을 롤아웃할 수 있다

</div>

<div v-click class="bg-slate-800/80 rounded-xl p-6 shadow-xl border-l-4 border-purple-400">

**확장성**

수평 스케일링으로 트래픽 증가에 유연하게 대응한다

</div>

<div v-click class="bg-slate-800/80 rounded-xl p-6 shadow-xl border-l-4 border-orange-400">

**이식성**

어디서든 동일한 환경으로 실행할 수 있다

</div>

</div>

<!--
왼쪽 테두리 색상으로 각 카드의 성격을 구분합니다.
border-l-4로 포인트 라인을 줍니다.
-->

---

# 패턴 3: v-motion 슬라이드인 카드

<div class="flex flex-col gap-4 mt-4">

<div
  v-click
  v-motion
  :initial="{ x: -60, opacity: 0 }"
  :enter="{ x: 0, opacity: 1, transition: { delay: 0 } }"
  class="bg-slate-800/80 rounded-xl p-5 shadow-xl border border-gray-700"
>

**Step 1** -- 프로젝트 초기화

`pnpm create slidev` 명령으로 새 프로젝트를 생성한다

</div>

<div
  v-click
  v-motion
  :initial="{ x: -60, opacity: 0 }"
  :enter="{ x: 0, opacity: 1, transition: { delay: 150 } }"
  class="bg-slate-800/80 rounded-xl p-5 shadow-xl border border-gray-700"
>

**Step 2** -- 슬라이드 작성

`slides.md` 파일에 마크다운으로 내용을 작성한다

</div>

<div
  v-click
  v-motion
  :initial="{ x: -60, opacity: 0 }"
  :enter="{ x: 0, opacity: 1, transition: { delay: 300 } }"
  class="bg-slate-800/80 rounded-xl p-5 shadow-xl border border-gray-700"
>

**Step 3** -- 발표 및 배포

dev 서버로 발표하거나 PDF/SPA로 내보낸다

</div>

</div>

<!--
v-motion으로 왼쪽에서 슬라이드인하는 효과.
initial에서 x: -60으로 왼쪽 오프셋, opacity: 0으로 투명하게 시작.
enter에서 원래 위치로 돌아오며 나타납니다.
-->

---

# 패턴 4: 하이라이트 포인트 카드

<div class="grid grid-cols-2 gap-5 mt-4">

<div v-click class="bg-blue-900/30 rounded-xl p-6 shadow-xl border border-blue-500/50">

<div class="text-center">
  <span class="text-5xl font-bold text-blue-400">95%</span>
  <p class="text-gray-400 mt-2 text-sm">빌드 성공률</p>
</div>

</div>

<div v-click class="bg-green-900/30 rounded-xl p-6 shadow-xl border border-green-500/50">

<div class="text-center">
  <span class="text-5xl font-bold text-green-400">3.2s</span>
  <p class="text-gray-400 mt-2 text-sm">평균 배포 시간</p>
</div>

</div>

<div v-click class="bg-purple-900/30 rounded-xl p-6 shadow-xl border border-purple-500/50">

<div class="text-center">
  <span class="text-5xl font-bold text-purple-400">42</span>
  <p class="text-gray-400 mt-2 text-sm">일일 배포 횟수</p>
</div>

</div>

<div v-click class="bg-orange-900/30 rounded-xl p-6 shadow-xl border border-orange-500/50">

<div class="text-center">
  <span class="text-5xl font-bold text-orange-400">99.9%</span>
  <p class="text-gray-400 mt-2 text-sm">서비스 가용성</p>
</div>

</div>

</div>

<!--
통계/수치를 강조하는 포인트 카드.
각 카드에 해당 색상 계열의 bg/border/text를 일관되게 적용합니다.
bg-blue-900/30 같이 낮은 투명도로 은은한 배경을 줍니다.
-->

---

# 패턴 5: 라이트/다크 모드 호환 카드

<div class="grid grid-cols-3 gap-4 mt-6">

<div v-click class="bg-white dark:bg-slate-800/80 rounded-xl p-5 shadow-lg border border-gray-200 dark:border-gray-700 text-gray-800 dark:text-gray-100">

**라이트/다크 호환**

`dark:` 접두사로 모드별 스타일을 분리한다

</div>

<div v-click class="bg-white dark:bg-slate-800/80 rounded-xl p-5 shadow-lg border border-gray-200 dark:border-gray-700 text-gray-800 dark:text-gray-100">

**반응형 색상**

`bg-white dark:bg-slate-800/80`으로 배경을 전환한다

</div>

<div v-click class="bg-white dark:bg-slate-800/80 rounded-xl p-5 shadow-lg border border-gray-200 dark:border-gray-700 text-gray-800 dark:text-gray-100">

**테두리도 전환**

`border-gray-200 dark:border-gray-700`로 테두리 색을 맞춘다

</div>

</div>

<div v-click class="mt-6 bg-yellow-100/80 dark:bg-yellow-900/30 rounded-lg p-4 border border-yellow-300 dark:border-yellow-600 text-yellow-800 dark:text-yellow-200 text-sm">

**Tip**: 다크모드 전용 프로젝트라면 `dark:` 접두사 없이 어두운 색상을 직접 사용해도 된다

</div>

<!--
dark: 접두사를 활용하면 라이트/다크 모드 전환에 대응할 수 있습니다.
프로젝트가 다크모드 전용이라면 dark: 없이 어두운 색상을 직접 쓰면 됩니다.
-->
