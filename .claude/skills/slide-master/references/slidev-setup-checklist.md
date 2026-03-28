# Slidev 개발 환경 셋업 체크리스트

새 `lectures/{topic}/slides/` 디렉토리를 만들 때 빠뜨리기 쉬운 항목들. 하나라도 빠지면 폰트 깨짐, Mermaid 에러, 느린 시작 등이 발생한다.

## 새 프로젝트 셋업 순서

```bash
TOPIC="mcp-vs-cli"
REF="typescript-react"  # 참조할 기존 프로젝트

# 1. package.json 복사 + 설치
cp lectures/${REF}/slides/package.json lectures/${TOPIC}/slides/
cd lectures/${TOPIC}/slides && pnpm install

# 2. @slidev/types 추가 (setup/mermaid.ts용)
pnpm add @slidev/types

# 3. 폰트 복사 (9개 웨이트)
mkdir -p assets/fonts
cp ../../../lectures/${REF}/slides/assets/fonts/Freesentation-*.ttf assets/fonts/

# 4. style.css 복사 (폰트 등록 + 웨이트 시스템 + Mermaid CSS + 박스 스타일)
cp ../../../lectures/${REF}/slides/style.css .

# 5. setup/mermaid.ts 복사 (다크 테마)
mkdir -p setup
cp ../../../lectures/${REF}/slides/setup/mermaid.ts setup/
```

**빠뜨리면 생기는 일**:
- #1 누락 → `npx` 매번 다운로드, 30초+ 지연
- #2 누락 → `Failed to resolve import "@slidev/types"` 에러
- #3 누락 → 시스템 폰트 fallback, 웨이트 무시
- #4 누락 → 폰트 웨이트 전부 Regular로 렌더링, Mermaid SVG 너비 제한 없음
- #5 누락 → Mermaid 다이어그램 라이트 모드로 렌더링 (다크 배경에서 안 보임)

## 포트 전달 함정

`slidev-serve.sh`가 `package.json`의 `"dev"` 스크립트를 감지하면 `pnpm dev -- --port $port`로 실행한다. **pnpm이 `--` 뒤의 `--port`를 slidev에 제대로 전달하지 못한다.**

**증상**: `--port 3031`을 지정했는데 `http://localhost:3030/`에서 뜸

**해결**: `npx slidev slides.md --port 3031`을 직접 사용하거나, tmux 세션을 직접 생성:
```bash
tmux new-session -d -s slidev -c /path/to/slides "npx slidev slides.md --port 3031"
```

**디버깅 팁**: 항상 `tmux capture-pane -t slidev -p | tail -20`으로 실제 포트를 확인한다.

## npx 느린 시작 방지

slides 디렉토리에 `package.json`이 없으면 `npx slidev`가 매번 패키지를 다운로드한다. 30초~1분 이상 소요.

**해결**: 새 slides 디렉토리를 만들 때 반드시 `package.json` + `pnpm install`을 먼저 실행.

## @slidev/types 필수 설치

`setup/mermaid.ts`를 사용하려면 `@slidev/types` 패키지가 필요하다. `@slidev/cli`의 transitive dependency로 포함되지 **않으므로** 명시적 설치 필수.

```bash
pnpm add @slidev/types
```

**증상**: `[plugin:vite:import-analysis] Failed to resolve import "@slidev/types" from "setup/mermaid.ts"`
