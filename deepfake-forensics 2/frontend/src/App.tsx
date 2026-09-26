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

interface AnalysisSummary {
  signal_count: number;
  confidence: number;
  risk: "low" | "medium" | "high";
  model_status: string;
}

interface AnalysisResult {
  file_id: string;
  timeline: TimelinePoint[];
  video_segments: Segment[];
  audio_segments: Segment[];
  provenance: { c2pa_found: boolean; note: string };
  report: string;
  analysis_summary?: AnalysisSummary;
  overall_risk?: "low" | "medium" | "high";
  model_status?: string;
}

const riskTone: Record<string, { label: string; className: string }> = {
  low: { label: "Low risk", className: "pill ok" },
  medium: { label: "Medium risk", className: "pill warn" },
  high: { label: "High risk", className: "pill danger" },
};

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

  const riskKey = result?.overall_risk || result?.analysis_summary?.risk || "low";
  const riskMeta = riskTone[riskKey] || riskTone.low;

  return (
    <>
      <style>{`
        :root {
          color-scheme: dark;
          --bg: #0a0d14;
          --panel: #121a2a;
          --panel-2: #0f1729;
          --line: #243046;
          --text: #e5edf9;
          --muted: #9aa8bd;
          --danger: #ff7b7b;
          --warn: #fbbf24;
          --ok: #4ade80;
          --blue: #60a5fa;
        }
        * { box-sizing: border-box; }
        body {
          margin: 0;
          font-family: Inter, "Segoe UI", sans-serif;
          background: radial-gradient(circle at top, #101a2d 0%, var(--bg) 50%);
          color: var(--text);
        }
        .app-shell {
          max-width: 1280px;
          margin: 0 auto;
          padding: 32px 20px 60px;
        }
        .header {
          display: flex;
          flex-direction: column;
          gap: 10px;
          margin-bottom: 20px;
        }
        .title {
          font-size: clamp(2rem, 3vw, 2.8rem);
          font-weight: 800;
          letter-spacing: -0.04em;
          margin: 0;
        }
        .subtitle {
          color: var(--muted);
          max-width: 720px;
          line-height: 1.5;
        }
        .uploader {
          border: 1px dashed #2f3d59;
          background: rgba(18, 26, 42, 0.9);
          border-radius: 18px;
          padding: 26px 20px;
          text-align: center;
          cursor: pointer;
          transition: border-color 0.2s ease, transform 0.2s ease;
        }
        .uploader:hover { border-color: #5b7fb5; }
        .uploader input { display: none; }
        .upload-label {
          color: var(--text);
          font-weight: 600;
        }
        .dashboard {
          display: grid;
          grid-template-columns: 1.2fr 0.8fr;
          gap: 20px;
          margin-top: 22px;
        }
        .panel {
          background: rgba(18, 26, 42, 0.92);
          border: 1px solid var(--line);
          border-radius: 18px;
          padding: 18px;
          box-shadow: 0 20px 50px rgba(0, 0, 0, 0.18);
        }
        .panel h2 {
          margin: 0 0 12px;
          font-size: 1rem;
          letter-spacing: 0.01em;
        }
        .summary-grid {
          display: grid;
          grid-template-columns: repeat(4, minmax(0, 1fr));
          gap: 12px;
          margin: 18px 0;
        }
        .metric {
          background: rgba(13, 18, 29, 0.9);
          border: 1px solid var(--line);
          border-radius: 14px;
          padding: 14px;
        }
        .metric small {
          display: block;
          color: var(--muted);
          margin-bottom: 8px;
        }
        .metric strong {
          font-size: 1.45rem;
          font-weight: 800;
        }
        .pill {
          display: inline-flex;
          align-items: center;
          border-radius: 999px;
          padding: 6px 10px;
          font-size: 11px;
          font-weight: 700;
          letter-spacing: 0.02em;
        }
        .pill.ok { background: rgba(74, 222, 128, 0.12); color: #a7f3d0; }
        .pill.warn { background: rgba(251, 191, 36, 0.12); color: #fcd34d; }
        .pill.danger { background: rgba(255, 123, 123, 0.12); color: #fecaca; }
        .pill.info { background: rgba(96, 165, 250, 0.12); color: #bfdbfe; }
        .signal-list {
          list-style: none;
          padding: 0;
          margin: 0;
          display: grid;
          gap: 10px;
          font-size: 0.95rem;
        }
        .signal-list li {
          padding: 10px 12px;
          border-radius: 10px;
          border: 1px solid var(--line);
          background: rgba(16, 21, 32, 0.75);
        }
        .signal-list li.video { border-left: 3px solid var(--danger); }
        .signal-list li.audio { border-left: 3px solid var(--warn); }
        .report-box {
          margin-top: 16px;
          font-size: 0.95rem;
          line-height: 1.7;
          color: #dfe9fa;
          background: rgba(11, 16, 26, 0.75);
          border: 1px solid var(--line);
          border-radius: 12px;
          padding: 14px;
        }
        .status-line {
          margin-top: 12px;
          color: var(--muted);
          font-size: 0.88rem;
        }
        .helper {
          color: var(--muted);
          font-size: 0.78rem;
          margin-top: 8px;
        }
        @media (max-width: 960px) {
          .dashboard { grid-template-columns: 1fr; }
          .summary-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
        }
      `}</style>

      <div className="app-shell">
        <header className="header">
          <h1 className="title">Explainable Deepfake Forensics</h1>
          <p className="subtitle">
            Localized detection across video and audio, with provenance checks and human-review guidance.
            This prototype is geared toward evidence-first analysis rather than a simple “real/fake” verdict.
          </p>
        </header>

        <label className="uploader">
          <input type="file" accept="video/*" onChange={handleUpload} />
          <span className="upload-label">
            {fileName ? `Selected: ${fileName}` : "Upload a suspicious video for forensic analysis"}
          </span>
        </label>

        {loading && (
          <div className="status-line">Extracting evidence, scoring manipulation signals, and preparing the forensic summary…</div>
        )}

        {error && (
          <div className="report-box" style={{ color: "#fecaca", borderColor: "#7f1d1d" }}>
            {error}
          </div>
        )}

        {result && (
          <div className="dashboard">
            <section className="panel" style={{ gridColumn: "1 / -1" }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", gap: 12, flexWrap: "wrap" }}>
                <h2>Case summary</h2>
                <span className={riskMeta.className}>{riskMeta.label}</span>
              </div>

              <div className="summary-grid">
                <div className="metric">
                  <small>Overall confidence</small>
                  <strong>{result.analysis_summary?.confidence ?? 0.5}</strong>
                </div>
                <div className="metric">
                  <small>Signal count</small>
                  <strong>{result.analysis_summary?.signal_count ?? 0}</strong>
                </div>
                <div className="metric">
                  <small>Model mode</small>
                  <strong>{result.model_status || "heuristic"}</strong>
                </div>
                <div className="metric">
                  <small>Provenance</small>
                  <strong>{result.provenance?.c2pa_found ? "Present" : "Missing"}</strong>
                </div>
              </div>
            </section>

            <section className="panel">
              <h2>Manipulation confidence timeline</h2>
              {result.timeline.length > 0 ? (
                <ResponsiveContainer width="100%" height={260}>
                  <LineChart data={result.timeline}>
                    <XAxis dataKey="time" stroke="#9aa8bd" tick={{ fill: "#9aa8bd", fontSize: 12 }} />
                    <YAxis domain={[0, 1]} stroke="#9aa8bd" tick={{ fill: "#9aa8bd", fontSize: 12 }} />
                    <Tooltip
                      contentStyle={{ background: "#111827", border: "1px solid #334155", borderRadius: 12, color: "#fff" }}
                    />
                    {result.video_segments.map((segment, idx) => (
                      <ReferenceArea key={idx} x1={segment.start} x2={segment.end} fill="#ff7b7b" fillOpacity={0.18} />
                    ))}
                    <Line type="monotone" dataKey="confidence" stroke="#ff7b7b" strokeWidth={3} dot={false} />
                  </LineChart>
                </ResponsiveContainer>
              ) : (
                <div className="helper">No timeline anomalies were detected from the current capture.</div>
              )}
            </section>

            <aside className="panel">
              <h2>Flagged segments</h2>
              <ul className="signal-list">
                {result.video_segments.length > 0 ? (
                  result.video_segments.map((segment, idx) => (
                    <li key={`video-${idx}`} className="video">
                      Face manipulation likely: {segment.start}s – {segment.end}s
                    </li>
                  ))
                ) : (
                  <li className="video">No strong visual face-segment anomaly detected.</li>
                )}

                {result.audio_segments.length > 0 ? (
                  result.audio_segments.map((segment, idx) => (
                    <li key={`audio-${idx}`} className="audio">
                      Audio anomaly: {segment.start}s – {segment.end}s ({segment.note || "suspicious signal"})
                    </li>
                  ))
                ) : (
                  <li className="audio">No strong audio discontinuity flagged.</li>
                )}
              </ul>
            </aside>

            <section className="panel" style={{ gridColumn: "1 / -1" }}>
              <h2>Evidence report</h2>
              <div className="report-box">{result.report}</div>
            </section>

            <section className="panel" style={{ gridColumn: "1 / -1" }}>
              <h2>Provenance and review guidance</h2>
              <div className="report-box">
                <div style={{ marginBottom: 8 }}>
                  {result.provenance.c2pa_found ? (
                    <span className="pill ok">C2PA: detected</span>
                  ) : (
                    <span className="pill warn">C2PA: unavailable</span>
                  )}
                </div>
                <div>{result.provenance.note}</div>
                <div style={{ marginTop: 12 }}>
                  <span className="pill info">Recommendation</span>
                  <div style={{ marginTop: 8 }}>Human review is recommended before any public claim, takedown, or reputation-impacting action.</div>
                </div>
              </div>
            </section>
          </div>
        )}
      </div>
    </>
  );
}
