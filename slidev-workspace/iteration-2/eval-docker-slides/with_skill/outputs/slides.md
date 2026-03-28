---
theme: default
title: Docker 입문 - 컨테이너의 세계로
author: Docker Workshop
highlighter: shiki
lineNumbers: true
transition: slide-left
colorSchema: dark
canvasWidth: 980
fonts:
  sans: Pretendard
  mono: Fira Code
---

# Docker 입문

<div class="text-xl text-gray-400 mt-2">컨테이너의 세계로</div>

<div class="mt-12 flex gap-8 justify-center">
  <div v-click v-motion :initial="{ y: 40, opacity: 0 }" :enter="{ y: 0, opacity: 1, transition: { delay: 0 } }"
       class="text-center">
    <div class="text-4xl">📦</div>
    <div class="text-sm text-gray-400 mt-1">컨테이너</div>
  </div>
  <div v-click v-motion :initial="{ y: 40, opacity: 0 }" :enter="{ y: 0, opacity: 1, transition: { delay: 100 } }"
       class="text-center">
    <div class="text-4xl">🐳</div>
    <div class="text-sm text-gray-400 mt-1">Docker</div>
  </div>
  <div v-click v-motion :initial="{ y: 40, opacity: 0 }" :enter="{ y: 0, opacity: 1, transition: { delay: 200 } }"
       class="text-center">
    <div class="text-4xl">🚀</div>
    <div class="text-sm text-gray-400 mt-1">배포</div>
  </div>
</div>

<div class="abs-bl mx-14 my-12 text-sm text-gray-500">
  컨테이너 vs VM · Dockerfile · Docker Compose
</div>

<!--
Docker 입문 강의에 오신 것을 환영합니다. 오늘은 컨테이너 기술의 핵심인 Docker를 처음부터 차근차근 배워보겠습니다. 컨테이너란 무엇인지, VM과 어떻게 다른지, 그리고 실제로 Dockerfile과 Docker Compose를 사용하는 방법까지 다루겠습니다.
-->

---

# 왜 Docker인가?

<div class="mt-4 text-lg text-gray-300">개발자라면 한 번쯤 겪어본 문제들</div>

<div class="mt-6 space-y-3">

<div v-click class="flex items-start gap-3 bg-red-900/20 rounded-lg p-3 border-l-4 border-red-500">
  <span class="text-xl">⚠️</span>
  <div><strong>"내 컴퓨터에서는 되는데..."</strong> — 환경 차이로 인한 배포 실패</div>
</div>

<div v-click class="flex items-start gap-3 bg-red-900/20 rounded-lg p-3 border-l-4 border-red-500">
  <span class="text-xl">⚠️</span>
  <div><strong>서버 셋업에 반나절</strong> — Node, Python, DB 버전 맞추기 삽질</div>
</div>

<div v-click class="flex items-start gap-3 bg-red-900/20 rounded-lg p-3 border-l-4 border-red-500">
  <span class="text-xl">⚠️</span>
  <div><strong>의존성 충돌</strong> — 프로젝트 A는 Node 16, 프로젝트 B는 Node 20</div>
</div>

</div>

<div v-click class="mt-6 bg-green-900/30 rounded-lg p-4 text-center border border-green-500/30">
  <span class="text-xl">✅</span> <strong class="text-lg">Docker가 이 모든 문제를 해결합니다</strong>
</div>

<!--
여러분도 이런 경험 있으시죠? "내 컴퓨터에서는 되는데 왜 서버에서는 안 되지?" 서버 환경 셋업하는 데만 반나절이 걸리거나, 프로젝트마다 다른 버전의 런타임이 필요한 상황. Docker는 이런 문제를 깔끔하게 해결해줍니다.
-->

---
clicks: 3
---

# 컨테이너 vs 가상머신 (VM)

<div class="grid grid-cols-2 gap-6 mt-4">
  <!-- VM 아키텍처 -->
  <div>
    <div class="text-center mb-2 font-bold text-amber-400">가상머신 (VM)</div>
    <div class="bg-slate-800 rounded-xl p-3 flex flex-col gap-1.5">
      <div class="flex gap-1.5">
        <div class="flex-1 bg-amber-700/60 rounded p-1.5 text-center text-xs">
          <div class="font-bold">App A</div>
          <div class="bg-amber-900/50 rounded mt-1 p-1 text-[10px]">Libs/Bins</div>
          <div class="rounded mt-1 p-1 text-[10px] font-bold transition-all duration-300"
               :class="$clicks === 1 ? 'bg-red-600 ring-2 ring-red-400 scale-105' : 'bg-red-800/50'">Guest OS</div>
        </div>
        <div class="flex-1 bg-amber-700/60 rounded p-1.5 text-center text-xs">
          <div class="font-bold">App B</div>
          <div class="bg-amber-900/50 rounded mt-1 p-1 text-[10px]">Libs/Bins</div>
          <div class="rounded mt-1 p-1 text-[10px] font-bold transition-all duration-300"
               :class="$clicks === 1 ? 'bg-red-600 ring-2 ring-red-400 scale-105' : 'bg-red-800/50'">Guest OS</div>
        </div>
      </div>
      <div class="bg-amber-600/40 rounded p-2 text-center text-xs font-bold">Hypervisor</div>
      <div class="rounded p-2 text-center text-xs font-bold transition-all duration-300"
           :class="$clicks === 1 ? 'bg-green-700/50' : $clicks === 2 ? 'bg-green-600 ring-2 ring-green-400' : 'bg-green-700/50'">Host OS</div>
      <div class="bg-slate-700/60 rounded p-1.5 text-center text-xs">Infrastructure</div>
    </div>
  </div>

  <!-- Container 아키텍처 -->
  <div>
    <div class="text-center mb-2 font-bold text-blue-400">컨테이너 (Docker)</div>
    <div class="bg-slate-800 rounded-xl p-3 flex flex-col gap-1.5">
      <div class="flex gap-1.5">
        <div class="flex-1 bg-blue-700/60 rounded p-1.5 text-center text-xs">
          <div class="font-bold">App A</div>
          <div class="bg-blue-900/50 rounded mt-1 p-1 text-[10px]">Libs/Bins</div>
        </div>
        <div class="flex-1 bg-blue-700/60 rounded p-1.5 text-center text-xs">
          <div class="font-bold">App B</div>
          <div class="bg-blue-900/50 rounded mt-1 p-1 text-[10px]">Libs/Bins</div>
        </div>
        <div class="flex-1 bg-blue-700/60 rounded p-1.5 text-center text-xs">
          <div class="font-bold">App C</div>
          <div class="bg-blue-900/50 rounded mt-1 p-1 text-[10px]">Libs/Bins</div>
        </div>
      </div>
      <div class="text-center text-[10px] text-gray-500 transition-all duration-300"
           :class="$clicks === 1 ? '' : 'opacity-0'">← Guest OS 없음!</div>
      <div class="bg-blue-600/40 rounded p-2 text-center text-xs font-bold">Docker Engine</div>
      <div class="rounded p-2 text-center text-xs font-bold transition-all duration-300"
           :class="$clicks === 2 ? 'bg-green-600 ring-2 ring-green-400 scale-105' : 'bg-green-700/50'">Host OS (커널 공유)</div>
      <div class="bg-slate-700/60 rounded p-1.5 text-center text-xs">Infrastructure</div>
    </div>
  </div>
</div>

<!-- 하단 설명: 남은 여백을 활용하여 text-xl로 크게 -->
<div class="flex-1 flex items-center justify-center mt-4">
  <div class="bg-slate-800/50 rounded-lg p-4 text-center w-full">
    <div class="text-xl transition-all duration-300"
         :class="$clicks === 1 ? '' : 'opacity-0 h-0 overflow-hidden'">
      <strong class="text-amber-400">VM</strong>: 각 앱마다 <strong class="text-red-400">Guest OS 전체를 포함</strong> → 무겁고 느림
    </div>
    <div class="text-xl transition-all duration-300"
         :class="$clicks === 2 ? '' : 'opacity-0 h-0 overflow-hidden'">
      <strong class="text-blue-400">Container</strong>: <strong class="text-green-400">Host OS 커널 공유</strong> → 가볍고 빠름
    </div>
    <div class="text-xl transition-all duration-300"
         :class="$clicks >= 3 ? '' : 'opacity-0 h-0 overflow-hidden'">
      핵심: <strong>OS 커널 공유</strong> 덕분에 컨테이너는 훨씬 가볍고 빠르다
    </div>
    <div class="text-lg opacity-30 transition-all duration-300"
         :class="$clicks === 0 ? '' : 'opacity-0 h-0 overflow-hidden'">
      클릭하여 핵심 차이를 확인하세요
    </div>
  </div>
</div>

<!--
[click] VM은 각 앱마다 전체 Guest OS를 포함하기 때문에 무겁습니다. 하이퍼바이저가 하드웨어를 가상화합니다.
[click] 반면 컨테이너는 Host OS의 커널을 공유합니다. Guest OS가 없으니 훨씬 가볍죠. 같은 서버에 더 많은 앱을 올릴 수 있습니다.
[click] 핵심은 OS 커널 공유입니다. 이것이 컨테이너를 빠르고 가볍게 만드는 비결입니다.
-->

---

# VM vs 컨테이너 — 한눈에 비교

<div class="mt-6">

| 항목 | <span class="text-amber-400">VM</span> | <span class="text-blue-400">컨테이너</span> |
|------|-----|---------|
| **크기** | 수 GB | 수십~수백 MB |
| **시작 시간** | 수십 초~분 | <span v-mark.underline.blue="1">**수 초 이내**</span> |
| **격리 수준** | 강함 (OS 분리) | 프로세스 수준 |
| **리소스 효율** | 낮음 | <span v-mark.underline.blue="2">**높음**</span> |
| **이식성** | 낮음 | <span v-mark.underline.blue="3">**높음 (어디서든 동일)**</span> |

</div>

<div v-click class="mt-6 flex justify-center gap-8">
  <div v-motion :initial="{ scale: 0.8, opacity: 0 }" :enter="{ scale: 1, opacity: 1, transition: { type: 'spring', stiffness: 300 } }"
       class="text-center bg-blue-900/30 rounded-xl p-4 border border-blue-500/30">
    <span class="text-4xl font-bold text-blue-400">10x</span>
    <p class="text-gray-400 text-sm mt-1">더 빠른 시작</p>
  </div>
  <div v-motion :initial="{ scale: 0.8, opacity: 0 }" :enter="{ scale: 1, opacity: 1, transition: { type: 'spring', stiffness: 300, delay: 150 } }"
       class="text-center bg-green-900/30 rounded-xl p-4 border border-green-500/30">
    <span class="text-4xl font-bold text-green-400">5x</span>
    <p class="text-gray-400 text-sm mt-1">더 적은 리소스</p>
  </div>
  <div v-motion :initial="{ scale: 0.8, opacity: 0 }" :enter="{ scale: 1, opacity: 1, transition: { type: 'spring', stiffness: 300, delay: 300 } }"
       class="text-center bg-amber-900/30 rounded-xl p-4 border border-amber-500/30">
    <span class="text-4xl font-bold text-amber-400">100%</span>
    <p class="text-gray-400 text-sm mt-1">환경 일관성</p>
  </div>
</div>

<!--
표로 정리하면 차이가 명확합니다. 컨테이너는 시작이 빠르고, 리소스 효율이 높고, 어디서든 동일하게 동작합니다. 시작 속도는 VM 대비 10배 이상 빠르고, 리소스는 5배 이상 절약됩니다. 그리고 가장 중요한 것은 개발-스테이징-운영 환경이 100% 동일하다는 점입니다.
-->

---
clicks: 4
---

# Docker 핵심 구성 요소

<!-- 상단 흐름: Dockerfile → Image → Container -->
<div class="flex items-center justify-center gap-6 mt-12">
  <div class="transition-all duration-300"
       :class="$clicks === 1 ? 'ring-2 ring-sky-300 scale-110 rounded-xl' : $clicks >= 1 ? '' : 'opacity-40'">
    <div class="bg-sky-600 text-white px-6 py-4 rounded-xl font-bold shadow-lg text-lg">Dockerfile</div>
  </div>
  <div class="flex flex-col items-center text-gray-400">
    <div class="text-base font-bold">build</div>
    <div class="text-xl">→</div>
  </div>
  <div class="transition-all duration-300"
       :class="$clicks === 2 || $clicks >= 4 ? 'ring-2 ring-green-300 scale-110 rounded-xl' : $clicks >= 2 ? '' : 'opacity-40'">
    <div class="bg-green-600 text-white px-6 py-4 rounded-xl font-bold shadow-lg text-lg">Image</div>
  </div>
  <div class="flex flex-col items-center text-gray-400">
    <div class="text-base font-bold">run</div>
    <div class="text-xl">→</div>
  </div>
  <div class="transition-all duration-300"
       :class="$clicks === 3 ? 'ring-2 ring-amber-300 scale-110 rounded-xl' : $clicks >= 3 ? '' : 'opacity-40'">
    <div class="bg-amber-600 text-white px-6 py-4 rounded-xl font-bold shadow-lg text-lg">Container</div>
  </div>
</div>

<!-- Image ↔ Registry -->
<div class="flex flex-col items-center mt-4 transition-all duration-300"
     :class="$clicks >= 4 ? '' : 'opacity-30'">
  <div class="flex items-center gap-3 text-gray-400 text-base">
    <span class="font-bold">push ↓</span>
    <span class="font-bold">↑ pull</span>
  </div>
  <div :class="$clicks >= 4 ? 'ring-2 ring-purple-300 scale-105 rounded-xl' : ''"
       class="transition-all duration-300 mt-2">
    <div class="bg-purple-600 text-white px-6 py-4 rounded-xl font-bold shadow-lg text-lg">Registry</div>
  </div>
</div>

<!-- 설명: text-xl -->
<div class="mt-6 bg-slate-800/50 rounded-lg p-4 text-center">
  <div class="text-xl transition-all duration-300" :class="$clicks === 0 ? 'opacity-30' : 'opacity-0 h-0 overflow-hidden'">Docker의 핵심 구성 요소 4가지</div>
  <div class="text-xl transition-all duration-300" :class="$clicks === 1 ? '' : 'opacity-0 h-0 overflow-hidden'"><strong class="text-sky-400">Dockerfile</strong> — 이미지를 만들기 위한 <strong>설계도</strong></div>
  <div class="text-xl transition-all duration-300" :class="$clicks === 2 ? '' : 'opacity-0 h-0 overflow-hidden'"><strong class="text-green-400">Image</strong> — 실행 가능한 <strong>읽기 전용 패키지</strong></div>
  <div class="text-xl transition-all duration-300" :class="$clicks === 3 ? '' : 'opacity-0 h-0 overflow-hidden'"><strong class="text-amber-400">Container</strong> — Image의 <strong>실행 인스턴스</strong></div>
  <div class="text-xl transition-all duration-300" :class="$clicks >= 4 ? '' : 'opacity-0 h-0 overflow-hidden'"><strong class="text-purple-400">Registry</strong> — 이미지를 저장·공유하는 <strong>저장소</strong> (push/pull로 Image 교환)</div>
</div>

<!--
Docker의 네 가지 핵심 구성 요소를 하나씩 살펴보겠습니다.
[click] 첫 번째, Dockerfile은 이미지를 만들기 위한 설계도입니다. 어떤 베이스 이미지를 쓰고, 어떤 파일을 복사하고, 어떤 명령을 실행할지 적어둡니다.
[click] 두 번째, Image는 Dockerfile로 빌드한 결과물입니다. 읽기 전용 패키지로, OOP의 클래스에 비유할 수 있습니다.
[click] 세 번째, Container는 Image를 실행한 인스턴스입니다. 하나의 이미지로 여러 컨테이너를 만들 수 있습니다. OOP의 객체와 같습니다.
[click] 네 번째, Registry는 이미지를 저장하고 공유하는 곳입니다. Docker Hub가 대표적입니다.
-->

---
layout: section
---

# Dockerfile 기본 문법

<div class="text-gray-400 text-lg">이미지를 만드는 설계도 작성법</div>

<!--
이제 Dockerfile의 기본 문법을 배워보겠습니다. Dockerfile은 이미지를 만들기 위한 명세서입니다. 한 줄 한 줄이 이미지의 레이어가 됩니다.
-->

---
clicks: 5
---

# Dockerfile 핵심 명령어

```dockerfile {1|3|5|7|9}{lines:true}
FROM node:20-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .
```

<div class="mt-3 bg-slate-800/50 rounded-lg p-3 text-center">
  <div class="text-lg transition-all duration-300" :class="$clicks === 1 ? '' : 'opacity-0 h-0 overflow-hidden'">
    <strong>FROM</strong>: 베이스 이미지 지정 — 모든 Dockerfile의 시작점
  </div>
  <div class="text-lg transition-all duration-300" :class="$clicks === 2 ? '' : 'opacity-0 h-0 overflow-hidden'">
    <strong>WORKDIR</strong>: 컨테이너 내 작업 디렉토리 설정
  </div>
  <div class="text-lg transition-all duration-300" :class="$clicks === 3 ? '' : 'opacity-0 h-0 overflow-hidden'">
    <strong>COPY</strong>: 호스트 → 컨테이너로 파일 복사
  </div>
  <div class="text-lg transition-all duration-300" :class="$clicks === 4 ? '' : 'opacity-0 h-0 overflow-hidden'">
    <strong>RUN</strong>: 빌드 시 실행할 셸 명령어 (각 RUN = 새 레이어)
  </div>
  <div class="text-lg transition-all duration-300" :class="$clicks >= 5 ? '' : 'opacity-0 h-0 overflow-hidden'">
    <strong>COPY . .</strong>: 나머지 소스 전체 복사 (캐시 최적화!)
  </div>
</div>

<!--
Dockerfile의 핵심 명령어 5가지를 하나씩 보겠습니다.
[click] FROM은 베이스 이미지를 지정합니다. alpine은 5MB짜리 초경량 리눅스입니다.
[click] WORKDIR은 이후 명령이 실행될 작업 디렉토리를 설정합니다.
[click] COPY로 호스트의 파일을 컨테이너에 복사합니다. package*.json으로 package.json과 package-lock.json을 함께 복사합니다.
[click] RUN은 빌드 중에 실행할 명령입니다. npm install로 의존성을 설치합니다.
[click] 마지막으로 나머지 소스 코드를 복사합니다. package.json을 먼저 따로 복사한 이유는 Docker 레이어 캐시를 활용하기 위해서입니다.
-->

---
clicks: 3
---

# Dockerfile — EXPOSE & CMD

```dockerfile {1|3|5}{lines:true}
EXPOSE 3000

ENV NODE_ENV=production

CMD ["node", "server.js"]
```

<div class="mt-4 bg-slate-800/50 rounded-lg p-3 text-center">
  <div class="text-lg transition-all duration-300" :class="$clicks === 1 ? '' : 'opacity-0 h-0 overflow-hidden'">
    <strong>EXPOSE</strong>: 포트를 문서화 (실제 오픈은 <code>-p</code> 플래그로)
  </div>
  <div class="text-lg transition-all duration-300" :class="$clicks === 2 ? '' : 'opacity-0 h-0 overflow-hidden'">
    <strong>ENV</strong>: 환경 변수 설정 — 빌드 시점과 런타임 모두 적용
  </div>
  <div class="text-lg transition-all duration-300" :class="$clicks >= 3 ? '' : 'opacity-0 h-0 overflow-hidden'">
    <strong>CMD</strong>: 컨테이너 시작 시 기본 명령어. exec 형식(배열) 권장
  </div>
</div>

<div v-click class="mt-4 bg-amber-900/20 rounded-lg p-3 border-l-4 border-amber-500">
  <strong>TIP:</strong> <code>CMD</code>는 <code>docker run</code> 시 덮어쓸 수 있지만, <code>ENTRYPOINT</code>는 항상 실행
</div>

<!--
나머지 핵심 명령어 세 가지입니다.
[click] EXPOSE는 컨테이너가 리스닝할 포트를 문서화합니다. 실제 포트 바인딩은 docker run의 -p 플래그로 합니다.
[click] ENV는 환경 변수를 설정합니다. 빌드 시점과 런타임 모두에서 사용됩니다.
[click] CMD는 컨테이너가 시작될 때 실행할 기본 명령입니다. 배열 형태의 exec 형식을 쓰는 것이 권장됩니다.
[click] CMD와 ENTRYPOINT의 차이도 기억해두세요. CMD는 docker run에서 다른 명령으로 대체할 수 있습니다.
-->

---

# 완성된 Dockerfile 예시

<div class="grid grid-cols-[1fr,1fr] gap-4 mt-4">
<div>

```dockerfile {*}{lines:true,maxHeight:'340px'}
# 1단계: 빌드
FROM node:20-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# 2단계: 실행
FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package*.json ./
RUN npm ci --omit=dev
```

</div>
<div class="flex flex-col justify-center gap-3">

<div v-click class="bg-sky-900/30 rounded-lg p-3 border-l-4 border-sky-500 forward:delay-100">
  <div class="text-sm"><strong class="text-sky-400">멀티스테이지 빌드</strong></div>
  <div class="text-xs text-gray-400 mt-1">빌드 도구 없이 실행 이미지만 경량화</div>
</div>

<div v-click class="bg-green-900/30 rounded-lg p-3 border-l-4 border-green-500 forward:delay-200">
  <div class="text-sm"><strong class="text-green-400">npm ci</strong></div>
  <div class="text-xs text-gray-400 mt-1">lock 파일 기반 정확한 설치 (CI/CD용)</div>
</div>

<div v-click class="bg-amber-900/30 rounded-lg p-3 border-l-4 border-amber-500 forward:delay-300">
  <div class="text-sm"><strong class="text-amber-400">--omit=dev</strong></div>
  <div class="text-xs text-gray-400 mt-1">프로덕션 의존성만 설치 → 이미지 크기 절감</div>
</div>

</div>
</div>

<!--
실제 프로덕션에서 사용하는 멀티스테이지 빌드 Dockerfile입니다. 왼쪽 코드를 보면 두 단계로 나뉘어 있죠.
[click] 멀티스테이지 빌드는 빌드에 필요한 도구와 실행에 필요한 파일을 분리합니다. 최종 이미지에는 실행에 필요한 것만 들어갑니다.
[click] npm ci는 package-lock.json을 기반으로 정확하게 설치합니다. CI/CD 파이프라인에서 필수입니다.
[click] --omit=dev로 devDependencies를 제외하면 이미지 크기를 크게 줄일 수 있습니다.
-->

---
layout: section
---

# Docker CLI 기본 명령어

<div class="text-gray-400 text-lg">이미지 빌드부터 컨테이너 실행까지</div>

<!--
이제 실제로 Docker를 사용하는 CLI 명령어를 배워보겠습니다. 이미지를 빌드하고, 컨테이너를 실행하고, 관리하는 방법을 다루겠습니다.
-->

---
clicks: 3
---

# docker build & run

<div class="grid grid-cols-[1fr,1fr] gap-6 mt-4">
<div>

```bash {1|2|3}
docker build -t myapp:1.0 .
docker run -d -p 3000:3000 --name web myapp:1.0
docker ps
```

</div>
<div class="flex items-center">
  <div class="bg-slate-800/50 rounded-lg p-4 w-full">
    <div class="transition-all duration-300" :class="$clicks === 1 ? '' : 'opacity-0 h-0 overflow-hidden'"><strong>build</strong>: Dockerfile → 이미지 생성<br/><code>-t</code> 이름:태그, <code>.</code> 빌드 컨텍스트</div>
    <div class="transition-all duration-300" :class="$clicks === 2 ? '' : 'opacity-0 h-0 overflow-hidden'"><strong>run</strong>: 이미지 → 컨테이너 실행<br/><code>-d</code> 백그라운드, <code>-p</code> 포트 매핑</div>
    <div class="transition-all duration-300" :class="$clicks >= 3 ? '' : 'opacity-0 h-0 overflow-hidden'"><strong>ps</strong>: 실행 중 컨테이너 목록<br/><code>-a</code>로 중지된 것도 확인</div>
  </div>
</div>
</div>


<!--
가장 기본적인 세 가지 명령입니다.
[click] docker build는 Dockerfile을 읽어서 이미지를 만듭니다. -t로 이름과 태그를 지정하고, 마지막 점은 빌드 컨텍스트 경로입니다.
[click] docker run은 이미지에서 컨테이너를 만들어 실행합니다. -d는 백그라운드, -p는 호스트포트:컨테이너포트 매핑입니다.
[click] docker ps로 실행 중인 컨테이너를 확인합니다. -a를 붙이면 중지된 컨테이너도 볼 수 있습니다.
[click] 실행 결과는 이렇게 보입니다. 컨테이너 ID, 이미지, 상태, 포트 매핑, 이름이 표시됩니다.
-->

---

# 컨테이너 관리 명령어

<div class="mt-4">

<v-clicks>

<div class="flex items-center gap-3 bg-slate-800/50 rounded-lg p-3 mb-2">
  <code class="text-white text-sm font-mono w-56">docker stop web</code>
  <span class="text-gray-400 text-sm">— 컨테이너 정상 종료 (SIGTERM → SIGKILL)</span>
</div>

<div class="flex items-center gap-3 bg-slate-800/50 rounded-lg p-3 mb-2">
  <code class="text-white text-sm font-mono w-56">docker start web</code>
  <span class="text-gray-400 text-sm">— 중지된 컨테이너 재시작</span>
</div>

<div class="flex items-center gap-3 bg-slate-800/50 rounded-lg p-3 mb-2">
  <code class="text-white text-sm font-mono w-56">docker logs -f web</code>
  <span class="text-gray-400 text-sm">— 컨테이너 로그 실시간 확인 (<code>-f</code> = follow)</span>
</div>

<div class="flex items-center gap-3 bg-slate-800/50 rounded-lg p-3 mb-2">
  <code class="text-white text-sm font-mono w-56">docker exec -it web sh</code>
  <span class="text-gray-400 text-sm">— 실행 중인 컨테이너에 셸 접속</span>
</div>

<div class="flex items-center gap-3 bg-slate-800/50 rounded-lg p-3 mb-2">
  <code class="text-white text-sm font-mono w-56">docker rm -f web</code>
  <span class="text-gray-400 text-sm">— ⚠️ 컨테이너 강제 삭제 (<code>-f</code> = force)</span>
</div>

</v-clicks>

</div>

<!--
컨테이너를 관리하는 명령어들입니다.
[click] docker stop은 컨테이너를 정상 종료합니다. 먼저 SIGTERM을 보내고, 10초 뒤에 SIGKILL로 강제 종료합니다.
[click] docker start는 중지된 컨테이너를 다시 시작합니다.
[click] docker logs로 컨테이너의 로그를 확인합니다. -f 옵션을 붙이면 실시간으로 스트리밍됩니다.
[click] docker exec로 실행 중인 컨테이너 안에 들어갈 수 있습니다. -it은 인터랙티브 터미널을 의미합니다.
[click] docker rm으로 컨테이너를 삭제합니다. -f를 붙이면 실행 중이어도 강제 삭제합니다.
-->

---
layout: section
---

# Docker Compose

<div class="text-gray-400 text-lg">여러 컨테이너를 한 번에 관리하기</div>

<!--
실제 애플리케이션은 웹서버, 데이터베이스, 캐시 등 여러 컨테이너가 함께 동작합니다. Docker Compose는 이런 멀티 컨테이너 환경을 하나의 YAML 파일로 정의하고 관리할 수 있게 해줍니다.
-->

---

# Docker Compose가 필요한 이유

<v-switch>
  <template #1>
    <div class="mt-4">
      <div class="text-lg font-bold text-red-400 mb-4">Without Compose — 명령어 지옥</div>

```bash {*}{maxHeight:'260px'}
# 네트워크 생성
docker network create myapp-net
# DB 실행
docker run -d --name db --network myapp-net \
  -e POSTGRES_PASSWORD=secret postgres:16
# Redis 실행
docker run -d --name cache --network myapp-net redis:7
# App 실행
docker run -d --name app --network myapp-net \
  -p 3000:3000 -e DB_HOST=db myapp:1.0
```

  <div class="mt-3 text-sm text-red-400">매번 이 명령들을 순서대로 입력해야 한다...</div>
    </div>
  </template>
  <template #2>
    <div class="mt-4">
      <div class="text-lg font-bold text-green-400 mb-4">With Compose — 파일 하나로 끝</div>

```bash
docker compose up -d    # 끝! 🎉
```

  <div class="mt-4 bg-green-900/20 rounded-lg p-4 border border-green-500/30">
    <div class="flex items-center gap-6 justify-center">
      <div class="text-center">
        <div class="text-2xl font-bold text-green-400">1개 파일</div>
        <div class="text-xs text-gray-400">docker-compose.yml</div>
      </div>
      <div class="text-center">
        <div class="text-2xl font-bold text-green-400">1줄 명령</div>
        <div class="text-xs text-gray-400">docker compose up</div>
      </div>
      <div class="text-center">
        <div class="text-2xl font-bold text-green-400">전체 관리</div>
        <div class="text-xs text-gray-400">네트워크 + 볼륨 자동</div>
      </div>
    </div>
  </div>
    </div>
  </template>
</v-switch>

<!--
왜 Docker Compose가 필요할까요?
[click] Compose 없이 여러 컨테이너를 띄우려면 이렇게 긴 명령어를 순서대로 입력해야 합니다. 네트워크도 직접 만들고, 환경 변수도 하나하나 지정해야 합니다.
[click] Compose를 쓰면? docker-compose.yml 파일 하나에 모든 서비스를 정의하고, 명령어 한 줄로 전체를 시작할 수 있습니다. 네트워크와 볼륨도 자동으로 관리됩니다.
-->

---
clicks: 4
---

# docker-compose.yml 구조

<div class="grid grid-cols-[1fr,1fr] gap-4 mt-2">
<div>

```yaml {1-2|3-8|9-13|14-16}{lines:true}
services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - DB_HOST=db
    depends_on: [db]

  db:
    image: postgres:16
    environment:
      - POSTGRES_PASSWORD=secret

    volumes:
      - db-data:/var/lib/postgresql/data
```

</div>
<div class="flex items-center">
  <div class="bg-slate-800/50 rounded-lg p-4 w-full">
    <div class="transition-all duration-300" :class="$clicks === 1 ? '' : 'opacity-0 h-0 overflow-hidden'"><strong>services</strong>: 실행할 컨테이너 정의<br/>각 서비스 = 하나의 컨테이너</div>
    <div class="transition-all duration-300" :class="$clicks === 2 ? '' : 'opacity-0 h-0 overflow-hidden'"><strong>app 서비스</strong>: 로컬 Dockerfile 빌드<br/>포트 매핑 + 환경 변수 + 의존성 순서</div>
    <div class="transition-all duration-300" :class="$clicks === 3 ? '' : 'opacity-0 h-0 overflow-hidden'"><strong>db 서비스</strong>: Docker Hub 이미지 직접 사용<br/>환경 변수로 비밀번호 설정</div>
    <div class="transition-all duration-300" :class="$clicks >= 4 ? '' : 'opacity-0 h-0 overflow-hidden'"><strong>volumes</strong>: DB 데이터 영구 저장<br/>컨테이너 삭제돼도 데이터 유지</div>
  </div>
</div>
</div>

<!--
docker-compose.yml의 기본 구조입니다.
[click] 최상위에 services 키 아래 실행할 컨테이너들을 정의합니다.
[click] app 서비스는 현재 디렉토리의 Dockerfile로 빌드합니다. 포트 매핑, 환경 변수, depends_on으로 DB 시작 후 app을 시작하도록 설정했습니다.
[click] db 서비스는 Docker Hub의 postgres:16 이미지를 바로 사용합니다. image를 직접 지정하면 build 없이 바로 실행됩니다.
[click] volumes로 데이터를 영구 저장합니다. 컨테이너를 삭제하고 다시 만들어도 데이터가 유지됩니다.
-->

---

# Compose 실전: 3-Tier 웹 앱

```yaml {*}{lines:true,maxHeight:'380px'}
services:
  frontend:
    build: ./frontend
    ports: ["3000:3000"]
    depends_on: [backend]

  backend:
    build: ./backend
    ports: ["8080:8080"]
    environment:
      - DATABASE_URL=postgres://user:pass@db:5432/mydb
      - REDIS_URL=redis://cache:6379
    depends_on: [db, cache]

  db:
    image: postgres:16-alpine
    volumes: [db-data:/var/lib/postgresql/data]
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass

  cache:
    image: redis:7-alpine

volumes:
  db-data:
```

<div v-click class="mt-2 bg-slate-800/50 rounded-lg p-2 text-sm text-center">
  <code class="text-green-400">docker compose up -d</code> → Frontend + Backend + PostgreSQL + Redis 전부 한 번에 실행
</div>

<!--
실전에서 자주 사용하는 3-Tier 아키텍처 예시입니다. 프론트엔드, 백엔드, 데이터베이스, 캐시 총 4개의 서비스를 하나의 파일로 관리합니다. depends_on으로 시작 순서를 제어하고, 서비스 이름(db, cache)이 자동으로 DNS 이름이 됩니다. docker compose up -d 한 줄이면 전부 실행됩니다.
-->

---

# Compose CLI 명령어

<div class="mt-4">

<v-clicks>

<div class="flex items-center gap-3 bg-slate-800/50 rounded-lg p-3 mb-2">
  <code class="text-white text-sm font-mono w-64">docker compose up -d</code>
  <span class="text-gray-400 text-sm">— 모든 서비스 백그라운드 시작</span>
</div>

<div class="flex items-center gap-3 bg-slate-800/50 rounded-lg p-3 mb-2">
  <code class="text-white text-sm font-mono w-64">docker compose down</code>
  <span class="text-gray-400 text-sm">— 모든 서비스 중지 + 컨테이너 삭제</span>
</div>

<div class="flex items-center gap-3 bg-slate-800/50 rounded-lg p-3 mb-2">
  <code class="text-white text-sm font-mono w-64">docker compose logs -f backend</code>
  <span class="text-gray-400 text-sm">— 특정 서비스 로그 실시간 확인</span>
</div>

<div class="flex items-center gap-3 bg-slate-800/50 rounded-lg p-3 mb-2">
  <code class="text-white text-sm font-mono w-64">docker compose ps</code>
  <span class="text-gray-400 text-sm">— Compose로 관리 중인 컨테이너 상태</span>
</div>

<div class="flex items-center gap-3 bg-slate-800/50 rounded-lg p-3 mb-2">
  <code class="text-white text-sm font-mono w-64">docker compose down -v</code>
  <span class="text-gray-400 text-sm">— ⚠️ 컨테이너 + <strong>볼륨까지</strong> 삭제 (데이터 초기화)</span>
</div>

</v-clicks>

</div>

<!--
Compose의 주요 CLI 명령어입니다.
[click] up -d로 모든 서비스를 백그라운드에서 시작합니다.
[click] down으로 모든 컨테이너를 중지하고 삭제합니다. 네트워크도 함께 정리됩니다.
[click] logs로 특정 서비스의 로그를 확인할 수 있습니다.
[click] ps로 Compose가 관리하는 컨테이너 상태를 봅니다.
[click] down -v는 볼륨까지 삭제하므로 주의해야 합니다. DB 데이터가 완전히 초기화됩니다.
-->

---
clicks: 4
---

# Docker 개발 워크플로우

<div class="flex items-center justify-center gap-4 mt-10">
  <div class="transition-all duration-300"
       :class="$clicks === 1 ? 'ring-2 ring-sky-300 scale-105 rounded-xl' : $clicks >= 1 ? '' : 'opacity-40'">
    <div class="bg-sky-600 text-white px-5 py-3 rounded-xl font-bold shadow-lg text-center">
      <div>1. Write</div>
      <div class="text-xs font-normal mt-1">Dockerfile 작성</div>
    </div>
  </div>

  <div class="text-xl opacity-30">→</div>

  <div class="transition-all duration-300"
       :class="$clicks === 2 ? 'ring-2 ring-green-300 scale-105 rounded-xl' : $clicks >= 2 ? '' : 'opacity-40'">
    <div class="bg-green-600 text-white px-5 py-3 rounded-xl font-bold shadow-lg text-center">
      <div>2. Build</div>
      <div class="text-xs font-normal mt-1">docker build</div>
    </div>
  </div>

  <div class="text-xl opacity-30">→</div>

  <div class="transition-all duration-300"
       :class="$clicks === 3 ? 'ring-2 ring-amber-300 scale-105 rounded-xl' : $clicks >= 3 ? '' : 'opacity-40'">
    <div class="bg-amber-600 text-white px-5 py-3 rounded-xl font-bold shadow-lg text-center">
      <div>3. Run</div>
      <div class="text-xs font-normal mt-1">docker run</div>
    </div>
  </div>

  <div class="text-xl opacity-30">→</div>

  <div class="transition-all duration-300"
       :class="$clicks >= 4 ? 'ring-2 ring-purple-300 scale-105 rounded-xl' : 'opacity-40'">
    <div class="bg-purple-600 text-white px-5 py-3 rounded-xl font-bold shadow-lg text-center">
      <div>4. Share</div>
      <div class="text-xs font-normal mt-1">docker push</div>
    </div>
  </div>
</div>

<div class="mt-8 bg-slate-800/50 rounded-lg p-4 text-center min-h-14 relative overflow-hidden">
  <div class="transition-all duration-300 absolute inset-0 flex items-center justify-center"
       :class="$clicks === 1 ? 'opacity-100' : 'opacity-0 pointer-events-none'">
    <strong class="text-sky-400">Write</strong>: 앱 코드와 Dockerfile을 작성한다
  </div>
  <div class="transition-all duration-300 absolute inset-0 flex items-center justify-center"
       :class="$clicks === 2 ? 'opacity-100' : 'opacity-0 pointer-events-none'">
    <strong class="text-green-400">Build</strong>: Dockerfile → Image로 빌드한다
  </div>
  <div class="transition-all duration-300 absolute inset-0 flex items-center justify-center"
       :class="$clicks === 3 ? 'opacity-100' : 'opacity-0 pointer-events-none'">
    <strong class="text-amber-400">Run</strong>: Image → Container로 실행하고 테스트한다
  </div>
  <div class="transition-all duration-300 absolute inset-0 flex items-center justify-center"
       :class="$clicks >= 4 ? 'opacity-100' : 'opacity-0 pointer-events-none'">
    <strong class="text-purple-400">Share</strong>: 검증된 이미지를 Registry에 푸시하여 팀과 공유
  </div>
  <div class="invisible">placeholder</div>
</div>

<!--
Docker를 사용한 개발 워크플로우는 4단계 사이클입니다.
[click] 먼저 애플리케이션 코드와 Dockerfile을 작성합니다.
[click] docker build로 이미지를 빌드합니다.
[click] docker run이나 compose up으로 실행하고 테스트합니다.
[click] 검증이 끝나면 docker push로 Registry에 업로드하여 팀원들과 공유합니다. 이 사이클을 반복하면서 개발합니다.
-->

---

# 오늘 배운 것 정리

<div class="grid grid-cols-3 gap-4 mt-6">

<div v-click class="bg-slate-800/50 rounded-xl p-4 border border-sky-500/30 forward:delay-100">
  <div class="text-sky-400 font-bold text-lg mb-2">컨테이너 vs VM</div>
  <div class="text-sm space-y-1 text-gray-300">
    <div>• OS 커널 공유로 경량화</div>
    <div>• 수 초 내 시작</div>
    <div>• 환경 100% 일관성</div>
  </div>
</div>

<div v-click class="bg-slate-800/50 rounded-xl p-4 border border-green-500/30 forward:delay-200">
  <div class="text-green-400 font-bold text-lg mb-2">Dockerfile</div>
  <div class="text-sm space-y-1 text-gray-300">
    <div>• FROM → WORKDIR → COPY</div>
    <div>• RUN → EXPOSE → CMD</div>
    <div>• 멀티스테이지 빌드</div>
  </div>
</div>

<div v-click class="bg-slate-800/50 rounded-xl p-4 border border-purple-500/30 forward:delay-300">
  <div class="text-purple-400 font-bold text-lg mb-2">Docker Compose</div>
  <div class="text-sm space-y-1 text-gray-300">
    <div>• YAML로 멀티 컨테이너 정의</div>
    <div>• <code class="text-xs">docker compose up -d</code></div>
    <div>• 네트워크/볼륨 자동 관리</div>
  </div>
</div>

</div>

<div v-click class="mt-6 bg-blue-900/20 rounded-xl p-4 border border-blue-500/30 text-center">
  <div class="text-lg"><strong class="text-blue-400">핵심 메시지</strong>: Docker는 <span v-mark.underline.blue="5">"어디서든 동일하게 동작"</span>하는 환경을 보장합니다</div>
</div>

<!--
오늘 배운 내용을 정리하겠습니다.
[click] 첫째, 컨테이너가 VM과 어떻게 다른지 배웠습니다. OS 커널을 공유하기 때문에 가볍고 빠릅니다.
[click] 둘째, Dockerfile의 핵심 명령어를 배웠습니다. FROM부터 CMD까지, 그리고 멀티스테이지 빌드까지.
[click] 셋째, Docker Compose로 여러 컨테이너를 하나의 YAML 파일로 관리하는 방법을 배웠습니다.
[click] Docker의 핵심 가치는 "어디서든 동일하게 동작"하는 환경을 보장하는 것입니다. 개발, 테스트, 운영 환경이 모두 같아집니다.
-->

---
layout: end
---

# 감사합니다

<div class="text-gray-400 mt-2">질문이 있으신가요?</div>

<div class="mt-8 text-sm text-gray-500">
  <div>Docker 공식 문서: <a href="https://docs.docker.com" class="text-blue-400">docs.docker.com</a></div>
  <div class="mt-1">Docker Hub: <a href="https://hub.docker.com" class="text-blue-400">hub.docker.com</a></div>
</div>

<!--
오늘 Docker 입문 강의는 여기까지입니다. 질문이 있으시면 편하게 물어봐주세요. Docker 공식 문서도 참고하시면 좋습니다. 감사합니다.
-->
