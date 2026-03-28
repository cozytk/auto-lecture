# Slidev 실행 가이드 (Claude Code 환경)

Claude Code의 Bash 도구에서 Slidev를 실행할 때의 제약사항과 검증된 패턴을 정리한다.
14개 시나리오의 체계적 테스트(2026-03-16)를 통해 검증됨.

## 핵심 원칙: TTY 판단 휴리스틱

CLI 도구를 백그라운드로 실행하기 전에:

1. **유한한 명령인가?** (`build`, `export`, `format`) → 그대로 실행. TTY 불필요.
2. **장기 실행 서버인가?** → 키보드 단축키(`r`estart, `o`pen, `q`uit 등)가 있는지 확인.
3. **키보드 단축키가 있는가?** → **`script -q /dev/null` 래퍼 필수.**
4. **키보드 단축키가 없는가?** (예: `python3 -m http.server`) → `&`만으로 충분.

**일반 원칙**: CLI 출력에 "Press X to..." 같은 인터랙티브 안내가 보이면 TTY가 필요하다. TTY 없이는 배너만 출력하고 조용히 종료된다. Slidev 외에도 Vite 기반 인터랙티브 dev server에 동일하게 적용될 수 있다.

## TTY 제약 상세

**Slidev dev server는 TTY(pseudo-terminal)가 없으면 배너(URL) 출력 직후 즉시 종료된다.**

이는 Slidev가 키보드 입력(restart, open, edit, quit)을 대기하는 인터랙티브 모드로 동작하기 때문이다. TTY가 없으면 stdin이 즉시 닫히고, 프로세스가 종료된다.

### 증상 (이것을 보면 TTY 문제)

- 로그에 `http://localhost:PORT/` URL이 정상 출력됨
- 하지만 `curl`이나 브라우저에서 접속 불가 (connection refused)
- 프로세스가 2~3초 내에 자동 종료
- `lsof -i :PORT`에 아무것도 없음

## 실패하는 패턴 (사용 금지)

```bash
# 1. 단순 background - TTY 없음, 즉시 종료
npx slidev --port 3000 &

# 2. nohup - SIGHUP만 방지, TTY 문제 해결 불가
nohup npx slidev --port 3000 &

# 3. stdin 차단 - 확실하게 실패
npx slidev --port 3000 < /dev/null &

# 4. run_in_background: true - Bash 도구 옵션, 동일하게 실패
# (태스크 완료 시 프로세스도 함께 종료)

# 5. setsid - macOS에서 정상 동작 안 함
setsid npx slidev --port 3000 &
```

## 성공하는 패턴

### 패턴 1: 정적 빌드 (가장 안정적, 권장)

```bash
npx slidev build
# 결과: ./dist/ 디렉토리에 정적 SPA 생성
# 소요 시간: ~3초
```

- 유한한 명령이므로 TTY 불필요
- CI/CD, 배포에 적합
- `dist/` 디렉토리를 `python3 -m http.server`로 서빙 가능

### 패턴 2: PDF 내보내기

```bash
# 사전 설치 (1회)
npm install -D playwright-chromium

# PDF 생성
npx slidev export --output slides.pdf
```

- `playwright-chromium` 미설치 시 에러 발생
- 유한한 명령이므로 TTY 불필요

### 패턴 3: Dev server + 작업 (pseudo-TTY 필수)

**`script -q /dev/null` 명령으로 pseudo-TTY를 제공해야 한다.**

```bash
# 서버 시작 (pseudo-TTY 포함)
script -q /dev/null npx slidev --port PORT > /tmp/slidev.log 2>&1 &
SERVER_PID=$!

# 준비 대기 (폴링)
for i in $(seq 1 30); do
  HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:PORT/ 2>/dev/null)
  if [ "$HTTP_CODE" = "200" ]; then
    echo "Server ready after ${i}s"
    break
  fi
  [ $i -eq 30 ] && echo "TIMEOUT" && kill $SERVER_PID 2>/dev/null && exit 1
  sleep 1
done

# ... 여기서 작업 수행 (curl, Playwright 등) ...

# 정리
kill $SERVER_PID 2>/dev/null
wait $SERVER_PID 2>/dev/null
```

**반드시 단일 Bash 명령 안에서 서버 시작 → 작업 → 종료를 모두 수행한다.**
Bash 명령이 끝나면 자식 프로세스도 함께 종료되기 때문이다.

### 패턴 4: Playwright 시각 검증 (전체 워크플로우)

```bash
# 서버 시작
script -q /dev/null npx slidev --port PORT > /tmp/slidev.log 2>&1 &
SERVER_PID=$!

# 준비 대기
for i in $(seq 1 30); do
  HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:PORT/ 2>/dev/null)
  [ "$HTTP_CODE" = "200" ] && echo "Ready in ${i}s" && break
  [ $i -eq 30 ] && echo "TIMEOUT" && kill $SERVER_PID 2>/dev/null && exit 1
  sleep 1
done

# Playwright 스크린샷
node -e "
const { chromium } = require('playwright-chromium');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 980, height: 552 } });

  const totalSlides = 10; // 실제 슬라이드 수로 변경
  for (let i = 1; i <= totalSlides; i++) {
    await page.goto('http://localhost:PORT/' + i);
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(2000);
    await page.screenshot({ path: '/tmp/slide-' + i + '.png' });
    console.log('Slide ' + i + ': OK');
  }
  await browser.close();
})().catch(e => { console.error('FAILED:', e.message); process.exit(1); });
"

# 정리
kill $SERVER_PID 2>/dev/null
wait $SERVER_PID 2>/dev/null
```

**viewport**: 980x552px (Slidev 기본 캔버스 크기)

## 정적 빌드 후 서빙

`npx slidev build` 후 정적 파일을 서빙하려면:

```bash
python3 -m http.server 3000 --directory ./dist &
SERVER_PID=$!
sleep 2
# curl, Playwright 등 작업 수행
kill $SERVER_PID
```

Python http.server는 TTY 불필요하므로 `script` 없이 `&`만으로 동작한다.

## 의존성 설치

슬라이드 프로젝트의 `package.json`에 최소 필요:

```json
{
  "dependencies": {
    "@slidev/cli": "^52.14.1",
    "@slidev/theme-default": "^0.25.0"
  },
  "devDependencies": {
    "playwright-chromium": "latest"
  }
}
```

- `playwright-chromium`: PDF 내보내기 및 Playwright 시각 검증에 필요
- `@slidev/theme-default`: 기본 테마 (theme: default 사용 시)

## 포트 선택

- 기본 포트: 3030
- 충돌 방지를 위해 `--port` 플래그로 명시적 지정 권장
- 사용 중인 포트 확인: `lsof -i :PORT`

## exit code 참고

| exit code | 의미 |
|-----------|------|
| 0 | 정상 종료 (build, export 완료) |
| 1 | 에러 (의존성 없음, 파일 없음 등) |
| 143 | SIGTERM으로 종료 (kill에 의한 정상 종료) |

- dev server를 `kill`로 종료하면 exit code 143이 반환된다. 이는 정상이다.
- Bash 도구에서 exit code 143은 에러로 표시되지만 무시해도 된다.

## 주의사항

1. **`node_modules` 변경 후 첫 실행**: Vite가 의존성을 재최적화하므로 서버 시작이 느릴 수 있다. 폴링 대기를 30초로 넉넉히 잡는다.
2. **좀비 프로세스 정리**: 비정상 종료 시 남은 프로세스를 `pkill -f "slidev"` 또는 `lsof -i :PORT`로 확인·정리한다.
3. **동시 실행 금지**: 같은 포트에서 여러 Slidev 서버를 동시 실행하면 포트 충돌. 에이전트별 고유 포트를 지정한다.
