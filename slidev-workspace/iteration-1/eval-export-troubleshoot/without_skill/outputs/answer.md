# Slidev PDF 내보내기 트러블슈팅 & Dev Server 백그라운드 실행 가이드

## 1. PDF 내보내기 에러 해결: `Cannot find module 'playwright-chromium'`

### 원인

`npx slidev export` 명령은 내부적으로 Playwright의 Chromium 브라우저를 사용하여 슬라이드를 렌더링한 뒤 PDF로 변환한다. Slidev는 기본 설치 시 `playwright-chromium` 패키지를 포함하지 않기 때문에, export 기능을 처음 사용할 때 이 에러가 발생한다.

### 해결 방법

#### Step 1: playwright-chromium 설치

프로젝트 디렉토리(slides.md가 있는 곳)에서 다음 명령을 실행한다:

```bash
npm install -D playwright-chromium
```

이 명령은 두 가지를 수행한다:
- `playwright-chromium` npm 패키지를 devDependencies로 설치
- Chromium 브라우저 바이너리를 자동으로 다운로드 (약 150~200MB)

#### Step 2: 브라우저 바이너리가 설치되지 않은 경우

만약 패키지는 설치되었지만 브라우저 바이너리가 없다는 에러가 나오면, 수동으로 브라우저를 설치한다:

```bash
npx playwright install chromium
```

#### Step 3: PDF 내보내기 실행

```bash
npx slidev export
```

기본적으로 `slides-export.pdf` 파일이 생성된다.

### 주요 export 옵션

```bash
# 기본 내보내기 (slides.md -> slides-export.pdf)
npx slidev export

# 특정 파일 지정
npx slidev export my-slides.md

# 출력 파일명 지정
npx slidev export --output my-presentation.pdf

# 다크 모드로 내보내기
npx slidev export --dark

# 대기 시간 설정 (애니메이션이 많은 경우 늘린다)
npx slidev export --timeout 60000

# PNG 이미지로 각 슬라이드를 내보내기 (PDF 대신)
npx slidev export --format png

# 클릭 애니메이션 단계별로 각각 별도 페이지로 내보내기
npx slidev export --with-clicks

# 특정 슬라이드 범위만 내보내기
npx slidev export --range 1,4-6,10
```

### 자주 발생하는 추가 에러와 해결법

| 에러 | 원인 | 해결 |
|------|------|------|
| `Timed out` | 슬라이드 렌더링 시간 초과 | `--timeout 120000` 옵션 추가 |
| `Error: browserType.launch` | 시스템 의존성 부족 (Linux) | `npx playwright install-deps chromium` 실행 |
| `Cannot find module '@slidev/cli'` | Slidev CLI 미설치 | `npm install -D @slidev/cli` 실행 |
| 빈 페이지가 export됨 | Dev server 포트 충돌 또는 슬라이드 에러 | 기존 dev server 종료 후 재시도 |

### package.json에 스크립트 등록 (권장)

매번 긴 명령을 입력하지 않도록 스크립트를 등록해 둔다:

```json
{
  "scripts": {
    "dev": "slidev",
    "build": "slidev build",
    "export": "slidev export",
    "export:dark": "slidev export --dark",
    "export:png": "slidev export --format png"
  },
  "devDependencies": {
    "@slidev/cli": "^0.50.0",
    "@slidev/theme-default": "latest",
    "playwright-chromium": "^1.49.0"
  }
}
```

---

## 2. Claude Code Bash에서 Slidev Dev Server 백그라운드 실행

Claude Code의 Bash 도구는 명령 실행 후 결과를 기다리는 동기 방식으로 동작한다. `npx slidev` 같은 dev server는 프로세스가 종료되지 않고 계속 실행되므로, 일반적인 방식으로 실행하면 타임아웃이 발생한다.

### 방법 1: `run_in_background` 파라미터 사용 (권장)

Claude Code의 Bash 도구에는 `run_in_background` 파라미터가 있다. 이를 `true`로 설정하면 명령이 백그라운드에서 실행되고, 완료 시 알림을 받는다.

```
Bash 도구 호출 시:
- command: "cd /path/to/slides && npx slidev --port 3030"
- run_in_background: true
```

이 방식의 장점:
- Dev server가 백그라운드에서 계속 실행됨
- Claude Code가 다른 작업을 계속 수행할 수 있음
- 프로세스 완료(또는 종료) 시 알림을 받음

### 방법 2: nohup + & 조합

쉘에서 전통적인 백그라운드 실행 방법:

```bash
cd /path/to/slides && nohup npx slidev --port 3030 > /tmp/slidev.log 2>&1 &
echo "Slidev PID: $!"
```

- `nohup`: 터미널 세션이 끊어져도 프로세스가 유지됨
- `&`: 백그라운드에서 실행
- `> /tmp/slidev.log 2>&1`: stdout과 stderr를 로그 파일로 리다이렉트
- `$!`: 마지막 백그라운드 프로세스의 PID를 출력

### 방법 3: 특정 포트에서 실행 후 확인

```bash
# 1. 백그라운드로 dev server 시작
cd /path/to/slides && npx slidev --port 3030 > /tmp/slidev.log 2>&1 &

# 2. 서버가 준비될 때까지 대기 (최대 15초)
for i in $(seq 1 15); do
  curl -s http://localhost:3030 > /dev/null 2>&1 && echo "Server is ready on port 3030" && break
  sleep 1
done

# 3. 로그 확인
cat /tmp/slidev.log
```

### Dev Server 종료 방법

```bash
# 방법 1: PID로 종료
kill <PID>

# 방법 2: 포트 번호로 프로세스 찾아서 종료
lsof -ti:3030 | xargs kill

# 방법 3: 프로세스 이름으로 찾아서 종료
pkill -f "slidev"
```

### 실전 워크플로우 예시

PDF export를 위해 dev server 없이 바로 export하는 것이 일반적이지만, 슬라이드 미리보기가 필요한 경우 다음 순서로 작업한다:

```bash
# 1. 의존성 설치 (최초 1회)
cd /path/to/slides && npm install

# 2. 백그라운드로 dev server 실행
npx slidev --port 3030 > /tmp/slidev.log 2>&1 &

# 3. (작업 수행 - 슬라이드 수정 등)

# 4. PDF 내보내기 (dev server와 별개로 실행 가능)
npx slidev export --dark

# 5. 작업 완료 후 dev server 종료
lsof -ti:3030 | xargs kill 2>/dev/null
```

### 참고: export는 dev server 없이도 가능

`npx slidev export`는 내부적으로 자체 서버를 띄우고 렌더링한 뒤 종료하므로, **PDF 내보내기를 위해 별도로 dev server를 띄울 필요는 없다**. Dev server는 슬라이드를 브라우저에서 미리보기할 때 필요하다.
