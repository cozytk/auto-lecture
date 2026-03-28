#!/bin/bash
# Slidev 서버를 tmux 세션으로 시작/중지/상태확인
# Usage:
#   scripts/slidev-serve.sh start <slides-dir> [file] [--port 3030]
#   scripts/slidev-serve.sh stop [--port 3030]
#   scripts/slidev-serve.sh status
#   scripts/slidev-serve.sh restart <slides-dir> [file] [--port 3030]

DEFAULT_PORT=3030

cmd="${1:-status}"
shift

# Extract --port first
port="$DEFAULT_PORT"
args=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    --port)
      port="$2"
      shift 2
      ;;
    *)
      args+=("$1")
      shift
      ;;
  esac
done

# Positional: slides_dir, slide_file
slides_dir="${args[0]:-}"
slide_file="${args[1]:-slides.md}"

SESSION="slidev-${port}"

case "$cmd" in
  start)
    if [ -z "$slides_dir" ]; then
      echo "Usage: $0 start <slides-dir> [file] [--port PORT]"
      exit 1
    fi
    abs_dir="$(cd "$slides_dir" 2>/dev/null && pwd)"
    if [ ! -d "$abs_dir" ]; then
      echo "Error: directory not found: $slides_dir"
      exit 1
    fi

    # Kill existing session for this port
    tmux kill-session -t "$SESSION" 2>/dev/null
    lsof -ti:"$port" | xargs kill -9 2>/dev/null
    sleep 1

    # Build run command
    if [ "$slide_file" = "slides.md" ] && [ -f "$abs_dir/package.json" ] && grep -q '"dev"' "$abs_dir/package.json"; then
      run_cmd="pnpm dev -- --port $port"
    else
      run_cmd="npx slidev $slide_file --port $port"
    fi

    echo "Starting: $run_cmd"
    echo "  dir: $abs_dir"

    # Start tmux session (provides TTY — required for Slidev dev server)
    tmux new-session -d -s "$SESSION" -c "$abs_dir" "$run_cmd"

    # Wait for server (1st check)
    ready=false
    for i in $(seq 1 30); do
      if curl -s -o /dev/null -w "%{http_code}" "http://localhost:$port/1" 2>/dev/null | grep -q 200; then
        ready=true
        break
      fi
      if ! tmux has-session -t "$SESSION" 2>/dev/null; then
        echo "Error: Slidev process died during startup"
        echo "Try manually: cd $abs_dir && $run_cmd"
        exit 1
      fi
      sleep 1
    done

    if [ "$ready" = false ]; then
      echo "Error: server not responding after 30s"
      echo "tmux log:"
      tmux capture-pane -t "$SESSION" -p 2>/dev/null | tail -10
      exit 1
    fi

    # 2nd verification
    sleep 2
    if ! tmux has-session -t "$SESSION" 2>/dev/null; then
      echo "Error: Slidev crashed shortly after start"
      exit 1
    fi
    http2=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:$port/1" 2>/dev/null)
    if [ "$http2" != "200" ]; then
      echo "Error: server stopped responding (HTTP: $http2)"
      exit 1
    fi

    echo "Slidev running: http://localhost:$port"
    echo "  tmux: tmux attach -t $SESSION"
    ;;

  stop)
    tmux list-sessions -F '#{session_name}' 2>/dev/null | grep '^slidev-' | while read s; do
      tmux kill-session -t "$s" 2>/dev/null
      echo "Killed session: $s"
    done
    lsof -ti:"$port" | xargs kill -9 2>/dev/null
    echo "Slidev stopped"
    ;;

  status)
    count=$(tmux list-sessions -F '#{session_name}' 2>/dev/null | grep -c '^slidev-')
    if [ "$count" = "0" ]; then
      echo "No Slidev sessions running"
    else
      tmux list-sessions -F '#{session_name}' 2>/dev/null | grep '^slidev-' | while read s; do
        p="${s#slidev-}"
        http=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:$p/1" 2>/dev/null)
        if [ "$http" = "200" ]; then
          echo "Slidev on port $p — http://localhost:$p (session: $s)"
        else
          echo "Session $s exists but not responding (HTTP: $http)"
        fi
      done
    fi
    ;;

  restart)
    "$0" stop --port "$port"
    sleep 1
    "$0" start "$slides_dir" "$slide_file" --port "$port"
    ;;

  *)
    echo "Usage: $0 {start|stop|status|restart} [slides-dir] [file] [--port PORT]"
    exit 1
    ;;
esac
