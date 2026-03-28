"""
프로젝트 설정 관리

환경변수와 모델/RAG/Tool 설정을 중앙에서 관리한다.
.env 파일에서 API 키를 로드하고, 프로젝트 전반에서 사용하는 상수를 정의한다.
"""

import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()


# ============================================================
# API 키
# ============================================================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY", "")

# ============================================================
# LLM 설정
# ============================================================
LLM_MODEL = "gpt-4o"  # 사용할 LLM 모델 (gpt-4o, claude-3-5-sonnet 등)
LLM_TEMPERATURE = 0.0  # 0.0 = 결정론적, 1.0 = 창의적
LLM_MAX_TOKENS = 2048  # 최대 출력 토큰

# ============================================================
# RAG 설정 (ChromaDB)
# ============================================================
CHROMA_COLLECTION_NAME = "my_documents"  # ChromaDB 컬렉션 이름
CHROMA_PERSIST_DIR = "./data/chroma_db"  # ChromaDB 저장 경로
CHUNK_SIZE = 800  # 문서 Chunk 크기 (문자 수)
CHUNK_OVERLAP = 200  # Chunk 간 오버랩 (문자 수)
RETRIEVAL_TOP_K = 5  # 검색 결과 상위 K개

# ============================================================
# Agent 설정
# ============================================================
AGENT_RECURSION_LIMIT = 10  # LangGraph 최대 반복 횟수
AGENT_TIMEOUT_SECONDS = 30  # Agent 전체 타임아웃 (초)

# ============================================================
# LangSmith 설정
# ============================================================
LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT", "day5-mvp")

# ============================================================
# System Prompt
# ============================================================
SYSTEM_PROMPT = """당신은 [프로젝트 목적]을 위한 AI Agent입니다.

역할:
- [Agent의 주요 역할을 구체적으로 기술]

제약:
- [Agent가 하지 말아야 할 것]
- 확실하지 않은 정보는 "확인이 필요합니다"라고 답변

출력 형식:
- [기대하는 출력 형식 설명]
"""


def validate_config():
    """필수 설정값 검증"""
    errors = []

    if not OPENAI_API_KEY and "gpt" in LLM_MODEL:
        errors.append("OPENAI_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요.")

    if not ANTHROPIC_API_KEY and "claude" in LLM_MODEL:
        errors.append("ANTHROPIC_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요.")

    if errors:
        print("=== 설정 오류 ===")
        for error in errors:
            print(f"  - {error}")
        print("=================")
        return False

    return True


if __name__ == "__main__":
    if validate_config():
        print("설정 검증 완료. 모든 필수값이 설정되어 있습니다.")
        print(f"  LLM 모델: {LLM_MODEL}")
        print(f"  Temperature: {LLM_TEMPERATURE}")
        print(f"  RAG Collection: {CHROMA_COLLECTION_NAME}")
        print(f"  LangSmith Project: {LANGSMITH_PROJECT}")
    else:
        print("설정을 수정한 후 다시 실행하세요.")
