#!/bin/bash
# 자동 수정 루프 스크립트 (완성 버전)
# opencode를 사용하여 테스트가 모두 통과할 때까지 자동으로 코드를 수정합니다.

set -e

MAX_ATTEMPTS=5
ATTEMPT=0
LOG_FILE="auto_fix_log.txt"
TEST_OUTPUT_FILE="test_output.txt"

echo "자동 수정 루프 시작 - $(date)" | tee "$LOG_FILE"
echo "최대 시도 횟수: $MAX_ATTEMPTS" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

while [ $ATTEMPT -lt $MAX_ATTEMPTS ]; do
    ATTEMPT=$((ATTEMPT + 1))
    echo "=== 시도 $ATTEMPT/$MAX_ATTEMPTS ===" | tee -a "$LOG_FILE"
    echo "시작 시각: $(date)" | tee -a "$LOG_FILE"

    # 테스트 실행 및 결과 저장
    echo "테스트 실행 중..." | tee -a "$LOG_FILE"
    python -m unittest test_vocab -v 2>&1 | tee "$TEST_OUTPUT_FILE" | tee -a "$LOG_FILE"
    TEST_EXIT_CODE=${PIPESTATUS[0]}

    # 테스트 통과 여부 확인
    if [ $TEST_EXIT_CODE -eq 0 ]; then
        echo "" | tee -a "$LOG_FILE"
        echo "모든 테스트 통과! 자동 수정 완료." | tee -a "$LOG_FILE"
        echo "총 시도 횟수: $ATTEMPT" | tee -a "$LOG_FILE"
        echo "완료 시각: $(date)" | tee -a "$LOG_FILE"
        exit 0
    fi

    # 테스트 실패 - 에이전트에게 수정 요청
    echo "" | tee -a "$LOG_FILE"
    echo "테스트 실패. 에이전트에게 수정 요청 중..." | tee -a "$LOG_FILE"

    FAILED_TESTS=$(grep -E "^FAIL:|^ERROR:" "$TEST_OUTPUT_FILE" || true)
    echo "실패한 테스트: $FAILED_TESTS" | tee -a "$LOG_FILE"

    # opencode로 에이전트 실행 (비대화형 모드)
    PROMPT="다음 Python 테스트가 실패했습니다. 코드를 분석하고 수정해주세요.

실패한 테스트 출력:
$(cat $TEST_OUTPUT_FILE)

수정 대상 파일: vocab.py, quiz.py, stats.py
규칙:
1. test_vocab.py는 수정하지 마세요 (테스트는 올바릅니다)
2. 버그가 있는 코드만 수정하세요
3. 수정 후 이유를 간단히 설명해주세요"

    opencode run "$PROMPT" 2>&1 | tee -a "$LOG_FILE"

    echo "" | tee -a "$LOG_FILE"
    echo "에이전트 수정 완료. 다음 시도를 진행합니다." | tee -a "$LOG_FILE"
    echo "" | tee -a "$LOG_FILE"
done

echo "=== 최대 시도 횟수($MAX_ATTEMPTS) 초과 ===" | tee -a "$LOG_FILE"
echo "수동으로 코드를 확인해주세요." | tee -a "$LOG_FILE"
echo "로그 파일: $LOG_FILE" | tee -a "$LOG_FILE"
exit 1
