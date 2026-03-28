# Day 2 Session 0: Langfuse 셀프 호스팅

> **20분** | 00_basics 실습 전 환경 준비

<callout icon="📖" color="blue_bg">
	**학습 목표**
	1. LLM Observability의 필요성을 이해한다
	2. Docker Compose로 Langfuse를 로컬에서 실행할 수 있다
	3. API 키를 발급하고 .env에 설정할 수 있다
</callout>

---

## 왜 Docker를 사용하는가

Langfuse는 웹 서버, 데이터베이스, 캐시 등 **5개 서비스**가 함께 동작한다.
이 서비스들을 내 컴퓨터에 하나씩 직접 설치하면 다음과 같은 문제가 생긴다.

- PostgreSQL, Redis, ClickHouse, MinIO를 각각 설치해야 한다
- 버전 충돌, 포트 충돌, 설정 파일 관리가 필요하다
- 실습 후 깨끗하게 삭제하기 어렵다

Docker는 이 문제를 해결한다.
각 서비스를 **컨테이너**라는 격리된 상자에 넣어 실행한다.
내 컴퓨터 환경을 오염시키지 않고, 삭제도 한 줄로 끝난다.

```
┌────────────────────────────────────────────┐
│           내 컴퓨터 (Host)                  │
│                                            │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐     │
│  │Postgres│ │Redis │ │Click │ │MinIO │     │
│  │  DB   │ │캐시  │ │House │ │저장소│      │
│  └──────┘ └──────┘ └──────┘ └──────┘     │
│       ↕          ↕        ↕        ↕       │
│  ┌─────────────────────────────────────┐  │
│  │         langfuse-web (:3000)         │  │
│  └─────────────────────────────────────┘  │
└────────────────────────────────────────────┘
  각 서비스가 컨테이너 안에서 독립적으로 실행
```

### Docker Compose란

Docker Compose는 **여러 컨테이너를 한 번에 관리**하는 도구다.
`compose.yml` 파일에 필요한 서비스를 정의하면 된다.
`docker compose up -d` 한 줄이면 5개 서비스가 동시에 시작된다.

| 명령 | 역할 |
|------|------|
| `docker compose up -d` | 모든 서비스 시작 (백그라운드) |
| `docker compose ps` | 서비스 상태 확인 |
| `docker compose logs -f` | 실시간 로그 확인 |
| `docker compose down` | 모든 서비스 중지 |
| `docker compose down -v` | 중지 + 데이터 삭제 |

### Docker Desktop은 왜 설치하는가

Docker는 원래 Linux 전용 기술이다.
Windows나 macOS에서 Docker를 쓰려면 **가상 Linux 환경**이 필요하다.
Docker Desktop이 이 가상 환경을 자동으로 만들어준다.

- Windows: WSL 2 위에 Docker Engine을 자동 설치
- macOS: 경량 Linux VM 위에 Docker Engine 설치
- GUI 대시보드로 컨테이너 상태를 시각적으로 확인 가능

<callout icon="💡" color="gray_bg">
	Docker Desktop을 실행하지 않으면 `docker` 명령이 동작하지 않는다.
	실습 전에 반드시 Docker Desktop 앱이 실행 중인지 확인한다.
</callout>

---

## Day 1에서 LangSmith를 배운 이유

Day 1에서 LangSmith를 사용한 것은 특정 제품을 추천하기 위해서가 아니다.
LLM Observability 플랫폼은 **대부분 비슷한 기능**을 제공한다.
트레이싱, 프롬프트 관리, 평가, 비용 모니터링 — 핵심 개념은 동일하다.

LangSmith로 개념을 익혀두면 **다른 오픈소스 도구에도 그대로 적용**된다.
Langfuse, Phoenix, OpenLIT 등 어떤 도구를 선택해도 사용법이 유사하다.

> "그런데 LangSmith는 클라우드 서비스라 사내에서 못 쓰는 거 아닌가?"

맞다. 이 거부감은 자연스럽다.
그래서 오늘은 **직접 설치해서 사내망에서 운영할 수 있는 Langfuse**로 전환한다.
Day 1에서 배운 Observability 개념은 그대로 가져가면서, 배포 환경만 바꾸는 것이다.

### LangSmith — 생태계 통합의 강점

LangSmith가 나쁜 도구라는 뜻이 아니다.
LangChain 생태계와 **네이티브 통합**되는 것은 큰 장점이다.

- **환경변수 하나**(`LANGSMITH_TRACING=true`)로 추적 활성화
- **Playground** — 브라우저에서 프롬프트를 바로 테스트
- **Online Evaluation** — 프로덕션 트래픽을 실시간 평가
- **Datasets + 실험** — 오프라인 회귀 테스트와 버전 비교
- **Fleet / Studio** — 노코드로 Agent를 설계하고 배포

클라우드 환경에 제약이 없다면 LangSmith는 가장 편한 선택이다.

### Langfuse — 사내망에서 돌릴 수 있는 대안

Langfuse는 **오픈소스이고 셀프 호스팅이 가능**하다.
사내망, 에어갭 환경에서도 Observability를 확보할 수 있다.

- **셀프 호스팅** — `compose.yml` 하나로 `localhost:3000`에서 실행
- **50+ 프레임워크 지원** — LangChain 외 OpenAI SDK, Vercel AI 등
- **OpenTelemetry 기반** — 벤더 종속 없음
- **프롬프트 관리** — 버전 관리 + Playground + 실험

### 비교표

| 기준 | LangSmith | Langfuse |
|------|:---------:|:--------:|
| **생태계 통합** | LangChain 네이티브 | CallbackHandler |
| **배포 환경** | 클라우드 전용 | 클라우드 + **셀프 호스팅** |
| **평가** | Online + Offline | Online + Offline |
| **프롬프트 관리** | Hub + Playground | 버전 관리 + Playground |
| **Agent 배포** | Fleet / Studio | 미지원 |
| **프레임워크 지원** | 다중 (OpenAI, Anthropic 등) | 50+ (OpenTelemetry) |
| **라이선스** | 상용 (무료 티어) | 오픈소스 (MIT) |

<callout icon="💡" color="gray_bg">
	**선택 기준**: 클라우드 환경이고 LangChain 중심이면 → LangSmith.
	사내망 제약이 있거나 멀티 프레임워크면 → Langfuse.
	둘 다 사용해도 된다 — LangSmith로 개발하고, Langfuse를 사내 프로덕션에 배포하는 조합도 가능하다.
</callout>

<callout icon="⚠️" color="yellow_bg">
	Langfuse 셀프 호스팅 버전은 일부 엔터프라이즈 기능이 제한된다.
	자세한 내용: https://langfuse.com/self-hosting/license-key
</callout>

---

## 사전 준비

Docker Desktop이 설치되어 있어야 한다.

- Windows: [Docker Desktop 다운로드](https://www.docker.com/products/docker-desktop/)
- 설치 후 Docker Desktop 실행 → 왼쪽 하단에 초록색 "Engine running" 확인

```bash
# Docker가 정상 동작하는지 확인
docker --version
docker compose version
```

---

## Step 1: Langfuse 실행

```bash
# langfuse-self-host 디렉토리로 이동
cd labs/day2/langfuse-self-host

# Docker Compose로 실행 (백그라운드)
docker compose up -d
```

5개 서비스가 순서대로 시작된다.

| 서비스 | 역할 | 포트 |
|--------|------|------|
| postgres | 메인 DB | 5432 |
| redis | 캐시/큐 | 6379 |
| clickhouse | 분석 DB | 8123 |
| minio | 오브젝트 저장소 | 9090 |
| **langfuse-web** | **웹 UI** | **3000** |

<callout icon="💡" color="gray_bg">
	첫 실행 시 이미지 다운로드에 3~5분 소요된다.
	`docker compose logs -f langfuse-web`으로 진행 상황을 확인할 수 있다.
</callout>

---

## Step 2: 계정 생성

브라우저에서 `http://localhost:3000` 접속한다.

- **Sign Up** 클릭
- 이메일, 이름, 비밀번호 입력 (로컬이므로 아무 값이나 OK)
- 로그인 완료

---

## Step 3: API 키 발급

- 좌측 사이드바 → **Settings** → **API Keys**
- **Create API Key** 클릭
- `Secret Key`와 `Public Key`를 복사

---

## Step 4: .env 설정

```bash
# labs/day2/.env에 다음 값을 추가
LANGFUSE_SECRET_KEY=sk-lf-...   # 위에서 복사한 Secret Key
LANGFUSE_PUBLIC_KEY=pk-lf-...   # 위에서 복사한 Public Key
LANGFUSE_HOST=http://localhost:3000
```

이후 `00_basics/00_setup.ipynb`에서 Langfuse 연동이 자동으로 활성화된다.

---

## 확인

```python
# 00_setup.ipynb 실행 시 아래 메시지가 출력되면 성공
# "Langfuse tracing ON — http://localhost:3000"
```

실습 도중 `http://localhost:3000`에서 Trace를 실시간으로 확인할 수 있다.

---

## 종료 및 정리

```bash
# 실습 종료 후
docker compose down       # 컨테이너 중지 (데이터 유지)
docker compose down -v    # 컨테이너 + 데이터 삭제
```
