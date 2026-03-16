// ─── src/types.ts ───
// 프로젝트 전체에서 사용하는 타입 정의

/** JSONPlaceholder User */
export interface User {
  id: number;
  name: string;
  username: string;
  email: string;
  phone: string;
  website: string;
  address: {
    street: string;
    suite: string;
    city: string;
    zipcode: string;
  };
  company: {
    name: string;
    catchPhrase: string;
    bs: string;
  };
}

/** JSONPlaceholder Post */
export interface Post {
  id: number;
  userId: number;
  title: string;
  body: string;
}

/** JSONPlaceholder Comment */
export interface Comment {
  id: number;
  postId: number;
  name: string;
  email: string;
  body: string;
}

/** JSONPlaceholder Todo */
export interface Todo {
  id: number;
  userId: number;
  title: string;
  completed: boolean;
}

/** JSONPlaceholder Album */
export interface Album {
  id: number;
  userId: number;
  title: string;
}

/** JSONPlaceholder Photo */
export interface Photo {
  id: number;
  albumId: number;
  title: string;
  url: string;
  thumbnailUrl: string;
}

/** 대시보드 통계 */
export interface DashboardStats {
  posts: number;
  comments: number;
  todoDone: number;
  todoTotal: number;
  albums: number;
  photos: number;
}

/**
 * 통계 업데이트 콜백 (도전 과제)
 *
 * 자식 컴포넌트에서 특정 통계를 갱신할 때 사용합니다.
 * 예: onStatsUpdate("todoDone", 13)  → todoDone을 13으로 변경
 * 예: onStatsUpdate("posts", prev => prev + 1)  → posts를 1 증가
 */
export type StatsUpdateFn = (
  key: keyof DashboardStats,
  value: number | ((prev: number) => number)
) => void;
