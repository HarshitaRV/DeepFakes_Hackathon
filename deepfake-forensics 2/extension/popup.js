const API_BASE = "http://localhost:8000";

document.getElementById("analyzeBtn").addEventListener("click", async () => {
  const btn = document.getElementById("analyzeBtn");
  const statusEl = document.getElementById("status");
  const reportEl = document.getElementById("report");

  btn.disabled = true;
  statusEl.textContent = "Capturing frames from page video...";
  reportEl.textContent = "";

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

      statusEl.textContent = "Analyzing captured frames...";

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
        reportEl.textContent = data.report;
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
