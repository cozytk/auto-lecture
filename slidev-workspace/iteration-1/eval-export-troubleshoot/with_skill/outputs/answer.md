# Slidev Export 트러블슈팅 & Dev Server 실행 가이드

## 1. `Cannot find module 'playwright-chromium'` 에러 해결

### 원인

Slidev의 PDF/PPTX/PNG export 기능은 내부적으로 Playwright 브라우저를 사용하여 각 슬라이드를 렌더링한 뒤 캡처합니다. `playwright-chromium`은 Slidev의 기본 의존성에 포함되어 있지 않기 때문에, export 전에 별도로 설치해야 합니다.

### 해결 방법

프로젝트 디렉토리에서 devDependency로 설치합니다:

```bash
# npm 사용 시
npm install -D playwright-chromium

# pnpm 사용 시
pnpm add -D playwright-chromium

# yarn 사용 시
yarn add -D playwright-chromium
```

설치 후 다시 export를 실행합니다:

```bash
npx slidev export --output slides.pdf
```

### CI/CD 환경에서 추가 설정

CI/CD 서버(GitHub Actions, GitLab CI 등)에서는 Chromium 브라우저 바이너리도 별도로 설치해야 할 수 있습니다:

```bash
npx playwright install chromium
```

### package.json 권장 설정

export를 자주 사용한다면 `package.json`에 스크립트와 함께 의존성을 명시해 두세요:

```json
{
  "scripts": {
    "dev": "slidev",
    "build": "slidev build",
    "export": "slidev export"
  },
  "dependencies": {
    "@slidev/cli": "^52.14.1",
    "@slidev/theme-default": "^0.25.0"
  },
  "devDependencies": {
    "playwright-chromium": "latest"
  }
}
```

### Export 주요 옵션

설치 완료 후 다양한 형식으로 내보낼 수 있습니다:

```bash
# PDF (기본)
npx slidev export
npx slidev export --output my-slides.pdf

# 다크모드 PDF
npx slidev export --dark

# 클릭 애니메이션 단계별 페이지 포함
npx slidev export --with-clicks

# PowerPoint
npx slidev export --format pptx

# PNG (개별 이미지)
npx slidev export --format png
npx slidev export --format png --range 1-5

# 목차 포함 PDF
npx slidev export --with-toc

# 렌더링이 느린 슬라이드 대응 (타임아웃 + 대기시간 증가)
npx slidev export --timeout 60000 --wait 2000
```

---

## 2. Claude Code Bash에서 Dev Server 백그라운드 실행

### 핵심 문제: TTY(pseudo-terminal) 요구

Slidev dev server는 키보드 단축키(슬라이드 이동, 프레젠터 모드 등)를 지원하기 위해 pseudo-TTY가 필요합니다. Claude Code의 Bash 도구는 TTY를 제공하지 않기 때문에, 단순히 `&`를 붙여 백그라운드로 실행하면 프로세스가 2~3초 내에 자동 종료됩니다.

### 실패하는 패턴 (사용 금지)

아래 방법들은 모두 TTY가 없어 서버가 즉시 죽습니다:

```bash
# 모두 실패합니다:
npx slidev --port 3030 &                    # TTY 없음
nohup npx slidev --port 3030 &              # SIGHUP만 방지, TTY 문제는 해결 안 됨
npx slidev --port 3030 < /dev/null &        # stdin 차단, TTY 문제는 해결 안 됨
setsid npx slidev --port 3030 &             # macOS에서 비호환
# run_in_background: true                   # 태스크 종료 시 프로세스도 함께 죽음
```

### 해결: `script -q /dev/null` 래퍼

`script` 명령어는 pseudo-TTY를 생성해주는 Unix 유틸리티입니다. `-q /dev/null` 옵션으로 불필요한 출력 녹화 없이 TTY만 제공합니다:

```bash
script -q /dev/null npx slidev --port 3030 > /tmp/slidev.log 2>&1 &
```

**각 부분 설명:**

| 부분 | 역할 |
|------|------|
| `script -q /dev/null` | pseudo-TTY를 생성. `-q`는 quiet 모드, `/dev/null`은 녹화 파일을 버림 |
| `npx slidev --port 3030` | Slidev dev server를 포트 3030에서 실행 |
| `> /tmp/slidev.log 2>&1` | stdout과 stderr를 로그 파일로 리다이렉트 |
| `&` | 백그라운드 실행 |

### 완전한 실행 패턴: 서버 시작 + 대기(Polling) + 작업 + 정리

Claude Code Bash에서는 **모든 단계를 하나의 명령어로** 실행해야 합니다. 별도의 Bash 호출로 나누면 이전 호출에서 띄운 자식 프로세스가 죽을 수 있습니다.

```bash
# 1. 서버 시작 (pseudo-TTY 래퍼)
script -q /dev/null npx slidev --port 3030 > /tmp/slidev.log 2>&1 &
SERVER_PID=$!

# 2. 서버 준비 대기 (Polling)
for i in $(seq 1 30); do
  HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3030/ 2>/dev/null)
  if [ "$HTTP_CODE" = "200" ]; then
    echo "Server ready after ${i}s"
    break
  fi
  [ $i -eq 30 ] && echo "TIMEOUT: Server failed to start" && kill $SERVER_PID 2>/dev/null && exit 1
  sleep 1
done

# 3. 여기서 원하는 작업 수행 (curl, Playwright 스크린샷 등)
echo "Server is running at http://localhost:3030"

# 4. 작업 완료 후 정리
kill $SERVER_PID 2>/dev/null
wait $SERVER_PID 2>/dev/null
```

### Polling 패턴 설명

서버가 시작되는 데 수 초가 걸리므로, curl로 HTTP 응답을 확인하며 대기합니다:

- `curl -s -o /dev/null -w "%{http_code}"`: 응답 본문은 버리고 HTTP 상태 코드만 추출
- 1초 간격으로 최대 30회 시도 (30초 타임아웃)
- HTTP 200 응답을 받으면 서버 준비 완료
- 30초 내에 준비되지 않으면 타임아웃 처리 후 프로세스 종료

---

## 3. Exit Code 143 설명

Dev server를 `kill` 명령으로 종료하면 exit code **143**이 반환됩니다. 이것은 정상적인 동작입니다.

### 계산 원리

```
Exit Code = 128 + Signal Number
SIGTERM = Signal 15
128 + 15 = 143
```

`kill` 명령어는 기본적으로 `SIGTERM` (Signal 15)을 보냅니다. 프로세스가 이 시그널로 종료되면 쉘은 `128 + 시그널번호`를 exit code로 보고합니다.

### Exit Code 요약

| Code | 의미 |
|------|------|
| 0 | 정상 완료 (`build`, `export` 등 finite 명령) |
| 1 | 에러 (의존성 누락, 파일 없음 등) |
| 143 | SIGTERM으로 종료됨 (dev server를 `kill`로 정상 종료한 경우, **에러가 아님**) |

스크립트에서 exit code 143을 만나도 당황하지 마세요. Dev server를 `kill`로 종료한 경우 143은 "정상적으로 종료 시그널을 받고 종료했다"는 의미입니다.

---

## 4. TTY 필요 여부 판단 휴리스틱

Slidev 외에 다른 CLI 도구를 Claude Code에서 실행할 때도 동일한 원칙을 적용할 수 있습니다:

| 질문 | 답변 | 대응 |
|------|------|------|
| 유한한 명령인가? (`build`, `export`) | Yes | 직접 실행. TTY 불필요 |
| 키보드 단축키가 있는 장시간 서버인가? | Yes | `script -q /dev/null` 래퍼 필수 |
| 키보드 없는 단순 서버인가? (`python3 -m http.server`) | Yes | `&`만으로 충분 |

---

## 5. 대안: Static Build + 정적 서버

Dev server 대신 정적 빌드를 사용하면 TTY 문제를 완전히 회피할 수 있습니다:

```bash
# 1. 정적 빌드 (TTY 불필요, 가장 안정적)
npx slidev build

# 2. 빌드 결과물을 정적 서버로 제공
python3 -m http.server 3030 --directory ./dist &

# 3. 바로 접속 가능
echo "http://localhost:3030"
```

`slidev build`는 TTY가 필요 없는 finite 명령이므로 Claude Code Bash에서 문제 없이 실행됩니다. 빌드 결과물인 `./dist/` 디렉토리를 Python 내장 HTTP 서버로 제공하면 dev server와 동일하게 브라우저에서 슬라이드를 볼 수 있습니다.

단, 정적 빌드에서는 HMR(Hot Module Replacement)이 지원되지 않으므로, slides.md를 수정할 때마다 다시 빌드해야 합니다.

---

## 요약 체크리스트

- [ ] `playwright-chromium`을 devDependency로 설치: `npm install -D playwright-chromium`
- [ ] Export 실행: `npx slidev export --output slides.pdf`
- [ ] Dev server는 `script -q /dev/null` 래퍼로 실행
- [ ] 서버 준비 확인은 curl polling 패턴 사용
- [ ] 작업 완료 후 `kill $SERVER_PID`로 정리 (exit code 143은 정상)
- [ ] 모든 단계를 하나의 Bash 명령어 블록에서 실행
