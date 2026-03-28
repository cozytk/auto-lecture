"""
LangGraph 기반 단순 RAG 파이프라인
- 문서 로드 → 청킹 → 벡터 저장 → 검색 → 생성
"""

from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.graph import START, StateGraph
from typing_extensions import TypedDict

# ── 1. 샘플 문서 준비 ──
raw_docs = [
    Document(page_content="LangGraph는 LLM 기반 상태 기반 에이전트를 구축하는 프레임워크입니다. 노드와 엣지로 구성된 그래프 구조를 사용합니다."),
    Document(page_content="RAG(Retrieval-Augmented Generation)는 검색 결과를 컨텍스트로 활용하여 LLM의 응답 품질을 높이는 기법입니다."),
    Document(page_content="벡터 스토어는 텍스트를 임베딩 벡터로 변환하여 저장하고, 유사도 검색을 통해 관련 문서를 빠르게 찾습니다."),
    Document(page_content="LangChain은 LLM 애플리케이션 개발을 위한 프레임워크로, 체인, 에이전트, 도구 등 다양한 추상화를 제공합니다."),
]

# ── 2. 청킹 & 벡터 스토어 구성 ──
text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=50)
doc_splits = text_splitter.split_documents(raw_docs)

vectorstore = InMemoryVectorStore.from_documents(
    documents=doc_splits,
    embedding=OpenAIEmbeddings(model="text-embedding-3-small"),
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

# ── 3. LLM & 프롬프트 ──
llm = ChatOpenAI(model="gpt-5.4")

prompt = ChatPromptTemplate.from_template(
    """다음 컨텍스트를 참고하여 질문에 답하세요. 컨텍스트에 없는 내용은 모른다고 답하세요.

컨텍스트:
{context}

질문: {question}
"""
)


# ── 4. LangGraph 상태 & 노드 정의 ──
class State(TypedDict):
    question: str
    context: list[Document]
    answer: str


def retrieve(state: State) -> dict:
    docs = retriever.invoke(state["question"])
    return {"context": docs}


def generate(state: State) -> dict:
    context_text = "\n\n".join(doc.page_content for doc in state["context"])
    messages = prompt.invoke({"context": context_text, "question": state["question"]})
    response = llm.invoke(messages)
    return {"answer": response.content}


# ── 5. 그래프 구성 ──
graph = StateGraph(State)
graph.add_node("retrieve", retrieve)
graph.add_node("generate", generate)

graph.add_edge(START, "retrieve")
graph.add_edge("retrieve", "generate")

app = graph.compile()

# ── 6. 실행 ──
if __name__ == "__main__":
    result = app.invoke({"question": "RAG란 무엇인가요?"})
    print("질문:", result["question"])
    print("답변:", result["answer"])
