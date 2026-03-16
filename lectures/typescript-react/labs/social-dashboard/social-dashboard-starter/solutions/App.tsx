// ─── src/App.tsx (정답) ───

import { useState, useEffect, useMemo } from "react";
import type { User, Post, DashboardStats, StatsUpdateFn } from "./types";

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

type TabKey = "posts" | "todos" | "albums";

export default function App() {
  // ── State (필수 1-a, 1-b, 2-a) ──
  const [users, setUsers] = useState<User[]>([]);
  const [selectedUser, setSelectedUser] = useState<User | null>(null);
  const [posts, setPosts] = useState<Post[]>([]);
  const [search, setSearch] = useState("");
  const [tab, setTab] = useState<TabKey>("posts");
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState<DashboardStats | null>(null);

  // ── 필수 1-c: 사용자 목록 fetch ──
  useEffect(() => {
    const fetchUsers = async () => {
      const res = await fetch(`${API}/users`);
      const data: User[] = await res.json();
      setUsers(data);
      setLoading(false);
    };
    fetchUsers();
  }, []);

  // ── 필수 2-b: 선택된 사용자의 게시글 fetch ──
  useEffect(() => {
    if (!selectedUser) return;
    const fetchPosts = async () => {
      const res = await fetch(`${API}/posts?userId=${selectedUser.id}`);
      const data: Post[] = await res.json();
      setPosts(data);
    };
    fetchPosts();
  }, [selectedUser]);

  // ── 도전 8: 대시보드 통계 ──
  useEffect(() => {
    Promise.all([
      fetch(`${API}/posts`).then((r) => r.json()),
      fetch(`${API}/comments`).then((r) => r.json()),
      fetch(`${API}/todos`).then((r) => r.json()),
      fetch(`${API}/albums`).then((r) => r.json()),
      fetch(`${API}/photos`).then((r) => r.json()),
    ]).then(([posts, comments, todos, albums, photos]) => {
      setStats({
        posts: posts.length,
        comments: comments.length,
        todoDone: todos.filter((t: { completed: boolean }) => t.completed).length,
        todoTotal: todos.length,
        albums: albums.length,
        photos: photos.length,
      });
    });
  }, []);

  // ── 도전 11: 통계 업데이트 콜백 ──
  const handleStatsUpdate: StatsUpdateFn = (key, value) => {
    setStats((prev) => {
      if (!prev) return prev;
      const newValue = typeof value === "function" ? value(prev[key]) : value;
      return { ...prev, [key]: newValue };
    });
  };

  // ── 필수 3: 게시글 추가 ──
  const addPost = async ({ title, body }: { title: string; body: string }): Promise<void> => {
    const res = await fetch(`${API}/posts`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title, body, userId: selectedUser!.id }),
    });
    const newPost: Post = await res.json();
    setPosts((prev) => [{ ...newPost, id: Date.now() }, ...prev]);
    handleStatsUpdate("posts", (prev) => prev + 1); // 도전 11
  };

  // ── 필수 4: 게시글 삭제 ──
  const deletePost = async (id: number): Promise<void> => {
    await fetch(`${API}/posts/${id}`, { method: "DELETE" });
    setPosts((prev) => prev.filter((p) => p.id !== id));
    handleStatsUpdate("posts", (prev) => prev - 1); // 도전 11
  };

  // ── 도전 9: 검색 필터링 ──
  const filteredPosts = useMemo(() => {
    if (!search.trim()) return posts;
    const q = search.toLowerCase();
    return posts.filter(
      (p) =>
        p.title.toLowerCase().includes(q) ||
        p.body.toLowerCase().includes(q)
    );
  }, [posts, search]);

  return (
    <div className="min-h-screen bg-slate-50 font-sans">
      {/* Header */}
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
        {/* Dashboard Stats (도전 8) */}
        <div className="grid grid-cols-3 md:grid-cols-6 gap-3 mb-6">
          <StatCard icon="👥" label="Users" value={users.length || "—"} color="blue" />
          <StatCard icon="📝" label="Posts" value={stats?.posts ?? "—"} color="purple" />
          <StatCard icon="💬" label="Comments" value={stats?.comments ?? "—"} color="cyan" />
          <StatCard
            icon="✅"
            label="Todos"
            value={stats ? `${stats.todoDone}/${stats.todoTotal}` : "—"}
            color="emerald"
          />
          <StatCard icon="📁" label="Albums" value={stats?.albums ?? "—"} color="amber" />
          <StatCard icon="🖼️" label="Photos" value={stats?.photos ?? "—"} color="rose" />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* Sidebar: User List (필수 1-d) */}
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
                {users.map((user) => (
                  <UserCard
                    key={user.id}
                    user={user}
                    selected={selectedUser?.id === user.id}
                    onClick={setSelectedUser}
                  />
                ))}
              </div>
            )}
          </div>

          {/* Main Content */}
          <div className="lg:col-span-9">
            {!selectedUser ? (
              <div className="flex items-center justify-center h-64 bg-white rounded-2xl border border-slate-200">
                <div className="text-center text-slate-400">
                  <div className="text-4xl mb-3">👈</div>
                  <p className="text-sm font-medium">Select a user to explore</p>
                </div>
              </div>
            ) : (
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
                        @{selectedUser.username} · {selectedUser.company.name}
                      </p>
                      <p className="text-xs text-slate-400">
                        {selectedUser.email} · {selectedUser.phone}
                      </p>
                    </div>
                  </div>
                </div>

                {/* Tabs */}
                <div className="flex gap-1 bg-white rounded-xl border border-slate-200 p-1.5">
                  <TabButton active={tab === "posts"} onClick={() => setTab("posts")}>
                    📝 Posts
                  </TabButton>
                  <TabButton active={tab === "todos"} onClick={() => setTab("todos")}>
                    ✅ Todos
                  </TabButton>
                  <TabButton active={tab === "albums"} onClick={() => setTab("albums")}>
                    🖼️ Albums
                  </TabButton>
                </div>

                {/* Tab Content */}
                <div className="bg-white rounded-2xl border border-slate-200 p-5 space-y-4">
                  {tab === "posts" && (
                    <>
                      <SearchBar value={search} onChange={setSearch} />
                      <PostForm onSubmit={addPost} />
                      <div className="space-y-3">
                        {filteredPosts.length === 0 ? (
                          <p className="text-sm text-slate-400 text-center py-8">
                            No posts found.
                          </p>
                        ) : (
                          filteredPosts.map((post) => (
                            <PostCard
                              key={post.id}
                              post={post}
                              onDelete={deletePost}
                            />
                          ))
                        )}
                      </div>
                    </>
                  )}
                  {tab === "todos" && (
                    <TodoSection
                      userId={selectedUser.id}
                      onStatsUpdate={handleStatsUpdate}
                    />
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
