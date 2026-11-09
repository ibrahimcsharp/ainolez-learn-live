/*
 * Video timestamps in content ("00:40 IDE Choice", rendered by the server as
 * <a class="timestamp">): a click moves the video shown above the link to that
 * moment and plays it, instead of opening YouTube. With no video above, the
 * link works as a normal link.
 */
const PLAYER_HOSTS = /(^|\.)(youtube-nocookie\.com|youtube\.com|vimeo\.com)$/;

/** Seconds from a timestamp link's address ("...&t=40s" or "#t=40"), or null. */
export function secondsOf(href) {
  const match = /[?&#]t=(\d+)s?\b/.exec(href ?? "");
  return match ? Number(match[1]) : null;
}

/** The last video player placed before `link` on the page. */
export function playerBefore(link) {
  let found = null;
  for (const player of document.querySelectorAll("iframe, video")) {
    if (!(player.compareDocumentPosition(link) & Node.DOCUMENT_POSITION_FOLLOWING)) break;
    if (player.tagName === "VIDEO" || isVideoFrame(player)) found = player;
  }
  return found;
}

function isVideoFrame(frame) {
  try {
    return PLAYER_HOSTS.test(new URL(frame.src).hostname);
  } catch {
    return false;
  }
}

/** Point the player at `at` seconds and start it. */
export function seek(player, at) {
  if (player.tagName === "VIDEO") {
    player.currentTime = at;
    player.play?.().catch(() => {});
    return;
  }
  const url = new URL(player.src);
  if (url.hostname.endsWith("vimeo.com")) {
    url.searchParams.set("autoplay", "1");
    url.hash = `t=${at}s`;
  } else {
    url.searchParams.set("start", String(at));
    url.searchParams.set("autoplay", "1");
  }
  if (!/\bautoplay\b/.test(player.allow)) player.allow = `${player.allow}; autoplay`.replace(/^; /, "");
  player.src = url.toString();
}

function onClick(event) {
  const link = event.target.closest?.("a.timestamp");
  if (!link || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
  const at = secondsOf(link.getAttribute("href"));
  const player = at === null ? null : playerBefore(link);
  if (!player) return;
  event.preventDefault();
  seek(player, at);
  player.scrollIntoView?.({ behavior: "smooth", block: "center" });
}

/** Called once from main.jsx: one listener serves every page. */
export function enableTimestampLinks() {
  document.addEventListener("click", onClick);
}
