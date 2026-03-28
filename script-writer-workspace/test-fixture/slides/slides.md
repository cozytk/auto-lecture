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

---
layout: section
transition: fade
---

# 1. 버전관리란 무엇인가

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
