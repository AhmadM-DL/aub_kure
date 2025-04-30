'use client';

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Header from "../ui/Header";
import Footer from "../ui/Footer";
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

const Home = () => {
  const router = useRouter();
  const [notes, setNotes] = useState<Note[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [activeTab, setActiveTab] = useState<"notes" | "dashboard">("notes");

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
  }, [router]);

  return (
    <div className="min-h-screen bg-gray-50">
      <Header headerState="loggedin" />

      <main className="max-w-4xl mx-auto pt-24 px-4">
        <h1 className="text-3xl font-bold mb-6 text-center">Welcome</h1>

        {/* Tabs */}
        <div className="flex justify-center mb-6">
          <button
            className={`px-4 py-2 font-semibold border-b-2 ${
              activeTab === "notes"
                ? "border-blue-600 text-blue-600"
                : "border-transparent text-gray-600 hover:text-blue-500"
            }`}
            onClick={() => setActiveTab("notes")}
          >
            Notes
          </button>
          <button
            className={`px-4 py-2 font-semibold border-b-2 ml-4 ${
              activeTab === "dashboard"
                ? "border-blue-600 text-blue-600"
                : "border-transparent text-gray-600 hover:text-blue-500"
            }`}
            onClick={() => setActiveTab("dashboard")}
          >
            Dashboard
          </button>
        </div>

        {/* Notes Tab */}
        {activeTab === "notes" && (
          <>
            {loading && <p>Loading notes...</p>}
            {error && <p className="text-red-500">{error}</p>}

            <div className="space-y-6">
              {notes.length === 0 && !loading && <p>No notes found.</p>}

              {notes.map((note, index) => (
                <div
                  key={index}
                  className="relative bg-white p-4 rounded-lg shadow-md border border-gray-200"
                >
                  {note.is_suicidal && (
                    <div className="absolute top-3 right-3 text-black font-bold text-2xl">
                      ;
                    </div>
                  )}

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

                  <p className="text-gray-800 mb-3 whitespace-pre-line">
                    {note.text || "No text"}
                  </p>

                  {note.audio_url && (
                    <div className="mb-3">
                      <audio controls src={note.audio_url} className="w-full">
                        Your browser does not support the audio element.
                      </audio>
                    </div>
                  )}

                  <p className="text-sm text-gray-500 text-right mt-4">
                    {new Date(note.created_at).toLocaleString()}
                  </p>
                </div>
              ))}
            </div>
          </>
        )}

        {/* Dashboard Tab */}
        {activeTab === "dashboard" && (
          <div className="bg-white p-6 rounded-lg shadow">
            <h2 className="text-xl font-semibold mb-4">Dashboard (Coming Soon)</h2>
            <p>This section will show analytics and trends based on your notes.</p>
          </div>
        )}
      </main>

      <Footer />
    </div>
  );
};

export default Home;
