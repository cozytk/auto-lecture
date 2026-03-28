# 순정(vanilla) OpenCode 환경 설정
# oh-my-opencode 플러그인을 비활성화하고 기본 상태로 실행합니다.
#
# 사용법: source env.sh

export XDG_CONFIG_HOME="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)/.config"
echo "OpenCode 순정 모드 활성화 (config: $XDG_CONFIG_HOME/opencode)"
