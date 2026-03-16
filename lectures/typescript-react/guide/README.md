# TypeScript + React 프론트엔드 교육 과정

## 과정 개요

| 항목 | 내용 |
|------|------|
| **과정명** | TypeScript + React 프론트엔드 개발 입문 |
| **기간** | 1일 (7시간) |
| **대상** | 프로그래밍 경험이 있는 개발자 (TypeScript/React 초심자) |
| **목표** | React 프론트엔드 개발의 핵심 개념 이해 + 생성형 AI 활용 시 도움될 React 지식 습득 |

## 시간표

| 시간 | 세션 | 내용 | 유형 |
|------|------|------|------|
| 09:30 - 10:00 | Session 1 | TypeScript 문법 기초 및 핵심 | 강의 |
| 10:00 - 10:30 | Session 2 | TypeScript 실습 (typescript-exercises) | 독립 실습 |
| 10:30 - 10:40 | - | 쉬는시간 | - |
| 10:40 - 11:40 | Session 3 | React + TypeScript 프로젝트 설정 | 강의 + Guided Coding |
| 11:40 - 13:00 | - | 점심시간 | - |
| 13:00 - 14:00 | Session 4-A | React QuickStart: Tic-Tac-Toe | Guided Coding |
| 14:00 - 15:00 | Session 4-B | React QuickStart: Thinking in React | Guided Coding |
| 15:00 - 17:00 | Session 5 | 종합 실습: Social Dashboard | I DO 시연 + YOU DO 독립 실습 |
| 17:00 - 17:30 | 퀴즈 | 문제풀이 및 마무리 | 퀴즈 |

> **시간 운영 참고**: Session 1과 Session 2는 유연한 60분 블록으로 운영합니다. TypeScript 기초 설명이 길어지면 실습 시간에서 흡수하고, 빠르게 진행되면 실습 시간을 늘립니다.

## 비율

- **순수 강의**: ~120분 (31.6%)
- **Guided Coding** (강사 따라 코딩): ~95분
- **독립 실습**: ~165분
- **실습 합계**: ~260분 (68.4%) → **30:70 원칙 충족**

## 세션별 학습 목표

### Session 1: TypeScript 문법 기초 (30분)
- TypeScript가 왜 필요한지 이해
- 기본 타입(`string`, `number`, `boolean`, `array`)
- Interface와 Type Alias
- Union 타입과 타입 좁히기
- 제네릭 문법 맛보기 (`useState<User[]>`)

### Session 2: TypeScript 실습 (30분)
- [typescript-exercises.github.io](https://typescript-exercises.github.io) Exercise 1~4 풀이
- 실전 타입 정의 연습

### Session 3: React + TypeScript 프로젝트 설정 (1시간)
- React의 핵심 개념 (컴포넌트, JSX, 선언적 UI)
- Vite로 React + TypeScript 프로젝트 생성
- 프로젝트 구조 이해 (main.tsx, App.tsx, tsconfig.json)
- 첫 번째 컴포넌트 작성 및 JSX 규칙

### Session 4: React QuickStart (2시간)
- **Part A - Tic-Tac-Toe** (1시간): React 공식 튜토리얼 따라하기
  - State, Props, 이벤트 핸들링
  - State 끌어올리기 (Lifting State Up)
  - 불변성과 배열 조작
- **Part B - Thinking in React** (1시간): React적 사고방식
  - 컴포넌트 계층 설계
  - 최소한의 State 식별
  - 역방향 데이터 흐름 (Callback Props)

### Session 5: 종합 실습 - Social Dashboard (2시간)
- JSONPlaceholder API를 활용한 대시보드 앱 구현
- Task 1 (강사 시연): 사용자 목록 불러오기 — `useState`, `useEffect`, `fetch`
- Task 2~6 (독립 실습): 게시글 CRUD, Todo 토글, 댓글 표시
- Challenge Task 7~11: Promise.all, useMemo, 앨범 갤러리

## 수강 전 준비사항

> **상세 설치 가이드**: [session0-setup.md](./session0-setup.md)에 Windows/Linux/macOS별 설치 과정이 스크린샷 수준으로 안내되어 있습니다. 수업 전에 반드시 확인해 주세요.

### 필수 설치
- **Node.js** 18 이상 ([다운로드](https://nodejs.org/))
- **VS Code** ([다운로드](https://code.visualstudio.com/))
- **터미널** (macOS Terminal, Windows PowerShell, 또는 VS Code 내장 터미널)

### 권장 VS Code 확장
- ESLint
- Prettier
- ES7+ React/Redux/React-Native snippets

### 설치 확인
```bash
node --version    # v18.0.0 이상
npm --version     # 9.0.0 이상
```

## 참고 자료

### TypeScript
- [TypeScript for Java/C# Programmers](https://www.typescriptlang.org/docs/handbook/typescript-in-5-minutes-oop.html)
- [TypeScript Exercises](https://typescript-exercises.github.io)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/)

### React
- [React 공식 튜토리얼: Tic-Tac-Toe](https://react.dev/learn/tutorial-tic-tac-toe)
- [Thinking in React](https://react.dev/learn/thinking-in-react)
- [React Quick Start](https://react.dev/learn)

### 실습 프로젝트
- [JSONPlaceholder API](https://jsonplaceholder.typicode.com) — 무료 가짜 REST API
- Social Dashboard Starter — `social-dashboard-starter/` 폴더 참조

## 파일 구조

```
typescript-react/
├── guide/
│   ├── README.md                      ← 현재 파일
│   ├── session0-setup.md              실습 환경 설정 가이드 (사전 준비)
│   ├── session1-ts-basics.md          TypeScript 기초
│   ├── session2-ts-exercises.md       TypeScript 실습
│   ├── session3-react-ts-setup.md     React+TS 프로젝트 설정
│   ├── session4-react-quickstart.md   React QuickStart
│   └── session5-social-dashboard.md   종합 실습
├── slides/
│   ├── slides.md                      slidev 슬라이드
│   ├── style.css                      커스텀 스타일
│   └── assets/                        이미지/스크린샷
├── labs/
│   └── social-dashboard/
│       └── README.md                  실습 가이드
└── social-dashboard-starter/          실습 코드 (Starter + Solutions)
```
