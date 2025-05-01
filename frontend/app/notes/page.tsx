'use client';

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Header from "../ui/Header";
import { unstable_noStore as noStore } from 'next/cache';

interface Mood {
  mood: string;
  created_at: string;
}

interface Note {
  text: string;
  audio_url: string;
  created_at: string;
  is_suicidal: boolean;
  moods: Mood[];
}

const NotesPage = () => {
  const router = useRouter();
  const [notes, setNotes] = useState<Note[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchNotes = async () => {
      setLoading(true);
      noStore();

      const host = process.env.NEXT_PUBLIC_ORCHESTRATOR_HOST;
      const port = process.env.NEXT_PUBLIC_ORCHESTRATOR_PORT;
      const notesUrl = `http://${host}:${port}/notes`;

      try {
        const response = await fetch(notesUrl, {
          method: 'GET',
          credentials: 'include',
        });

        if (response.status === 401) {
          router.push('/');
          return;
        }

        const data = await response.json();
        setNotes(data.notes || []);
      } catch (err: unknown) {
        if (err instanceof Error) setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchNotes();
  }, [router]);

  return (
    <div className="min-h-screen bg-gray-50">
      <Header headerState="loggedin" />
      <main className="pt-24 max-w-4xl mx-auto px-4">
        <h1 className="text-3xl font-bold mb-6 text-center">Your Notes</h1>

        {loading && <p>Loading notes...</p>}
        {error && <p className="text-red-500">{error}</p>}

        <div className="space-y-6">
          {notes.length === 0 && !loading && <p>No notes found.</p>}

          {notes.map((note, index) => (
            <div
              key={index}
              className="bg-white p-4 rounded-lg shadow-md border border-gray-200"
            >
              <div className="flex flex-wrap gap-2 mb-2">
                {note.is_suicidal && (
                  <span className="text-xs bg-black text-white px-2 py-1 rounded-full font-medium">
                    Suicidal
                  </span>
                )}
                {note.moods.length > 0 ? (
                  note.moods.map((m, i) => (
                    <span
                      key={i}
                      className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded-full font-medium"
                    >
                      {m.mood}
                    </span>
                  ))
                ) : (
                  <span className="text-xs text-gray-400 px-2 py-1">No moods</span>
                )}
              </div>

              <p className="text-gray-800 mb-3 whitespace-pre-line">{note.text || "No text"}</p>

              {note.audio_url && (
                <div className="mb-3">
                  <audio controls src={note.audio_url} className="w-full" />
                </div>
              )}

              <p className="text-sm text-gray-500 text-right mt-4">
                {new Date(note.created_at).toLocaleString()}
              </p>
            </div>
          ))}
        </div>
      </main>
    </div>
  );
};

export default NotesPage;
