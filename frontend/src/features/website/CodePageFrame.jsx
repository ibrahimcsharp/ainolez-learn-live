import { RefreshCw, ShieldAlert } from "lucide-react";
import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router";
import { API_ORIGIN } from "../../shared/api/client";
import { LoadingBar, Spinner } from "../../shared/ui/Loader";
import styles from "./SitePage.module.css";

const MAX_HEIGHT = 40000; // a page that grows with its frame (height: 100vh + margin) stops here
const SLOW_MS = 12000;
const BLOCKED_MS = 4000; // the page's helper script did not answer this long after the frame loaded

/**
 * A custom code page: the admin's HTML, CSS and JS run in a sandboxed iframe of
 * the API's page document (another origin, an opaque one, see website/code_page.py),
 * so they cannot touch this site, its cookies or its storage.
 * The page reports its height (the frame grows to fit) and the links clicked in it.
 */
export function CodePageFrame({ page }) {
  const frame = useRef(null);
  const navigate = useNavigate();
  const [height, setHeight] = useState(null);
  const [ready, setReady] = useState(false);
  const [slow, setSlow] = useState(false);
  const [heard, setHeard] = useState(false); // the page's helper script answered
  const [loaded, setLoaded] = useState(false);
  const [blocked, setBlocked] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => setSlow(true), SLOW_MS);
    function receive(event) {
      const data = event.data;
      if (event.source !== frame.current?.contentWindow || data?.source !== "ainolez-page") return;
      setHeard(true);
      if (data.type === "height" && Number.isFinite(data.height)) {
        setHeight(Math.min(Math.ceil(data.height), MAX_HEIGHT));
      } else if (data.type === "ready") {
        setReady(true);
      } else if (data.type === "navigate" && typeof data.href === "string") {
        follow(data.href);
      }
    }
    function follow(href) {
      if (href.startsWith("/") && !href.startsWith("//")) navigate(href);
      else if (/^(https?:|mailto:)/i.test(href)) window.location.assign(href);
      // anything else (javascript:, relative paths) is ignored
    }
    window.addEventListener("message", receive);
    return () => {
      clearTimeout(timer);
      window.removeEventListener("message", receive);
    };
  }, [navigate]);

  // Loaded but silent: the browser (usually an extension) blocked the frame.
  useEffect(() => {
    if (!loaded || heard) return undefined;
    const timer = setTimeout(() => setBlocked(true), BLOCKED_MS);
    return () => clearTimeout(timer);
  }, [loaded, heard]);

  if (blocked && !heard) {
    return (
      <div className={styles.codePage}>
        <div className={styles.cover} role="alert">
          <ShieldAlert size={36} className={styles.alert} />
          <h1 className={styles.blockedTitle}>{page.title} could not load</h1>
          <p className={styles.blockedText}>
            Your browser blocked this page. This is usually a browser extension, such as an ad or script blocker.
            Allow this site in the extension, or open the page in a private window.
          </p>
          <button type="button" className="btn btn-primary" onClick={() => window.location.reload()}>
            <RefreshCw size={16} /> Try again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className={styles.codePage} data-ready={ready}>
      <LoadingBar done={ready} />
      {!ready && (
        <div className={styles.cover} role="status">
          <Spinner size={44} label={`Loading ${page.title}`} />
          <p>{slow ? "Still loading… this page is taking a while." : `Loading ${page.title}…`}</p>
        </div>
      )}
      <iframe ref={frame} title={page.title} className={styles.frame}
        src={`${API_ORIGIN}${page.frame_path}`}
        style={height ? { height } : undefined}
        // no allow-same-origin: the page gets an opaque origin
        sandbox="allow-scripts allow-forms allow-modals allow-popups allow-popups-to-escape-sandbox allow-downloads"
        allow="fullscreen; clipboard-write; autoplay"
        // a page whose scripts never say "ready" (an error) still shows after it loads
        onLoad={() => {
          setLoaded(true);
          setTimeout(() => setReady(true), 400);
        }} />
    </div>
  );
}
