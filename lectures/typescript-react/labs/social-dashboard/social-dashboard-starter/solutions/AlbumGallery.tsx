// ─── src/components/AlbumGallery.tsx (정답) ───

import { useState, useEffect } from "react";
import { Skeleton } from "./ui/Skeleton";
import type { Album, Photo } from "../types";

const API = "https://jsonplaceholder.typicode.com";

// ── Photo Modal ──
interface PhotoModalProps {
  photo: Photo | null;
  onClose: () => void;
}

function PhotoModal({ photo, onClose }: PhotoModalProps) {
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

// ── AlbumGallery ──
interface AlbumGalleryProps {
  userId: number;
}

export default function AlbumGallery({ userId }: AlbumGalleryProps) {
  const [albums, setAlbums] = useState<Album[]>([]);
  const [photos, setPhotos] = useState<Photo[]>([]);
  const [selectedAlbum, setSelectedAlbum] = useState<Album | null>(null);
  const [selectedPhoto, setSelectedPhoto] = useState<Photo | null>(null);
  const [loading, setLoading] = useState(false);

  // 도전 10-b: 앨범 목록 fetch
  useEffect(() => {
    if (!userId) return;
    const fetchAlbums = async () => {
      const res = await fetch(`${API}/albums?userId=${userId}`);
      const data: Album[] = await res.json();
      setAlbums(data);
    };
    fetchAlbums();
  }, [userId]);

  // 도전 10-c: 앨범 클릭 시 사진 fetch
  const openAlbum = async (album: Album): Promise<void> => {
    setSelectedAlbum(album);
    setLoading(true);
    const res = await fetch(`${API}/albums/${album.id}/photos`);
    const data: Photo[] = await res.json();
    setPhotos(data.slice(0, 12));
    setLoading(false);
  };

  if (!userId) return null;

  return (
    <div className="space-y-3">
      {!selectedAlbum ? (
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
