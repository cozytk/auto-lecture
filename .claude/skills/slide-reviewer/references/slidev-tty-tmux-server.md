# Slidev TTY Requirement and tmux Server Management

Slidev의 dev server(Vite 기반)는 **stdin이 TTY가 아니면 즉시 종료**한다(exit code 0, 에러 메시지 없음). Claude Code의 Bash 도구는 TTY를 제공하지 않으므로, `&`, `nohup`, `run_in_background` 모두 실패한다. **tmux만이 해결책**이다.

## TTY 해결: tmux

```bash
# 올바른 방법: tmux가 pseudo-TTY를 제공
tmux new-session -d -s slidev-3030 -c "$slides_dir" "npx slidev $file --port 3030"

# 틀린 방법들 (전부 실패):
npx slidev &                    # TTY 없음 → 즉시 종료
nohup npx slidev &              # TTY 없음 → 즉시 종료
run_in_background: true         # TTY 없음 → 즉시 종료
```

## 서버 검증: 2단계

1단계 curl 체크는 **필요하지만 충분하지 않다**. 서버가 응답 직후 죽을 수 있으므로:

```bash
# 1차: curl 폴링 (최대 30초)
# 2차: 2초 후 tmux session + curl 재확인
sleep 2
tmux has-session -t "$SESSION" && curl -s localhost:$PORT/1 | grep 200
```

## 쉘 스크립트 인자 파싱: --flag 값을 안전하게 추출

```bash
# 올바른 패턴: --flag를 먼저 추출하고 나머지를 위치 인자로
args=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    --port) port="$2"; shift 2 ;;
    *)      args+=("$1"); shift ;;
  esac
done
slides_dir="${args[0]}"
slide_file="${args[1]:-slides.md}"
```

`for` 루프 + `prev_arg` + `continue` 패턴은 상태 관리가 깨지기 쉬우므로 **사용하지 않는다**.

## 참조 스크립트

현재 동작하는 스크립트: `scripts/slidev-serve.sh`
