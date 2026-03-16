// ─── src/App.jsx ───
// Mini Social Dashboard — 메인 엔트리포인트
// 아래의 TODO를 순서대로 구현하세요!

import { useState, useEffect } from "react";

// 컴포넌트 import
import UserCard from "./components/UserCard";
import PostCard from "./components/PostCard";
import PostForm from "./components/PostForm";
import TodoSection from "./components/TodoSection";
import SearchBar from "./components/SearchBar";
import AlbumGallery from "./components/AlbumGallery";
import TabButton from "./components/ui/TabButton";
import StatCard from "./components/ui/StatCard";
import { CardSkeleton } from "./components/ui/Skeleton";

const API = "https://jsonplaceholder.typicode.com";

export default function App() {
  // ── State 선언 ──

  // TODO (필수 1-a): users 상태를 만드세요
  // const [users, setUsers] = useState([])

  // TODO (필수 1-b): selectedUser 상태를 만드세요 (초기값: null)

  // TODO (필수 2-a): posts 상태를 만드세요

  const [search, setSearch] = useState("");
  const [tab, setTab] = useState("posts");
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState(null); // 도전 8

  // ── 데이터 Fetch ──

  // TODO (필수 1-c): 컴포넌트 마운트 시 사용자 목록을 fetch하세요
  //   - URL: `${API}/users`
  //   - 응답을 users state에 저장
  //   - 완료 후 setLoading(false)
  useEffect(() => {
    // 여기에 fetch 로직을 구현하세요
  }, []);

  // TODO (필수 2-b): selectedUser가 바뀔 때마다 게시글을 fetch하세요
  //   - URL: `${API}/posts?userId=${selectedUser.id}`
  //   - selectedUser가 null이면 fetch하지 마세요
  //   - 의존성 배열: [selectedUser]
  useEffect(() => {
    if (!selectedUser) return; // TODO: selectedUser 변수가 없으면 에러납니다! 위의 state를 먼저 만드세요
    // 여기에 fetch 로직을 구현하세요
  }, [/* TODO: 의존성 */]);

  // TODO (도전 8): 대시보드 통계를 위해 모든 리소스를 한번에 fetch하세요
  //   - Promise.all([
  //       fetch(`${API}/posts`).then(r => r.json()),
  //       fetch(`${API}/comments`).then(r => r.json()),
  //       fetch(`${API}/todos`).then(r => r.json()),
  //       fetch(`${API}/albums`).then(r => r.json()),
  //       fetch(`${API}/photos`).then(r => r.json()),
  //     ])
  //   - 결과에서 각 리소스의 .length를 stats에 저장

  // ── 이벤트 핸들러 ──

  // TODO (필수 3): 게시글 추가 함수
  //   - POST `${API}/posts`로 요청
  //   - body: JSON.stringify({ title, body, userId: selectedUser.id })
  //   - headers: { "Content-Type": "application/json" }
  //   - 응답 받은 후 posts state 앞에 추가 (id는 Date.now()로 대체)
  const addPost = async ({ title, body }) => {
    // 여기에 구현하세요
  };

  // TODO (필수 4): 게시글 삭제 함수
  //   - DELETE `${API}/posts/${id}`로 요청
  //   - posts state에서 해당 id 제거
  const deletePost = async (id) => {
    // 여기에 구현하세요
  };

  // TODO (도전 9): 검색 필터링
  //   - posts에서 search 키워드로 title과 body를 필터링하세요
  //   - 힌트: useMemo를 사용하면 성능이 좋아집니다
  const filteredPosts = []; // TODO: 필터링된 게시글 목록으로 교체

  // ── 렌더링 ──

  // 임시 변수 (TODO 구현 전 에러 방지용 — state 만든 후 삭제하세요)
  const users = [];
  const selectedUser = null;
  const posts = [];

  return (
    <div className="min-h-screen bg-slate-50 font-sans">
      {/* ── Header ── */}
      <header className="bg-white border-b border-slate-200 sticky top-0 z-30">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 bg-indigo-500 rounded-lg flex items-center justify-center">
              <span className="text-white text-sm font-bold">S</span>
            </div>
            <h1 className="text-lg font-bold text-slate-800">
              Social Dashboard
            </h1>
          </div>
          <div className="text-xs text-slate-400 bg-slate-100 px-3 py-1.5 rounded-lg font-mono">
            JSONPlaceholder API
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-6 py-6">
        {/* ── Dashboard Stats (도전 8) ── */}
        <div className="grid grid-cols-3 md:grid-cols-6 gap-3 mb-6">
          <StatCard
            icon="👥"
            label="Users"
            value={users.length || "—"}
            color="blue"
          />
          <StatCard
            icon="📝"
            label="Posts"
            value={stats?.posts ?? "—"}
            color="purple"
          />
          <StatCard
            icon="💬"
            label="Comments"
            value={stats?.comments ?? "—"}
            color="cyan"
          />
          <StatCard
            icon="✅"
            label="Todos"
            value={
              stats ? `${stats.todoDone}/${stats.todoTotal}` : "—"
            }
            color="emerald"
          />
          <StatCard
            icon="📁"
            label="Albums"
            value={stats?.albums ?? "—"}
            color="amber"
          />
          <StatCard
            icon="🖼️"
            label="Photos"
            value={stats?.photos ?? "—"}
            color="rose"
          />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* ── Sidebar: User List (필수 1) ── */}
          <div className="lg:col-span-3 space-y-3">
            <h2 className="text-xs font-bold text-slate-400 uppercase tracking-wider px-1">
              Users
            </h2>
            {loading ? (
              <div className="space-y-2">
                {[1, 2, 3, 4, 5].map((i) => (
                  <CardSkeleton key={i} />
                ))}
              </div>
            ) : (
              <div className="space-y-2">
                {/* TODO (필수 1-d): users.map()으로 UserCard를 렌더링하세요 */}
                {/* Props: user, selected (selectedUser?.id === user.id), onClick */}
                <p className="text-sm text-slate-400 text-center py-4">
                  TODO: UserCard를 렌더링하세요
                </p>
              </div>
            )}
          </div>

          {/* ── Main Content (필수 2~4, 도전 9~10) ── */}
          <div className="lg:col-span-9">
            {!selectedUser ? (
              /* 사용자 미선택 상태 */
              <div className="flex items-center justify-center h-64 bg-white rounded-2xl border border-slate-200">
                <div className="text-center text-slate-400">
                  <div className="text-4xl mb-3">👈</div>
                  <p className="text-sm font-medium">
                    Select a user to explore
                  </p>
                </div>
              </div>
            ) : (
              /* 사용자 선택됨 */
              <div className="space-y-4">
                {/* User Header */}
                <div className="bg-white rounded-2xl border border-slate-200 p-5">
                  <div className="flex items-center gap-4">
                    <div className="w-14 h-14 bg-indigo-500 rounded-2xl flex items-center justify-center text-white text-xl font-bold">
                      {selectedUser.name.charAt(0)}
                    </div>
                    <div>
                      <h2 className="text-lg font-bold text-slate-800">
                        {selectedUser.name}
                      </h2>
                      <p className="text-sm text-slate-500">
                        @{selectedUser.username} ·{" "}
                        {selectedUser.company.name}
                      </p>
                      <p className="text-xs text-slate-400">
                        {selectedUser.email} · {selectedUser.phone}
                      </p>
                    </div>
                  </div>
                </div>

                {/* Tabs */}
                <div className="flex gap-1 bg-white rounded-xl border border-slate-200 p-1.5">
                  <TabButton
                    active={tab === "posts"}
                    onClick={() => setTab("posts")}
                  >
                    📝 Posts
                  </TabButton>
                  <TabButton
                    active={tab === "todos"}
                    onClick={() => setTab("todos")}
                  >
                    ✅ Todos
                  </TabButton>
                  <TabButton
                    active={tab === "albums"}
                    onClick={() => setTab("albums")}
                  >
                    🖼️ Albums
                  </TabButton>
                </div>

                {/* Tab Content */}
                <div className="bg-white rounded-2xl border border-slate-200 p-5 space-y-4">
                  {tab === "posts" && (
                    <>
                      {/* 도전 9: SearchBar */}
                      <SearchBar value={search} onChange={setSearch} />

                      {/* 필수 3: PostForm */}
                      <PostForm onSubmit={addPost} />

                      {/* 필수 2, 4: PostCard 목록 */}
                      <div className="space-y-3">
                        {/* TODO: filteredPosts (또는 posts)를 map으로 렌더링 */}
                        {/* <PostCard key={...} post={...} onDelete={deletePost} /> */}
                        <p className="text-sm text-slate-400 text-center py-8">
                          TODO: PostCard를 렌더링하세요
                        </p>
                      </div>
                    </>
                  )}
                  {tab === "todos" && (
                    <TodoSection userId={selectedUser.id} />
                  )}
                  {tab === "albums" && (
                    <AlbumGallery userId={selectedUser.id} />
                  )}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
