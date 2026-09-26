const API_BASE = "http://localhost:8000";

function renderSummary(data) {
  const reportEl = document.getElementById("report");
  const videoSegments = data.video_segments || [];
  const audioSegments = data.audio_segments || [];
  const provenance = data.provenance || { c2pa_found: false, note: "No provenance data." };

  const videoHtml = videoSegments.length
    ? videoSegments.map((s) => `<div class="seg">• Face manipulation likely: ${s.start}s–${s.end}s</div>`).join("")
    : "<div>• No strong visual segment flagged.</div>";

  const audioHtml = audioSegments.length
    ? audioSegments.map((s) => `<div class="seg">• Audio anomaly: ${s.start}s–${s.end}s</div>`).join("")
    : "<div>• No strong audio discontinuity flagged.</div>";

  const provenanceState = provenance.c2pa_found
    ? '<span class="pill ok">Provenance: present</span>'
    : '<span class="pill risk">Provenance: missing</span>';

  reportEl.innerHTML = `
    <div class="summary">
      ${provenanceState}
      <div><strong>Risk</strong>: Human review recommended</div>
      <div class="seg">${data.report || "No report available."}</div>
      <div style="margin-top:8px;">${videoHtml}</div>
      <div style="margin-top:6px;">${audioHtml}</div>
      <div style="margin-top:8px;">${provenance.note || "No provenance note."}</div>
    </div>
  `;
}

document.getElementById("analyzeBtn").addEventListener("click", async () => {
  const btn = document.getElementById("analyzeBtn");
  const statusEl = document.getElementById("status");
  const reportEl = document.getElementById("report");

  btn.disabled = true;
  statusEl.textContent = "Capturing frames from page video...";
  reportEl.innerHTML = "";

  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

    chrome.tabs.sendMessage(tab.id, { type: "CAPTURE_FRAMES" }, async (response) => {
      if (chrome.runtime.lastError) {
        statusEl.textContent = "Could not reach page (try reloading the tab).";
        btn.disabled = false;
        return;
      }
      if (!response || response.error) {
        statusEl.textContent = response?.error || "Capture failed.";
        btn.disabled = false;
        return;
      }

      statusEl.textContent = "Analyzing captured frames and audio indicators...";

      try {
        const res = await fetch(`${API_BASE}/analyze_frames`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            frames: response.frames,
            duration: response.duration,
          }),
        });

        if (!res.ok) throw new Error(`Server responded ${res.status}`);
        const data = await res.json();

        statusEl.textContent = "Analysis complete.";
        renderSummary(data);
      } catch (e) {
        statusEl.textContent = `Backend unreachable at ${API_BASE}. Is it running?`;
      } finally {
        btn.disabled = false;
      }
    });
  } catch (e) {
    statusEl.textContent = "Unexpected error: " + e.message;
    btn.disabled = false;
  }
});
