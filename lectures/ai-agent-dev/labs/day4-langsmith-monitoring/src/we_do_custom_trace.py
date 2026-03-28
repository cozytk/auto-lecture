"""
Day 4 실습 - WE DO: 커스텀 Trace 및 메트릭 수집

전체가 함께 커스텀 Trace를 설정하고 LangSmith API로 메트릭을 조회한다.
"""

import os
from datetime import datetime, timedelta
from langsmith import Client, traceable
from langsmith.run_helpers import get_current_run_tree
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage


# =============================================================================
# 1. LangSmith 클라이언트 설정
# =============================================================================

ls_client = Client(api_key=os.environ.get("LANGSMITH_API_KEY", ""))
PROJECT_NAME = os.environ.get("LANGSMITH_PROJECT", "day4-monitoring-lab")


# =============================================================================
# 2. 메타데이터가 풍부한 커스텀 Trace
# =============================================================================

@traceable(
    name="cs_agent_v2",
    run_type="chain",
    metadata={
        "agent_version": "2.0.0",
        "environment": "lab",
        "team": "day4-class"
    },
    tags=["lab", "customer-support"]
)
def customer_support_agent(user_id: str, query: str, session_id: str) -> dict:
    """고객 지원 Agent - 메타데이터 태깅 예시"""

    # 현재 Run에 동적 메타데이터 추가
    run_tree = get_current_run_tree()
    if run_tree:
        run_tree.extra = run_tree.extra or {}
        run_tree.extra["metadata"] = run_tree.extra.get("metadata", {})
        run_tree.extra["metadata"].update({
            "user_id": user_id,
            "session_id": session_id,
            "query_category": classify_query(query),
            "query_length": len(query),
        })

    # Agent 실행
    answer = generate_cs_response(query)

    return {
        "status": "success",
        "answer": answer,
        "user_id": user_id,
    }


@traceable(name="classify_query", run_type="chain")
def classify_query(query: str) -> str:
    """질문 분류"""
    keywords = {
        "환불": "refund",
        "배송": "delivery",
        "교환": "exchange",
        "추천": "recommendation",
    }
    for keyword, category in keywords.items():
        if keyword in query:
            return category
    return "general"


@traceable(name="generate_cs_response", run_type="chain")
def generate_cs_response(query: str) -> str:
    """고객 지원 응답 생성"""
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        api_key=os.environ["OPENAI_API_KEY"],
        temperature=0
    )

    response = llm.invoke([
        SystemMessage(content=(
            "당신은 친절한 고객 지원 상담원입니다. "
            "간결하고 정확하게 답변하세요. "
            "확인되지 않은 정보는 안내하지 마세요."
        )),
        HumanMessage(content=query)
    ])

    return response.content


# =============================================================================
# 3. LangSmith API로 메트릭 조회
# =============================================================================

def get_recent_runs(hours: int = 1, limit: int = 50) -> list:
    """최근 N시간 내 실행 기록 조회"""
    try:
        runs = list(ls_client.list_runs(
            project_name=PROJECT_NAME,
            start_time=datetime.now() - timedelta(hours=hours),
            is_root=True,
            limit=limit,
        ))
        return runs
    except Exception as e:
        print(f"  LangSmith 조회 실패: {e}")
        return []


def compute_metrics(runs: list) -> dict:
    """실행 기록에서 메트릭 산출"""
    if not runs:
        return {"message": "조회된 실행 기록이 없습니다"}

    total = len(runs)
    errors = sum(1 for r in runs if r.error)
    success = total - errors

    latencies = []
    total_tokens = 0

    for run in runs:
        if run.end_time and run.start_time:
            lat = (run.end_time - run.start_time).total_seconds() * 1000
            latencies.append(lat)

        if run.total_tokens:
            total_tokens += run.total_tokens

    latencies.sort()

    metrics = {
        "total_runs": total,
        "success_count": success,
        "error_count": errors,
        "success_rate": round(success / total, 4) if total > 0 else 0,
        "total_tokens": total_tokens,
        "avg_tokens_per_run": round(total_tokens / total) if total > 0 else 0,
    }

    if latencies:
        metrics.update({
            "latency_avg_ms": round(sum(latencies) / len(latencies), 1),
            "latency_p50_ms": round(latencies[len(latencies) // 2], 1),
            "latency_p95_ms": round(latencies[int(len(latencies) * 0.95)], 1) if len(latencies) > 1 else round(latencies[0], 1),
            "latency_min_ms": round(min(latencies), 1),
            "latency_max_ms": round(max(latencies), 1),
        })

    return metrics


def get_error_summary(runs: list) -> list[dict]:
    """에러 요약"""
    errors = []
    for run in runs:
        if run.error:
            errors.append({
                "run_id": str(run.id),
                "name": run.name,
                "error": run.error[:200] if run.error else "unknown",
                "time": run.start_time.isoformat() if run.start_time else None,
            })
    return errors


# =============================================================================
# 4. 함께 실습하기
# =============================================================================

def run_demo():
    """커스텀 Trace + 메트릭 조회 시연"""
    print("=" * 60)
    print("WE DO: 커스텀 Trace 및 메트릭 수집")
    print("=" * 60)

    # --- Agent 실행 (Trace 생성) ---
    print("\n--- 1. Agent 실행 (Trace 생성) ---")

    test_queries = [
        ("user_001", "환불하고 싶어요. 주문번호 ORD-1234입니다.", "sess_001"),
        ("user_002", "배송이 아직 안 왔는데 언제 오나요?", "sess_002"),
        ("user_003", "이 제품 추천해줄 수 있나요?", "sess_003"),
    ]

    for user_id, query, session_id in test_queries:
        print(f"  [{user_id}] {query[:30]}...")
        result = customer_support_agent(user_id, query, session_id)
        print(f"    -> {result['answer'][:60]}...")

    # --- 메트릭 조회 ---
    print("\n--- 2. 메트릭 조회 ---")
    print("  최근 1시간 내 실행 기록 조회 중...")

    runs = get_recent_runs(hours=1)
    print(f"  조회된 실행: {len(runs)}건")

    if runs:
        metrics = compute_metrics(runs)
        print("\n  [운영 메트릭]")
        for key, value in metrics.items():
            print(f"    {key}: {value}")

        # 에러 요약
        errors = get_error_summary(runs)
        if errors:
            print(f"\n  [에러 요약] {len(errors)}건")
            for e in errors[:5]:
                print(f"    - {e['name']}: {e['error'][:80]}")
        else:
            print("\n  [에러 요약] 에러 없음")
    else:
        print("  (실행 기록이 아직 LangSmith에 반영되지 않았을 수 있습니다)")
        print("  -> 잠시 후 다시 시도하거나, LangSmith 대시보드에서 직접 확인하세요")

    print("\n" + "=" * 60)
    print("확인사항:")
    print(f"  1. https://smith.langchain.com/ 에서 '{PROJECT_NAME}' 프로젝트 확인")
    print("  2. 'cs_agent_v2' Trace 클릭 -> 내부 span 확인")
    print("  3. 메타데이터 탭에서 user_id, session_id 등 확인")
    print("=" * 60)


if __name__ == "__main__":
    run_demo()
