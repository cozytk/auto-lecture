#!/bin/bash
# 자동 수정 루프 스크립트 템플릿
# 학생이 TODO 부분을 완성해야 합니다.
#
# 목표: 에이전트를 반복 실행하여 모든 테스트가 통과할 때까지 자동으로 코드를 수정

set -e

MAX_ATTEMPTS=5
ATTEMPT=0
LOG_FILE="auto_fix_log.txt"

echo "자동 수정 루프 시작" | tee "$LOG_FILE"
echo "최대 시도 횟수: $MAX_ATTEMPTS" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

while [ $ATTEMPT -lt $MAX_ATTEMPTS ]; do
    ATTEMPT=$((ATTEMPT + 1))
    echo "=== 시도 $ATTEMPT/$MAX_ATTEMPTS ===" | tee -a "$LOG_FILE"
    echo "시작 시각: $(date)" | tee -a "$LOG_FILE"

    # TODO 1: 테스트를 실행하고 결과를 저장하세요
    # 힌트: python -m pytest test_vocab.py -v 2>&1 | tee -a "$LOG_FILE"
    # 힌트: 또는 python -m unittest test_vocab -v 2>&1 | tee -a "$LOG_FILE"

    # TODO 2: 테스트 결과를 확인하세요
    # 힌트: $? 변수로 마지막 명령어의 종료 코드를 확인할 수 있습니다
    # 종료 코드 0 = 성공, 1 = 실패

    # TODO 3: 모든 테스트가 통과하면 성공 메시지를 출력하고 종료하세요
    # 힌트: exit 0

    # TODO 4: 테스트가 실패하면 에이전트에게 수정을 요청하세요
    # 힌트: opencode run "테스트 실패 내용을 분석하고 코드를 수정해주세요"
    # 힌트: 실패한 테스트 내용을 에이전트에게 전달하면 더 정확하게 수정됩니다

    echo "" | tee -a "$LOG_FILE"
done

echo "=== 최대 시도 횟수 초과 ===" | tee -a "$LOG_FILE"
echo "수동으로 코드를 확인해주세요." | tee -a "$LOG_FILE"
exit 1
