"use client";
import { useEffect, useState } from "react";
import Header from "../ui/Header";
import Footer from "../ui/Footer";
import { unstable_noStore as noStore } from 'next/cache';
import { ExclamationTriangleIcon } from '@heroicons/react/24/solid';

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

const Home = () => {
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
        const response = await fetch(notesUrl);

        if (!response.ok) {
          const data = await response.json();
          throw new Error(data.message || "Failed to fetch notes.");
        }

        const data = await response.json();
        setNotes(data.notes || []);
      } catch (err: unknown) {
        if (err instanceof Error) {
          setError(err.message);
        }
      } finally {
        setLoading(false);
      }
    };

    fetchNotes();
  }, []);

  return (
    <div className="min-h-screen bg-gray-50">
      <Header headerState='loggedin'/>

      <main className="max-w-4xl mx-auto pt-24 px-4">
        <h1 className="text-3xl font-bold mb-6 text-center">Your Notes</h1>

        {loading && <p>Loading notes...</p>}
        {error && <p className="text-red-500">{error}</p>}

        <div className="space-y-6">
          {notes.length === 0 && !loading && <p>No notes found.</p>}

          {notes.map((note, index) => (
            <div
              key={index}
              className="relative bg-white p-4 rounded-lg shadow-md border border-gray-200"
            >
              {/* Suicide Icon */}
              {note.is_suicidal && (
                <div className="absolute top-3 right-3 text-red-600">
                  <ExclamationTriangleIcon className="w-6 h-6" />
                </div>
              )}

              {/* Mood Tags */}
              <div className="flex flex-wrap gap-2 mb-2">
                {note.moods.length > 0 ? (
                  note.moods.map((m, i) => (
                    <span
                      key={i}
                      className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded-full"
                    >
                      {m.mood}
                    </span>
                  ))
                ) : (
                  <span className="text-xs text-gray-400">No moods</span>
                )}
              </div>

              {/* Text */}
              <p className="text-gray-800 mb-3 whitespace-pre-line">
                {note.text || "No text"}
              </p>

              {/* Audio */}
              {note.audio_url && (
                <div className="mb-3">
                  <audio controls src={note.audio_url} className="w-full">
                    Your browser does not support the audio element.
                  </audio>
                </div>
              )}

              {/* Created At Date */}
              <p className="text-sm text-gray-500 text-right mt-4">
                {new Date(note.created_at).toLocaleString()}
              </p>
            </div>
          ))}
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default Home;
