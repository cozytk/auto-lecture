// ─── src/components/AlbumGallery.jsx ───
// 포토 갤러리 (도전 10)
// Props: userId (number)

import { useState, useEffect } from "react";
import { Skeleton } from "./ui/Skeleton";

const API = "https://jsonplaceholder.typicode.com";

// ── Photo Modal (스타일 완성됨) ──
function PhotoModal({ photo, onClose }) {
  if (!photo) return null;
  return (
    <div
      className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4"
      onClick={onClose}
    >
      <div
        className="bg-white rounded-2xl p-2 max-w-md w-full shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        <img src={photo.url} alt={photo.title} className="w-full rounded-xl" />
        <p className="text-xs text-slate-500 p-3 text-center">{photo.title}</p>
      </div>
    </div>
  );
}

export default function AlbumGallery({ userId }) {
  // TODO (도전 10-a): albums, photos, selectedAlbum, selectedPhoto 상태를 만드세요
  const [albums, setAlbums] = useState([]);
  const [photos, setPhotos] = useState([]);
  const [selectedAlbum, setSelectedAlbum] = useState(null);
  const [selectedPhoto, setSelectedPhoto] = useState(null);
  const [loading, setLoading] = useState(false);

  // TODO (도전 10-b): userId가 바뀔 때 앨범 목록을 fetch하세요
  //   - URL: `${API}/albums?userId=${userId}`
  useEffect(() => {
    if (!userId) return;
    // 여기에 fetch 로직을 구현하세요
  }, [userId]);

  // TODO (도전 10-c): 앨범 클릭 시 해당 앨범의 사진을 fetch하세요
  //   - URL: `${API}/albums/${album.id}/photos`
  //   - 사진이 많으니 .slice(0, 12)로 12개만 표시하세요
  const openAlbum = async (album) => {
    setSelectedAlbum(album);
    // 여기에 fetch 로직을 구현하세요
  };

  if (!userId) return null;

  return (
    <div className="space-y-3">
      {!selectedAlbum ? (
        /* ── 앨범 목록 ── */
        <div className="grid grid-cols-2 gap-2">
          {albums.length === 0 ? (
            <p className="col-span-2 text-sm text-slate-400 text-center py-8">
              No albums loaded yet.
            </p>
          ) : (
            albums.map((a) => (
              <button
                key={a.id}
                onClick={() => openAlbum(a)}
                className="p-3 rounded-xl border border-slate-200 bg-white hover:border-indigo-300 hover:shadow-sm transition text-left"
              >
                <div className="text-2xl mb-1">📁</div>
                <div className="text-xs font-medium text-slate-700 line-clamp-2">
                  {a.title}
                </div>
              </button>
            ))
          )}
        </div>
      ) : (
        /* ── 사진 그리드 ── */
        <div className="space-y-3">
          <button
            onClick={() => setSelectedAlbum(null)}
            className="text-xs text-indigo-500 hover:text-indigo-700 font-medium"
          >
            ← Back to albums
          </button>
          <h4 className="text-sm font-semibold text-slate-700">
            {selectedAlbum.title}
          </h4>
          {loading ? (
            <div className="grid grid-cols-3 gap-2">
              {[1, 2, 3, 4, 5, 6].map((i) => (
                <Skeleton key={i} className="aspect-square" />
              ))}
            </div>
          ) : (
            <div className="grid grid-cols-3 gap-2">
              {photos.map((p) => (
                <button
                  key={p.id}
                  onClick={() => setSelectedPhoto(p)}
                  className="aspect-square rounded-lg overflow-hidden border border-slate-200 hover:border-indigo-400 transition"
                >
                  <img
                    src={p.thumbnailUrl}
                    alt={p.title}
                    className="w-full h-full object-cover"
                  />
                </button>
              ))}
            </div>
          )}
        </div>
      )}
      <PhotoModal
        photo={selectedPhoto}
        onClose={() => setSelectedPhoto(null)}
      />
    </div>
  );
}
