import { useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  ReferenceArea,
} from "recharts";

const API_BASE = "http://localhost:8000";

interface TimelinePoint {
  time: number;
  confidence: number;
}

interface Segment {
  start: number;
  end: number;
  type: string;
  note?: string;
}

interface AnalysisResult {
  file_id: string;
  timeline: TimelinePoint[];
  video_segments: Segment[];
  audio_segments: Segment[];
  provenance: { c2pa_found: boolean; note: string };
  report: string;
}

export default function App() {
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [fileName, setFileName] = useState<string>("");

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setFileName(file.name);
    setLoading(true);
    setError(null);
    setResult(null);

    const form = new FormData();
    form.append("file", file);

    try {
      const res = await fetch(`${API_BASE}/analyze`, {
        method: "POST",
        body: form,
      });
      if (!res.ok) throw new Error(`Server responded ${res.status}`);
      const data: AnalysisResult = await res.json();
      setResult(data);
    } catch (err) {
      setError(
        err instanceof Error
          ? `${err.message} — is the backend running on ${API_BASE}?`
          : "Unknown error"
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen p-8">
      <div className="max-w-3xl mx-auto space-y-6">
        <header>
          <h1 className="text-2xl font-bold">Deepfake Forensics Report</h1>
          <p className="text-sm text-gray-400 mt-1">
            Explainable multimodal manipulation detection with localization + provenance.
          </p>
        </header>

        <label className="block border-2 border-dashed border-gray-700 rounded-xl p-6 text-center cursor-pointer hover:border-gray-500 transition">
          <input
            type="file"
            accept="video/*"
            onChange={handleUpload}
            className="hidden"
          />
          <span className="text-gray-300">
            {fileName ? `Selected: ${fileName}` : "Click to upload a video for analysis"}
          </span>
        </label>

        {loading && (
          <div className="text-sm text-gray-400 animate-pulse">
            Extracting frames and scoring manipulation signals...
          </div>
        )}

        {error && (
          <div className="bg-red-950 border border-red-800 text-red-200 text-sm p-3 rounded-lg">
            {error}
          </div>
        )}

        {result && (
          <div className="space-y-6">
            <section className="bg-gray-900 p-4 rounded-xl">
              <h2 className="font-semibold mb-2">Manipulation Confidence Timeline</h2>
              {result.timeline.length > 0 ? (
                <ResponsiveContainer width="100%" height={220}>
                  <LineChart data={result.timeline}>
                    <XAxis
                      dataKey="time"
                      stroke="#9ca3af"
                      label={{ value: "seconds", position: "insideBottom", dy: 10, fill: "#9ca3af" }}
                    />
                    <YAxis domain={[0, 1]} stroke="#9ca3af" />
                    <Tooltip
                      contentStyle={{ background: "#1f2937", border: "none", color: "#fff" }}
                    />
                    {result.video_segments.map((s, i) => (
                      <ReferenceArea key={i} x1={s.start} x2={s.end} fill="#f87171" fillOpacity={0.2} />
                    ))}
                    <Line type="monotone" dataKey="confidence" stroke="#f87171" dot={false} strokeWidth={2} />
                  </LineChart>
                </ResponsiveContainer>
              ) : (
                <p className="text-sm text-gray-500">No timeline data available.</p>
              )}
            </section>

            <section className="bg-gray-900 p-4 rounded-xl">
              <h2 className="font-semibold mb-2">Flagged Segments</h2>
              <ul className="text-sm space-y-1">
                {result.video_segments.map((s, i) => (
                  <li key={`v-${i}`} className="text-red-300">
                    Face manipulation suspected: {s.start}s – {s.end}s
                  </li>
                ))}
                {result.audio_segments.map((s, i) => (
                  <li key={`a-${i}`} className="text-yellow-300">
                    Audio anomaly: {s.start}s – {s.end}s {s.note ? `(${s.note})` : ""}
                  </li>
                ))}
                {result.video_segments.length === 0 && result.audio_segments.length === 0 && (
                  <li className="text-gray-500">No segments flagged.</li>
                )}
              </ul>
            </section>

            <section className="bg-gray-900 p-4 rounded-xl">
              <h2 className="font-semibold mb-2">Evidence Report</h2>
              <p className="text-sm leading-relaxed text-gray-200">{result.report}</p>
            </section>

            <section className="bg-gray-900 p-4 rounded-xl">
              <h2 className="font-semibold mb-2">Provenance (C2PA)</h2>
              <p className="text-sm">
                {result.provenance.c2pa_found
                  ? "✅ Content Credentials found"
                  : `⚠️ ${result.provenance.note}`}
              </p>
            </section>
          </div>
        )}
      </div>
    </div>
  );
}
