## 프론트엔드 교육 2: TypeScript + React 실무 과정 (1일 / 7시간)

| 시간 | 주제 | 세부 내용 | 실습 내용 | 비고 |
|---|---|---|---|---|
| 09:30-10:30 | TypeScript 핵심 기초 | - TypeScript의 필요성과 장점<br>- 기본 타입 (string, number, boolean)<br>- 배열, 객체 타입 정의<br>- 타입 추론과 명시적 타입 | - TypeScript 개발 환경 구축<br>- 기본 타입 선언 실습<br>- VS Code IntelliSense 활용 | |
| 10:30-11:40 | TypeScript 심화 타입 | - Interface와 Type Alias<br>- Union / Intersection 타입<br>- 제네릭 기초<br>- 유틸리티 타입 (Partial, Pick) | - 사용자 / 상품 인터페이스 정의<br>- 제네릭 함수 작성<br>- API 응답 타입 모델링 | |
| 11:40-13:00 | 점심시간 | - | - | |
| 13:00-14:00 | React + TypeScript 프로젝트 설정 | - CRA / Vite로 TS 프로젝트 생성<br>- 프로젝트 구조와 설정 파일<br>- Props / State 타입 정의 기초<br>- children 타입 처리 | - Vite + React + TS 프로젝트 생성<br>- 첫 번째 타입 안전 컴포넌트 작성<br>- Props 인터페이스 정의 | |
| 14:00-15:00 | 컴포넌트 타입 패턴 & Hooks | - 함수형 컴포넌트 타입 (FC vs 일반 함수)<br>- 이벤트 핸들러 타입<br>- DOM 요소 타입<br>- useState / useEffect 타입<br>- Custom Hook 타입 | - 버튼 / 입력 컴포넌트 타입 정의<br>- 폼 이벤트 핸들링<br>- 제네릭 Custom Hook 작성 | |
| 15:00-17:00 | 종합 실습: 타입 안전한 React 앱 | - 실무 프로젝트 타입 설계<br>- 컴포넌트 Props 설계 패턴<br>- 타입 가드 활용<br>- API 통신 타입 처리<br>- 디버깅 및 트러블슈팅 | - 타입 안전한 Todo 앱 구현<br>- API 연동 및 상태 관리 적용<br>- 전체 코드 타입 검증 | |
| 17:00-17:30 | 문제풀이 및 실습 | - 주요 개념 정리<br>- 자주 발생하는 타입 오류 분석<br>- 실무 Best Practice 공유 | - 코드 리뷰<br>- Q&A 및 추가 실습 | |


## 흐름
- TypeScript 문법 기초 및 핵심 (30분)
    - TypeScript for Java/C# Programmers(https://www.typescriptlang.org/docs/handbook/typescript-in-5-minutes-oop.html)
- TypeScript 문법 실습 (30분)
    - https://typescript-exercises.github.io
- React + TypeScript 프로젝트 설정 (1시간)
    - Vite로 TS 프로젝트 생성
    - 프로젝트 구조와 설정 파일
- React QuickStart (2시간)
    - QuickStart: Tic-Tac-Toe(https://react.dev/learn/tutorial-tic-tac-toe) (1시간/총2시간)
    - QuickStart: Thinking in React(https://react.dev/learn/thinking-in-react) (1시간/총2시간)
- 종합 실습: TypeScript + React 기반 Social-Dashboard 앱 구현 (2시간)
    - 필수 1먼저 앞에서 보여주고 나머지는 학생들이 직접 구현하도록 유도.
- 퀴즈 (30분)
    - 문제 10분, 퀴즈 5분

## 안내사항

- 수업의 목표는 1) 이미 개발자이지만 TypeScript와 React를 처음 배우는 학생들을 대상으로 React를 활용한 프론트엔드 개발의 감 익히기 2) 생성형 AI의 도움을 받아 웹사이트를 만들 때, 도움이 될만한 React(Front-end) 지식. 3) React로 개발할 때 알아야하는 깊지 않지만 필수적인 핵심 기능
- 따라서 마지막 종합 실습에서 진행할 투두앱을 만드는 데 필요한 개념들을 앞에서 빠짐 없이 설명하는 것이 매우 중요해.
- 가장 중요한 건 내가 TypeScript랑 React를 잘 몰라. 슬라이드의 발표자 대본을 정말 상세하게 작성해야해.
    - 슬라이드 발표자 대본에는 우리의 목표를 위해 지금 이 개념이 왜 중요하고 어떻게 쓰이는지, 개념을 일상 혹은 프론트엔드가 아닌 다른 개발과 비교하면 어떻게 비교할 수 있는지, 흔한 오해나 실수는 어떤 것들이 있는지 실제 스크립트를 있는 그대로 읽고 진행할 수 있는 수준으로 자세하게 작성해줘.
- 실습은 이미 social-dashboard-starter 폴더에 만들어 놨어.

## 상세내용
- TypeScript 문법 기초 및 핵심를 진행할 때는, 전체적으로 TypeScript 문법에 대해 설명을 하되 오늘 실습 및 목표로 한 것을 크게 벗어나는 내용까지는 다루지 않아도 괜찮아.
- https://typescript-exercises.github.io 해당 주소에서 실습을 진행할거야. 해당 실습을 진행할 수 있을 정도의 내용을 앞에서 다루도록 하고, 오늘의 목표를 넘어서는 실습까지는 진행하지 않는 분량 안에서만 풀 문제들을 선택해
- React + TypeScript 프로젝트 설정에서는 학생들이 Vite로 처음 프로젝트를 만들고 프로젝트를 구성하는 최소한의 구조를 이해하는 데 초점을 맞춰. 여기서 명령어나 코드 등을 상세하게 설명해주는 것이 좋아.
- React QuickStart에서는 React 공식 문서에서 이미 차근차근 잘 설명하고 있는 것들을 따와서 똑같이 잘 설명하는 가이드 문서로 작성하고, v-click을 적극적으로 사용한 슬라이드를 제작하는 것이 중요해. slidev의 코드 에니메이션을 적절하게 사용해. 학생들이 추가로 해볼 수 있는 퀴즈나 실습을 적절하게 고안하고 진행해
- 종합실습은 이미 만들어 놓았어. 해당 실습을 핵심 1은 앞에서 시연으로 보여줄거니까 과정을 상세하게 슬라이드로도 만들고, 중간중간 예시결과 같은 것도 잘 만들어
- 실습 코드를 직접 테스트해보고 PlayWright MCP로 캡쳐한 다음에 슬라이드에 넣는 것도 고려해.
- 퀴즈는 그냥 퀴즈시간이라고만 띄워놔.
- 기존에 guide 작성 스킬과 슬라이드 작성 스킬을 통한 가이드의 분량과 슬라이드 대본의 분량이 내 생각보다 너무 적었어. 정말 차근차근 설명해줘. 헷갈릴 수 있는 요소에 대해서도 미리미리 정리하고.