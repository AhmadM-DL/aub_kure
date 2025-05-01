'use client';
import { useRouter } from "next/navigation";
import { useEffect, useState, useRef } from "react";
import Header from "../ui/Header";
import * as d3 from "d3";
import { removeStopwords } from "stopword";
import cloud, { Word } from "d3-cloud";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Bar } from 'react-chartjs-2';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

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

const Dashboard = () => {
  const router = useRouter();
  const [allNotes, setAllNotes] = useState<Note[]>([]);
  const [notes, setNotes] = useState<Note[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [suicidalCount, setSuicidalCount] = useState(0);
  const [moodCounts, setMoodCounts] = useState<Record<string, number>>({});
  const [wordCloudData, setWordCloudData] = useState<{ text: string; size: number }[]>([]);

  const [filterRange, setFilterRange] = useState<'week' | 'month'>('week');
  const svgRef = useRef<SVGSVGElement | null>(null);

  useEffect(() => {
    const fetchNotes = async () => {
      setLoading(true);

      const host = process.env.NEXT_PUBLIC_ORCHESTRATOR_HOST;
      const port = process.env.NEXT_PUBLIC_ORCHESTRATOR_PORT;
      const notesUrl = `http://${host}:${port}/notes`;

      try {
        const res = await fetch(notesUrl, {
          method: 'GET',
          credentials: 'include',
        });

        if (res.status === 401) {
          router.push('/');
          return;
        }

        const data = await res.json();
        setAllNotes(data.notes);
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

  useEffect(() => {
    if (allNotes.length === 0) return;

    const now = new Date();
    const cutoff = new Date(now);

    if (filterRange === 'week') {
      cutoff.setDate(now.getDate() - 7);
    } else {
      cutoff.setMonth(now.getMonth() - 1);
    }

    const filtered = allNotes.filter(note => new Date(note.created_at) >= cutoff);
    setNotes(filtered);
    processDashboardData(filtered);
  }, [filterRange, allNotes]);

  const processDashboardData = (notes: Note[]) => {
    setSuicidalCount(notes.filter(n => n.is_suicidal).length);

    const moodMap: Record<string, number> = {};
    notes.forEach(note =>
      note.moods.forEach(m => (moodMap[m.mood] = (moodMap[m.mood] || 0) + 1))
    );
    setMoodCounts(moodMap);

    const allText = notes.map(n => n.text || "").join(" ").toLowerCase();
    const words = allText.match(/\b\w+\b/g) || [];
    const filtered: string[] = removeStopwords(words);
    const freq: Record<string, number> = {};
    filtered.forEach(word => (freq[word] = (freq[word] || 0) + 1));

    const sorted = Object.entries(freq).sort((a, b) => b[1] - a[1]);
    setWordCloudData(sorted.map(([text, value]) => ({ text, size: value * 10 })));
  };

  useEffect(() => {
    const renderWordCloud = (words: { text: string; size: number }[]) => {
      const svg = d3.select(svgRef.current);
      svg.selectAll("*").remove();

      const width = 500;
      const height = 300;

      cloud()
        .size([width, height])
        .words(words)
        .padding(5)
        .rotate(() => (Math.random() > 0.5 ? 0 : 90))
        .font("sans-serif")
        .fontSize(d => d.size || 1)
        .on("end", draw)
        .start();

      function draw(words: Word[]) {
        svg
          .attr("width", "100%")
          .attr("height", height)
          .append("g")
          .attr("transform", `translate(${width / 2}, ${height / 2})`)
          .selectAll("text")
          .data(words)
          .enter()
          .append("text")
          .style("font-size", d => `${d.size}px`)
          .style("fill", () => d3.schemeCategory10[Math.floor(Math.random() * 10)])
          .attr("text-anchor", "middle")
          .attr("transform", d => `translate(${d.x}, ${d.y}) rotate(${d.rotate})`)
          .text(d => d.text || "");
      }
    };

    if (wordCloudData.length > 0) {
      renderWordCloud(wordCloudData);
    }
  }, [wordCloudData]);

  return (
    <div className="min-h-screen bg-gray-50">
      <Header headerState="loggedin" />
      <main className="pt-24 max-w-6xl mx-auto px-4">
        <h1 className="text-3xl font-bold mb-8 text-center">Dashboard</h1>

        {loading && <p>Loading...</p>}
        {error && <p className="text-red-500">{error}</p>}

        {/* Filter UI */}
        <div className="flex justify-end mb-4">
          <label className="mr-2 font-semibold">Filter by:</label>
          <select
            value={filterRange}
            onChange={(e) => setFilterRange(e.target.value as 'week' | 'month')}
            className="border border-gray-300 rounded px-2 py-1"
          >
            <option value="week">Last Week</option>
            <option value="month">Last Month</option>
          </select>
        </div>

        {!loading && notes.length > 0 && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Suicidal Thoughts */}
            <div className="bg-white p-6 rounded-lg shadow-md">
              <h2 className="text-lg font-semibold mb-2">Suicidal Thoughts</h2>
              <p className="text-3xl font-bold text-red-600">{suicidalCount}</p>
            </div>

            {/* Mood Distribution */}
            <div className="bg-white p-6 rounded-lg shadow-md">
              <h2 className="text-lg font-semibold mb-4">Mood Distribution</h2>
              <Bar
                data={{
                  labels: Object.keys(moodCounts),
                  datasets: [{
                    label: "Count",
                    data: Object.values(moodCounts),
                    backgroundColor: "rgba(59,130,246,0.5)",
                  }]
                }}
              />
            </div>

            {/* Word Cloud */}
            <div className="bg-white p-6 rounded-lg shadow-md col-span-1 md:col-span-2">
              <h2 className="text-lg font-semibold mb-4">Word Cloud</h2>
              <svg ref={svgRef} className="w-full h-[300px]"></svg>
            </div>
          </div>
        )}
      </main>
    </div>
  );
};

export default Dashboard;
