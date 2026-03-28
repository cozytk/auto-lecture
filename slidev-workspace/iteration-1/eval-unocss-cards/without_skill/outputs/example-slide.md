---
theme: default
title: UnoCSS 카드 레이아웃 예제
colorSchema: dark
---

# UnoCSS 카드 레이아웃 패턴

다크 배경 + 둥근 모서리 + 그림자 + v-click 애니메이션

---
class: bg-slate-900
---

# 패턴 1: 기본 3열 카드

<div class="grid grid-cols-3 gap-6 mt-8">
  <div v-click class="bg-slate-700 rounded-xl shadow-lg p-6">
    <h3 class="text-blue-400 text-xl font-bold mb-2">설계</h3>
    <p class="text-gray-300 text-sm">요구사항을 분석하고 아키텍처를 설계합니다</p>
  </div>

  <div v-click class="bg-slate-700 rounded-xl shadow-lg p-6">
    <h3 class="text-green-400 text-xl font-bold mb-2">구현</h3>
    <p class="text-gray-300 text-sm">설계를 바탕으로 코드를 작성합니다</p>
  </div>

  <div v-click class="bg-slate-700 rounded-xl shadow-lg p-6">
    <h3 class="text-purple-400 text-xl font-bold mb-2">배포</h3>
    <p class="text-gray-300 text-sm">자동화된 파이프라인으로 배포합니다</p>
  </div>
</div>

---
class: bg-slate-900
---

# 패턴 2: 테두리 강조 카드 + 호버 효과

<div class="grid grid-cols-3 gap-6 mt-8">
  <div v-click class="bg-slate-800 rounded-2xl shadow-xl p-6 border border-slate-700 hover:border-blue-500 transition-all duration-300">
    <div class="text-3xl mb-3">🚀</div>
    <h3 class="text-blue-400 text-lg font-bold mb-2">빠른 시작</h3>
    <p class="text-gray-400 text-sm">5분 안에 프로젝트를 시작할 수 있습니다</p>
  </div>

  <div v-click class="bg-slate-800 rounded-2xl shadow-xl p-6 border border-slate-700 hover:border-green-500 transition-all duration-300">
    <div class="text-3xl mb-3">🔧</div>
    <h3 class="text-green-400 text-lg font-bold mb-2">간편 설정</h3>
    <p class="text-gray-400 text-sm">YAML 설정 하나로 모든 것을 관리합니다</p>
  </div>

  <div v-click class="bg-slate-800 rounded-2xl shadow-xl p-6 border border-slate-700 hover:border-purple-500 transition-all duration-300">
    <div class="text-3xl mb-3">📦</div>
    <h3 class="text-purple-400 text-lg font-bold mb-2">확장 가능</h3>
    <p class="text-gray-400 text-sm">플러그인으로 기능을 자유롭게 확장합니다</p>
  </div>
</div>

---
class: bg-slate-900
---

# 패턴 3: 2열 대형 카드

<div class="grid grid-cols-2 gap-8 mt-6">
  <div v-click class="bg-slate-800 rounded-2xl shadow-2xl p-8 border border-slate-700">
    <h3 class="text-cyan-400 text-2xl font-bold mb-4">Frontend</h3>
    <ul class="text-gray-300 text-sm space-y-2">
      <li>React / Vue / Svelte</li>
      <li>TypeScript 기반 개발</li>
      <li>컴포넌트 기반 아키텍처</li>
      <li>상태 관리 패턴</li>
    </ul>
  </div>

  <div v-click class="bg-slate-800 rounded-2xl shadow-2xl p-8 border border-slate-700">
    <h3 class="text-orange-400 text-2xl font-bold mb-4">Backend</h3>
    <ul class="text-gray-300 text-sm space-y-2">
      <li>Node.js / Go / Python</li>
      <li>REST API / GraphQL</li>
      <li>마이크로서비스 아키텍처</li>
      <li>데이터베이스 설계</li>
    </ul>
  </div>
</div>

---
class: bg-slate-900
---

# 패턴 4: 왼쪽 강조 테두리 카드 (세로 배치)

<div class="space-y-4 mt-6 max-w-2xl mx-auto">
  <div v-click class="bg-slate-800 rounded-lg shadow-lg p-5 border-l-4 border-blue-500">
    <h3 class="text-white text-lg font-bold mb-1">1단계: 환경 설정</h3>
    <p class="text-gray-400 text-sm">Docker와 Kubernetes 클러스터를 로컬에 구성합니다</p>
  </div>

  <div v-click class="bg-slate-800 rounded-lg shadow-lg p-5 border-l-4 border-green-500">
    <h3 class="text-white text-lg font-bold mb-1">2단계: 애플리케이션 배포</h3>
    <p class="text-gray-400 text-sm">컨테이너 이미지를 빌드하고 클러스터에 배포합니다</p>
  </div>

  <div v-click class="bg-slate-800 rounded-lg shadow-lg p-5 border-l-4 border-yellow-500">
    <h3 class="text-white text-lg font-bold mb-1">3단계: 모니터링 구성</h3>
    <p class="text-gray-400 text-sm">Prometheus와 Grafana로 모니터링 대시보드를 구축합니다</p>
  </div>

  <div v-click class="bg-slate-800 rounded-lg shadow-lg p-5 border-l-4 border-red-500">
    <h3 class="text-white text-lg font-bold mb-1">4단계: 자동 스케일링</h3>
    <p class="text-gray-400 text-sm">HPA를 설정하여 트래픽에 따라 자동으로 확장합니다</p>
  </div>
</div>

---
class: bg-slate-900
---

# 패턴 5: 글래스모피즘 카드

<div class="grid grid-cols-3 gap-6 mt-8">
  <div v-click class="bg-white/5 backdrop-blur-md rounded-xl shadow-lg p-6 border border-white/10 hover:bg-white/10 transition-all duration-300">
    <h3 class="text-white text-lg font-bold mb-2">투명 효과</h3>
    <p class="text-gray-300 text-sm">배경이 비치는 글래스모피즘 스타일의 카드입니다</p>
  </div>

  <div v-click class="bg-white/5 backdrop-blur-md rounded-xl shadow-lg p-6 border border-white/10 hover:bg-white/10 transition-all duration-300">
    <h3 class="text-white text-lg font-bold mb-2">모던 디자인</h3>
    <p class="text-gray-300 text-sm">최신 UI 트렌드를 반영한 세련된 카드 스타일입니다</p>
  </div>

  <div v-click class="bg-white/5 backdrop-blur-md rounded-xl shadow-lg p-6 border border-white/10 hover:bg-white/10 transition-all duration-300">
    <h3 class="text-white text-lg font-bold mb-2">가벼운 느낌</h3>
    <p class="text-gray-300 text-sm">반투명 효과로 시각적 무게를 줄인 디자인입니다</p>
  </div>
</div>

---
class: bg-slate-900
---

# 패턴 6: 그라데이션 배경 카드

<div class="grid grid-cols-2 gap-8 mt-8">
  <div v-click class="bg-gradient-to-br from-blue-900/50 to-slate-800 rounded-2xl shadow-xl p-8 border border-blue-800/30">
    <h3 class="text-blue-300 text-xl font-bold mb-3">클라우드 네이티브</h3>
    <p class="text-gray-300 text-sm">컨테이너화, 오케스트레이션, 서비스 메시 등 클라우드 네이티브 기술 스택을 학습합니다</p>
  </div>

  <div v-click class="bg-gradient-to-br from-purple-900/50 to-slate-800 rounded-2xl shadow-xl p-8 border border-purple-800/30">
    <h3 class="text-purple-300 text-xl font-bold mb-3">DevOps 실천</h3>
    <p class="text-gray-300 text-sm">CI/CD 파이프라인, IaC, 모니터링 등 DevOps 문화와 도구를 실습합니다</p>
  </div>
</div>

---
class: bg-slate-900
---

# 패턴 7: 숫자 순서 카드 + v-click 순서 지정

<div class="grid grid-cols-4 gap-4 mt-8">
  <div v-click="1" class="bg-slate-800 rounded-xl shadow-lg p-5 border border-slate-700 text-center">
    <div class="text-blue-400 text-4xl font-black mb-2">01</div>
    <h3 class="text-white text-sm font-bold">계획</h3>
  </div>

  <div v-click="2" class="bg-slate-800 rounded-xl shadow-lg p-5 border border-slate-700 text-center">
    <div class="text-green-400 text-4xl font-black mb-2">02</div>
    <h3 class="text-white text-sm font-bold">개발</h3>
  </div>

  <div v-click="3" class="bg-slate-800 rounded-xl shadow-lg p-5 border border-slate-700 text-center">
    <div class="text-yellow-400 text-4xl font-black mb-2">03</div>
    <h3 class="text-white text-sm font-bold">테스트</h3>
  </div>

  <div v-click="4" class="bg-slate-800 rounded-xl shadow-lg p-5 border border-slate-700 text-center">
    <div class="text-red-400 text-4xl font-black mb-2">04</div>
    <h3 class="text-white text-sm font-bold">릴리스</h3>
  </div>
</div>

<div v-click="5" class="mt-8 bg-blue-900/30 rounded-xl p-4 border border-blue-700/50 text-center">
  <p class="text-blue-300 text-lg font-bold">반복적 개선을 통해 품질을 높입니다</p>
</div>
