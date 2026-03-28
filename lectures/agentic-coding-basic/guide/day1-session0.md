# 세션 0: 실습 환경 세팅 가이드

<callout icon="📖" color="blue_bg">
	**학습 목표:**
	1. WSL + Ubuntu 24.04 LTS 환경에서 OpenCode를 설치할 수 있다
	2. OpenCode Zen 또는 OpenRouter를 연결하여 무료 모델로 코드 에이전트를 사용할 수 있다
	3. 첫 대화를 통해 정상 동작을 확인할 수 있다
</callout>

> 이 가이드는 **수업 전에 미리 완료**해야 하는 사전 세팅 가이드다.
> 수업 당일에는 환경이 준비된 상태에서 바로 실습에 들어간다.

---

## 0. 시작하기 전에

### 이미 코드 에이전트를 사용하고 있다면

<callout icon="💡" color="gray_bg">
	이미 **Claude Code**, **Codex**, **Gemini CLI** 등 코드 에이전트를 구독·사용 중이라면, 해당 도구로 수업 실습을 진행해도 된다. 오늘 수업에서 다루는 개념(에이전틱 루프, 컨텍스트 엔지니어링, 프로젝트 규칙 등)은 **특정 도구에 종속되지 않는 보편적 원리**이므로, 어떤 코드 에이전트를 사용하든 동일하게 적용된다.
</callout>

다만 다음 사항을 확인하자:

| 도구 | 확인 사항 |
|------|----------|
| **Claude Code** | `claude --version`으로 설치 확인. Max 또는 Pro 구독 필요 |
| **Codex** | `codex --version`으로 설치 확인. ChatGPT Plus/Pro 구독 필요 |
| **Gemini CLI** | `gemini --version`으로 설치 확인. Google AI Studio API 키 필요 |

위 도구 중 하나라도 준비되어 있다면 **"3. 설치 확인"** 단계로 바로 건너뛰어도 좋다.

코드 에이전트가 처음이거나 무료로 시작하고 싶다면, 아래 안내를 따라 **OpenCode + Zen**을 세팅하자.

---

## 1. OpenCode 설치 (WSL + Ubuntu 24.04 LTS)

### 사전 요구사항

다음이 이미 설치되어 있어야 한다:

- **WSL2 + Ubuntu 24.04 LTS** — 설치가 안 되어 있다면 Windows PowerShell(관리자)에서:
  ```powershell
  wsl --install -d Ubuntu-24.04
  ```
- **Node.js 18+** — 확인: `node --version`
  ```bash
  # 설치 안 되어 있다면 nvm으로 설치
  curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash
  source ~/.bashrc
  nvm install --lts
  ```
- **Git** — 확인: `git --version`

---

### 설치 방법

WSL Ubuntu 터미널을 열고 아래 명령어를 실행한다.

**방법 A: 공식 설치 스크립트 (권장)**

```bash
curl -fsSL https://opencode.ai/install | bash
```

**방법 B: npm으로 설치**

```bash
npm install -g opencode-ai
```

설치 확인:

```bash
opencode --version
```

<callout icon="⚠️" color="yellow_bg">
	**WSL 성능 팁**: 프로젝트 폴더는 WSL 파일시스템 안(`~/code/`)에 두는 것을 권장한다.
	`/mnt/c/` 경로(Windows 드라이브)에서 작업하면 파일 I/O 성능이 크게 떨어진다.
</callout>

---

## 2. OpenCode Zen 연결 (무료 모델 사용)

### OpenCode Zen이란?

OpenCode Zen은 OpenCode 팀이 운영하는 **관리형 AI 게이트웨이**다.
여러 AI 모델을 하나의 API 키로 사용할 수 있으며, **무료 모델**도 제공한다.

직접 OpenAI/Anthropic/Google API 키를 발급받을 필요 없이, Zen 계정 하나로 다양한 모델을 사용할 수 있어서 실습 환경으로 적합하다.

---

### Step 1: 계정 생성 및 API 키 발급

1. https://opencode.ai/auth 접속
2. **GitHub** 또는 **Google** 계정으로 로그인
3. 로그인 후 **API Key** 생성 → 키를 복사해 둔다

---

### Step 2: OpenCode에서 Zen 연결

OpenCode를 실행한 뒤, TUI 내에서 연결한다:

```bash
# 아무 프로젝트 폴더에서 opencode 실행
cd ~/code
mkdir practice && cd practice
git init
opencode
```

OpenCode TUI가 열리면:

```
/connect
```

입력 후 **"OpenCode Zen"**을 선택하고, 복사해 둔 API 키를 붙여넣는다.

인증 정보는 `~/.local/share/opencode/auth.json`에 저장된다.

---

### Step 3: 무료 모델 설정

프로젝트 루트에 `opencode.json` 파일을 만들어 무료 모델을 기본값으로 설정한다:

```jsonc
// opencode.json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "opencode/minimax-m2-5-free",
  "small_model": "opencode/mimo-v2-flash-free"
}
```

---

### 현재 사용 가능한 무료 모델 (2026년 3월 기준)

| 모델 | 특징 | 비고 |
|------|------|------|
| **MiniMax M2.5 Free** | 입출력 모두 무료, 코딩 성능 양호 | 실습 기본 모델로 추천 |
| **MiMo V2 Flash Free** | 빠른 응답, 간단한 작업에 적합 | `small_model`로 추천 |
| **Nemotron 3 Super Free** | NVIDIA 제공, 한시적 무료 | 기간 한정 |
| **Big Pickle** | 스텔스 모델, 성능 우수 | 데이터가 모델 개선에 활용됨 |

<callout icon="⚠️" color="yellow_bg">
	**무료 모델 주의사항**:
	- 무료 모델은 제공사가 **모델 개선을 위해 사용 데이터를 활용**할 수 있다. 민감한 코드 작업에는 주의.
	- 무료 모델 목록은 수시로 변경될 수 있다. 최신 목록은 [Zen 문서](https://opencode.ai/docs/zen/)에서 확인.
	- 유료 모델(Claude Sonnet, GPT-5.3 등)은 제로 리텐션 정책을 따른다.
</callout>

---

### 대안: OpenRouter 무료 모델 추가

Zen 외에 **OpenRouter**를 통해 추가 무료 모델을 사용할 수 있다.
OpenRouter는 다양한 AI 모델을 하나의 API로 제공하는 **AI 모델 라우터**다.

<callout icon="💡" color="gray_bg">
	**OpenRouter 무료 모델의 두 가지 유형:**
	- `:free` 태그 모델 — 공식 무료 모델. $10 이상 결제하지 않으면 **하루 총 50회 호출 제한**.
	- **`:free` 태그 없이 가격이 $0인 모델** — 출시 전 임시로 무료 제공되는 모델. `:free` 모델과 별도로, 50회 제한에 포함되지 않는다.
	아래 두 모델은 후자에 해당하며, Zen 무료 모델과 **병행하면 무료 사용량을 크게 늘릴 수 있다**.
</callout>

**현재 사용 가능한 OpenRouter 임시 무료 모델 (2026년 3월 기준):**

| 모델 | 컨텍스트 | 최대 출력 | 특징 |
|------|----------|----------|------|
| **Hunter Alpha** (`openrouter/hunter-alpha`) | 1M 토큰 | 32K | 1T 파라미터, 에이전틱 작업 특화. 추론·도구 사용 지원 |
| **Healer Alpha** (`openrouter/healer-alpha`) | 262K 토큰 | 32K | 멀티모달(텍스트·이미지·오디오·비디오 입력). 추론·도구 사용 지원 |

<callout icon="⚠️" color="yellow_bg">
	**임시 무료 모델 주의사항**:
	- 두 모델 모두 "프롬프트와 응답이 로깅되며 모델 개선에 활용될 수 있다"고 명시되어 있다.
	- **출시 전 임시 무료**이므로 언제든 유료로 전환될 수 있다. 수업 전 [OpenRouter](https://openrouter.ai/)에서 가격을 다시 확인하라.
	- 프로덕션이나 민감한 코드에는 사용하지 마라.
</callout>

---

### OpenRouter 연결 방법

**Step 1: API 키 발급**

1. https://openrouter.ai/ 접속 → 회원가입 (Google/GitHub)
2. https://openrouter.ai/settings/keys 에서 **API Key** 생성 → 복사

**Step 2: OpenCode에서 연결**

OpenCode TUI에서 `/connect` 입력 → **OpenRouter**를 선택 → 복사한 API 키 붙여넣기.

**Step 3: 모델 설정**

`opencode.json`에서 OpenRouter 모델을 기본값으로 설정한다:

```jsonc
// opencode.json — OpenRouter 모델 사용
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "openrouter": {
      "models": {
        "openrouter/hunter-alpha": {},
        "openrouter/healer-alpha": {}
      }
    }
  },
  "model": "openrouter/hunter-alpha",
  "small_model": "openrouter/healer-alpha"
}
```

<callout icon="💡" color="gray_bg">
	**Zen + OpenRouter 병행 설정:**
	Zen과 OpenRouter를 모두 연결해두면 `/models` 명령으로 실시간 전환이 가능하다.
	Zen 무료 모델이 레이트 리밋에 걸릴 때 OpenRouter 모델로 전환하는 식으로 **무료 사용량을 최대화**할 수 있다.
	```jsonc
	// Zen을 기본으로 쓰고, OpenRouter를 백업으로 두는 설정
	{
	  "$schema": "https://opencode.ai/config.json",
	  "provider": {
	    "openrouter": {
	      "models": {
	        "openrouter/hunter-alpha": {},
	        "openrouter/healer-alpha": {}
	      }
	    }
	  },
	  "model": "opencode/minimax-m2-5-free",
	  "small_model": "opencode/mimo-v2-flash-free"
	}
	```
	→ 기본은 Zen 무료 모델, 레이트 리밋 시 TUI에서 `/models` → Hunter Alpha로 전환.
</callout>

---

### 사용량 추정

무료 모델의 정확한 일일 한도는 공식 문서에 명시되어 있지 않으나, 커뮤니티 보고와 서드파티 문서를 종합하면:

| 항목 | Zen 무료 모델 | OpenRouter 임시 무료 모델 |
|------|--------------|--------------------------|
| **일일 요청 수** | 약 100회 내외 (비공식) | 별도 제한 (`:free` 50회와 독립) |
| **레이트 리밋** | 분당 요청 제한 있음 | 분당 요청 제한 있음 |
| **실습 기준 충분도** | 하루 수업에 충분 | Zen과 병행 시 여유 확보 |

<callout icon="💡" color="gray_bg">
	**실습 기준 사용량 계산**:
	수업 중 실습은 4개 세션에 걸쳐 진행된다. 실습당 평균 10~15회 요청을 보낸다고 가정하면, 하루 총 **40~60회** 수준이다.
	- **Zen만 사용**: 일일 한도 내에서 충분히 소화 가능
	- **Zen + OpenRouter 병행**: 레이트 리밋 걸릴 때 전환하면 사실상 **무제한에 가까운 무료 사용량** 확보
</callout>

레이트 리밋에 걸릴 경우 OpenCode TUI에 에러 메시지가 표시된다. 잠시 기다린 후 재시도하거나, `/models`로 다른 무료 모델로 전환하면 된다.

---

## 3. 설치 확인

어떤 코드 에이전트를 사용하든, 아래 체크리스트를 완료해야 수업 준비가 끝난다.

### 체크리스트

```
[ ] 코드 에이전트가 실행된다 (opencode / claude / codex / gemini)
[ ] 간단한 질문에 응답한다
[ ] 파일을 읽고 쓸 수 있다
[ ] 셸 명령을 실행할 수 있다
```

### 테스트 방법

**1단계: 프로젝트 준비**

```bash
cd ~/code
mkdir agent-test && cd agent-test
git init
echo "print('Hello, Agent!')" > hello.py
```

**2단계: 코드 에이전트 실행**

```bash
# OpenCode 사용자
opencode

# Claude Code 사용자
claude

# Codex 사용자
codex

# Gemini CLI 사용자
gemini
```

**3단계: 테스트 프롬프트**

에이전트가 실행되면 아래 프롬프트를 입력한다:

```
hello.py 파일을 읽고, 출력 메시지를 "Hello, Agentic Coding!"으로 바꿔줘.
그리고 python hello.py를 실행해서 결과를 보여줘.
```

에이전트가 다음을 수행하면 성공이다:
1. `hello.py` 파일을 읽는다
2. 코드를 수정한다
3. `python hello.py`를 실행한다
4. `Hello, Agentic Coding!` 출력을 확인한다

<callout icon="✅" color="green_bg">
	이 4단계가 모두 동작하면 실습 환경 준비 완료! 수업 당일에 바로 실습에 참여할 수 있다.
</callout>

---

## 4. 트러블슈팅

### OpenCode가 설치되지 않을 때

```bash
# Node.js 버전 확인 (18 이상 필요)
node --version

# npm 캐시 문제일 경우
npm cache clean --force
npm install -g opencode-ai
```

### Zen 연결이 안 될 때

```bash
# 네트워크 확인
curl -I https://opencode.ai

# 인증 정보 초기화 후 재연결
rm ~/.local/share/opencode/auth.json
# opencode 실행 후 /connect 재시도
```

### "Rate limited" 에러가 뜰 때

- 무료 모델의 레이트 리밋에 걸린 것이다
- 1~2분 기다린 후 재시도
- 다른 무료 모델로 전환: `opencode.json`에서 `model` 값을 변경

### WSL에서 opencode 실행이 느릴 때

```bash
# 프로젝트가 /mnt/c/ 아래에 있다면 WSL 파일시스템으로 이동
cp -r /mnt/c/Users/YourName/project ~/code/project
cd ~/code/project
opencode
```

---

## 참고 자료

- [OpenCode 공식 문서](https://opencode.ai/docs/)
- [OpenCode 다운로드](https://opencode.ai/download)
- [OpenCode Zen 문서](https://opencode.ai/docs/zen/)
- [OpenCode WSL 설치 가이드](https://opencode.ai/docs/windows-wsl/)
- [OpenCode 설정(Config) 문서](https://opencode.ai/docs/config/)
