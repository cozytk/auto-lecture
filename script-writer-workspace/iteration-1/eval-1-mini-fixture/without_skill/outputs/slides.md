---
theme: default
title: Git 기초 - 버전관리 개념부터 브랜치까지
transition: slide-left
mdc: true
---

# Git 기초

## 버전관리 개념부터 브랜치까지

<div class="mt-8 text-lg text-gray-400">
Day 1 - Session 1 (1시간)
</div>

<div class="absolute bottom-8 left-14 text-sm text-gray-500">
대상: 주니어 개발자 | CLI 기본 조작 가능 수준
</div>

<!-- [스크립트]
안녕하세요, 오늘은 Git 기초에 대해 함께 배워보겠습니다.
이번 세션은 약 1시간 분량이고, 버전관리의 개념부터 시작해서 브랜치까지 다룰 예정입니다.
CLI 기본 조작이 가능하신 분들을 대상으로 진행하니까, 터미널 열고 따라오시면 됩니다.
-->

---
transition: slide-left
---

# 오늘 배울 것

```mermaid {scale: 0.6}
graph LR
    A["🗂️ 버전관리"] --> B["📋 Git 3영역"]
    B --> C["🌿 브랜치"]
    C --> D["⌨️ 실습"]

    style A fill:#1a365d,stroke:#3182ce,color:#fff
    style B fill:#744210,stroke:#d69e2e,color:#fff
    style C fill:#22543d,stroke:#38a169,color:#fff
    style D fill:#553c9a,stroke:#9f7aea,color:#fff
```

<v-clicks>

- 버전관리의 필요성과 Git의 핵심 개념
- Git의 3가지 영역: Working Directory, Staging Area, Repository
- 기본 명령어: `init`, `add`, `commit`, `status`, `log`
- 브랜치 생성과 병합(merge)

</v-clicks>

<!-- [스크립트]
오늘 세션의 전체 흐름을 먼저 보겠습니다.
크게 네 단계로 진행됩니다.

첫째, 버전관리가 왜 필요한지, 그 개념을 잡고요.
둘째, Git이 파일을 관리하는 3가지 영역 — Working Directory, Staging Area, Repository — 을 이해합니다.
셋째, 브랜치를 만들고 병합하는 방법을 배우고요.
마지막으로 직접 실습을 통해 손에 익혀보겠습니다.

오늘 수업이 끝나면 git init부터 add, commit, status, log까지 기본 명령어를 자유롭게 사용할 수 있게 됩니다.
-->

---
layout: section
transition: fade
---

# 1. 버전관리란 무엇인가

<!-- [스크립트]
자, 그러면 첫 번째 주제로 들어가겠습니다.
버전관리란 무엇인지, 그리고 왜 개발자에게 필수인지 이야기해 보겠습니다.
-->

---
transition: slide-left
---

# 이런 경험, 있지 않나요?

<div class="mt-4 text-xl font-bold text-center text-gray-300">
파일 이름으로 버전 관리하기
</div>

<div class="flex justify-center mt-6 gap-3">

<v-clicks>

<div class="bg-gray-800 rounded-lg px-4 py-3 text-center">
  <div class="text-3xl mb-2">📄</div>
  <div class="text-sm">report_final.docx</div>
</div>

<div class="bg-gray-800 rounded-lg px-4 py-3 text-center">
  <div class="text-3xl mb-2">📄</div>
  <div class="text-sm">report_final_v2.docx</div>
</div>

<div class="bg-gray-800 rounded-lg px-4 py-3 text-center">
  <div class="text-3xl mb-2">📄</div>
  <div class="text-sm">report_진짜최종.docx</div>
</div>

<div class="bg-gray-800 rounded-lg px-4 py-3 text-center">
  <div class="text-3xl mb-2">📄</div>
  <div class="text-sm">report_최종_수정3.docx</div>
</div>

<div class="bg-red-900/40 rounded-lg px-4 py-3 text-center border border-red-500/50">
  <div class="text-3xl mb-2">❓</div>
  <div class="text-sm font-bold text-red-400">어떤 게 진짜?</div>
</div>

</v-clicks>

</div>

<div v-click class="mt-8 text-center text-lg">
코드에서는 <span class="text-red-400 font-bold">더 심각</span>하다 — 수정 후 원래대로 돌아갈 수 없다
</div>

<!-- [스크립트]
여러분, 이런 경험 한 번쯤 있으시죠?
보고서 작성할 때 "final"이라고 이름 붙였는데, 수정이 들어오면서 v2가 생기고, "진짜최종"이 생기고, "최종_수정3"까지...
결국 어떤 파일이 진짜 최종인지 모르게 됩니다.

문서도 이런데, 코드에서는 상황이 더 심각합니다.
잘 돌아가던 기능을 수정했다가, "아 원래 어떻게 되어 있었지?" 할 때 돌아갈 방법이 없는 거죠.
Ctrl+Z에도 한계가 있고, 파일을 저장하고 닫아버리면 끝입니다.

바로 이 문제를 해결하는 것이 버전관리 시스템, VCS입니다.
파일의 변경 이력을 체계적으로 기록해서, 언제든 과거 상태로 되돌릴 수 있게 해 줍니다.
-->

---
transition: slide-left
---

# 버전관리 = 게임 세이브

<div class="grid grid-cols-2 gap-8 mt-6">

<div>
<div class="text-center mb-4">
<span class="text-4xl">🎮</span>
<div class="text-lg font-bold mt-2">게임 세이브</div>
</div>

<v-clicks>

- 중요한 지점마다 **세이브**
- 실패하면 **세이브 포인트**로 복귀
- 여러 세이브 슬롯 관리

</v-clicks>

</div>

<div>
<div class="text-center mb-4">
<span class="text-4xl">💾</span>
<div class="text-lg font-bold mt-2">Git 커밋</div>
</div>

<v-clicks>

- 의미 있는 변경마다 **커밋**
- 문제 발생 시 **이전 커밋**으로 복구
- 브랜치로 **여러 갈래** 관리

</v-clicks>

</div>

</div>

<div v-click class="mt-6 p-3 bg-slate-800/50 rounded-lg text-center text-lg">
<strong>차이점</strong>: 게임 세이브는 혼자, Git은 <strong class="text-green-400">여러 사람이 동시에</strong> 세이브 + 합치기 가능
</div>

<!-- [스크립트]
버전관리를 쉽게 이해하기 위해 게임 세이브에 비유해 보겠습니다.

게임할 때 보스전 직전에 세이브하잖아요? 죽으면 그 세이브 포인트에서 다시 시작하고요.
슬롯을 여러 개 만들어서 각기 다른 진행 상태를 관리하기도 하죠.

Git 커밋이 바로 이 세이브와 같습니다.
코드에서 의미 있는 변경을 할 때마다 커밋하면, 문제가 생겼을 때 그 시점으로 돌아갈 수 있습니다.
그리고 브랜치라는 기능으로 여러 갈래의 작업을 동시에 관리할 수도 있고요.

다만 비유에는 한계가 있습니다.
게임 세이브는 혼자 쓰지만, Git은 여러 사람이 동시에 각자 세이브하고, 나중에 합칠 수 있다는 점이 다릅니다.
이게 바로 Git이 팀 협업에서 강력한 이유입니다.
-->

---
transition: slide-left
---

# VCS 비교: 왜 Git인가?

| 구분 | 파일 복사 | SVN (중앙집중) | **Git (분산)** |
|------|----------|---------------|---------------|
| 이력 관리 | 파일명 구분 | 중앙 서버 기록 | **로컬+원격** |
| 협업 | 충돌 빈발 | 서버 필수 | **오프라인 OK** |
| 속도 | - | 느림 | **빠름** |
| 복구 | 불가능 | 서버 의존 | **완전 복제** |

<v-clicks>

<div class="mt-4 p-3 bg-blue-900/30 rounded-lg">
<strong>핵심</strong>: Git은 로컬에 전체 이력을 가지므로 네트워크 없이도 커밋, 브랜치, 로그 확인이 가능
</div>

<div class="mt-2 p-3 bg-amber-900/30 rounded-lg">
💡 <strong>Git ≠ GitHub</strong>: Git은 도구, GitHub는 호스팅 서비스. Git 없이 GitHub 불가, GitHub 없이 Git 가능
</div>

</v-clicks>

<!-- [스크립트]
그러면 왜 하필 Git을 써야 할까요? 다른 방법과 비교해 보겠습니다.

표를 보시면, 파일 복사 방식은 아까 본 것처럼 이력 관리가 사실상 불가능하고 협업 시 충돌이 잦습니다.
SVN 같은 중앙집중형 VCS는 중앙 서버가 이력을 관리하지만, 서버에 연결되어 있어야만 작업할 수 있고 속도도 느립니다.
서버에 장애가 나면 전체 이력이 위험해지기도 하죠.

반면 Git은 분산형이라서 로컬에 전체 이력의 복제본을 가지고 있습니다.
그래서 네트워크 없이도 커밋, 브랜치 생성, 로그 확인이 전부 가능합니다.
속도도 로컬에서 처리하니까 빠르고, 모든 개발자의 복제본이 곧 백업이 되는 셈이라 복구도 안전합니다.

한 가지 꼭 구분해야 할 점이 있는데요.
Git과 GitHub는 다릅니다.
Git은 여러분 컴퓨터에서 돌아가는 버전관리 도구이고, GitHub는 Git 저장소를 온라인에 호스팅해주는 서비스입니다.
Git 없이 GitHub를 쓸 수는 없지만, GitHub 없이 Git만으로도 충분히 버전관리를 할 수 있습니다.
현재 업계 표준이 Git이기 때문에, 이번 수업에서는 Git을 중심으로 배워보겠습니다.
-->
