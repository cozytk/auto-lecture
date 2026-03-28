---

name: tui-screenshot-capture

description: VHS를 사용하여 TUI 앱(OpenCode, htop 등)의 실제 터미널 실행 화면을 PNG/GIF로 캡처한다

model: sonnet

context: fork

allowed-tools: Read, Write, Edit, Bash, Glob

argument-hint: "[command] [output-dir]"

---

# TUI 스크린샷 캡처

VHS(charmbracelet)를 사용하여 TUI 앱의 실제 터미널 렌더링을 브라우저로 캡처한다.

## 입력

- `command`: 캡처할 TUI 명령어 (예: `opencode`, `htop`)
- `output-dir`: 스크린샷 저장 디렉토리 (기본: 현재 디렉토리)

## 실행 절차

### 1. VHS 설치 확인

```bash
which vhs || brew install charmbracelet/tap/vhs
```

VHS는 ttyd + ffmpeg를 자동 포함하며, Chrome이 필요하다.

### 2. tape 파일 생성

```
Set Shell zsh
Set Width 1200
Set Height 700
Set FontSize 14
Set Theme "Dracula"
Set Padding 20

Type@50ms "cd /path/to/project"
Enter
Sleep 1s
Type@50ms "opencode"
Enter
Sleep 8s
Screenshot opencode-tui.png
Sleep 1s
Type@30ms "질문 내용을 입력"
Enter
Sleep 25s
Screenshot opencode-response.png
Ctrl+C
Sleep 2s
```

### 3. 캡처 실행

```bash
# output-dir에서 실행 (Screenshot이 실행 디렉토리에 생성됨)
cd $output_dir
vhs capture.tape
```

### 4. 결과물 검증

생성된 PNG/GIF 파일을 Read 도구로 확인하여 TUI가 올바르게 렌더링되었는지 검증한다.

## 핵심 주의사항

1. `Screenshot` 명령은 **경로 없이 파일명만** 사용 — `/tmp/out.png` ❌, `out.png` ✅
2. tape 파일이 있는 디렉토리에서 `vhs`를 실행해야 Screenshot 파일이 그 디렉토리에 생성됨
3. tmux 안에서 VHS를 실행하면 **ttyd 포트 충돌** 가능 — 별도 터미널에서 실행하거나 재시도
4. TUI 앱은 렌더링 시간이 필요 — `Sleep 8s` 이상 충분히 대기

## 실패하는 방법들 (시도하지 말 것)

| 방법 | 왜 실패하는가 |
|------|-------------|
| `tmux capture-pane -e -p \| freeze` | ANSI 이스케이프를 freeze가 완벽히 렌더링 못함 |
| `freeze --execute "command"` | 단순 CLI 출력만 가능. TUI 앱은 캡처 불가 |
| `screencapture -l <windowid>` | macOS 접근성 권한 필요 |
| `ansi2html` → `wkhtmltoimage` | 의존성 체인이 길고 TUI 렌더링 품질 낮음 |
| `tmux capture-pane` 단독 | TUI의 내부 스크롤 영역을 캡처할 수 없음 |

## CLI 출력 캡처 (TUI가 아닌 경우)

TUI가 아닌 단순 CLI 출력도 VHS로 캡처 가능:
```
Type@50ms "just setup"
Enter
Sleep 5s
Screenshot capture-setup.png
```

`freeze`는 코드 파일을 꾸미는 용도로만 사용하고, 실제 실행 캡처에는 쓰지 않는다.
