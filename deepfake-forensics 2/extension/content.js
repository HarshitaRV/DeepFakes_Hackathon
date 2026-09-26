chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.type !== "CAPTURE_FRAMES") return false;

  const video = document.querySelector("video");
  if (!video) {
    sendResponse({ error: "No video element found on this page." });
    return true;
  }

  const canvas = document.createElement("canvas");
  canvas.width = video.videoWidth || 640;
  canvas.height = video.videoHeight || 360;
  const ctx = canvas.getContext("2d");

  const duration = video.duration && isFinite(video.duration) ? video.duration : 10;
  const numFrames = 6;
  const frames = [];
  let i = 0;
  let wasPlaying = !video.paused;

  const finish = () => {
    if (wasPlaying) video.play().catch(() => {});
    sendResponse({ frames, duration });
  };

  const grabNext = () => {
    if (i >= numFrames) {
      finish();
      return;
    }
    const targetTime = (duration / numFrames) * i;

    const onSeeked = () => {
      video.removeEventListener("seeked", onSeeked);
      try {
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        frames.push(canvas.toDataURL("image/jpeg", 0.7));
      } catch (e) {
        // Cross-origin video without CORS headers taints the canvas
        frames.push(null);
      }
      i++;
      grabNext();
    };

    video.addEventListener("seeked", onSeeked);
    video.pause();
    video.currentTime = targetTime;
  };

  grabNext();
  return true; // keep the message channel open for async sendResponse
});
