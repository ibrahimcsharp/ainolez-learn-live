import { Check, Eye, Plus, RefreshCw, RotateCcw, Save, X } from "lucide-react";
import { useState } from "react";
import { api } from "../../../shared/api/client";
import { useApi } from "../../../shared/hooks/useApi";
import { Field } from "../../../shared/ui/Field";
import { RecordActions, StatusBadge } from "../shared/RecordActions";
import admin from "../shared/admin.module.css";
import { SEO } from "./SeoEditor";
import styles from "./Center.module.css";

const PERIODS = [7, 30, 90];
const KINDS = [
  ["search", "From search engines"],
  ["ai", "From AI engines"],
  ["social", "From social sites"],
];
const PURPOSES = {
  search: ["AI search engines", "Read pages to answer questions and link to them. Keep them allowed to be cited."],
  user: ["AI assistants opening a page", "Fetch a page when a person asks about it or shares the link."],
  training: ["AI training crawlers", "Collect pages to train models. Blocking them does not change AI search results."],
};

async function saveSettings(changes) {
  return api(`${SEO}/settings/`, { method: "PATCH", body: changes });
}

// --- Overview -----------------------------------------------------------------

export function OverviewTab({ onTab }) {
  const [days, setDays] = useState(30);
  const { data, error, reload } = useApi(`${SEO}/overview/?days=${days}`);
  const [busy, setBusy] = useState("");
  const [message, setMessage] = useState("");

  async function fix(key) {
    setBusy(key);
    try {
      await saveSettings({ [key]: true });
      reload();
    } catch (failure) {
      setMessage(failure.message);
    } finally {
      setBusy("");
    }
  }
  async function rebuild() {
    setBusy("build");
    setMessage("Building…");
    try {
      const { pages } = await api(`${SEO}/build/`, { method: "POST" });
      setMessage(`✓ Rebuilt ${pages} pages and the files for search and AI engines.`);
      reload();
    } catch (failure) {
      setMessage(failure.message);
    } finally {
      setBusy("");
    }
  }

  if (!data) {
    return <p className={error ? "page-loading" : "page-loading is-loading"}>{error?.message ?? "Loading…"}</p>;
  }
  const { seo, geo, fix_next: fixNext, traffic, build } = data;
  return (
    <>
      <div className={styles.scores}>
        <ScoreCard title="SEO score" note={`${seo.pages_ok} of ${seo.pages} indexed pages have no problems.`}
          score={seo.score} checks={seo.checks} busy={busy} onFix={fix} />
        <ScoreCard title="GEO score" note="How ready the site is to be read and cited by AI engines."
          score={geo.score} checks={geo.checks} busy={busy} onFix={fix} />
      </div>

      <section className={`card ${admin.panel}`}>
        <h2>Fix next</h2>
        {fixNext.length === 0 ? (
          <p className="muted">Nothing to fix. Keep content fresh: new lessons and updates are found faster.</p>
        ) : (
          <ul className={styles.fixList}>
            {fixNext.slice(0, 8).map((item) => (
              <li key={`${item.kind}-${item.label}`}>
                <span className={styles.kind}>{item.kind === "page" ? "pages" : item.kind}</span>
                <div>
                  <strong>{item.count ? `${item.count} × ` : ""}{item.label}</strong>
                  <small>{item.tip}</small>
                </div>
                {item.fix ? (
                  <button className={`btn btn-primary ${admin.small}`} disabled={Boolean(busy)}
                    onClick={() => fix(item.fix)}>
                    <Check /> Turn on
                  </button>
                ) : item.kind === "page" ? (
                  <button className={`btn btn-outline ${admin.small}`} onClick={() => onTab("report")}>
                    Open report
                  </button>
                ) : null}
              </li>
            ))}
          </ul>
        )}
      </section>

      <div className={styles.head}>
        <h2 style={{ margin: 0 }}>Visitors</h2>
        <div className={styles.periods} role="group" aria-label="Period">
          {PERIODS.map((n) => (
            <button key={n} type="button" aria-pressed={n === days} onClick={() => setDays(n)}>
              {n} days
            </button>
          ))}
        </div>
      </div>
      <Traffic traffic={traffic} days={days} />

      <section className={`card ${admin.panel}`}>
        <h2>Files for search and AI engines</h2>
        <p className="muted">
          Rebuilt by the site a minute after any change, and every night.{" "}
          {build.last_build_at
            ? `Last build: ${new Date(build.last_build_at).toLocaleString()} (${build.pages} pages).`
            : "Not built yet."}
        </p>
        <p className="muted">
          IndexNow:{" "}
          {build.indexnow_enabled
            ? build.indexnow_last_result
              ? `${build.indexnow_last_result} (${new Date(build.indexnow_last_at).toLocaleString()})`
              : "on, waiting for the next build."
            : "off."}
        </p>
        <button className="btn btn-outline" disabled={Boolean(busy)} onClick={rebuild}>
          <RefreshCw /> Rebuild now
        </button>{" "}
        <span>{message}</span>
      </section>

      <section className={`card ${admin.panel}`}>
        <div className={admin.toolbar}>
          <h2 style={{ margin: 0 }}>Recent changes</h2>
          <button className={`btn btn-outline ${admin.small}`} onClick={() => onTab("changes")}>
            Full change log
          </button>
        </div>
        <ChangeTable rows={data.recent_changes} onChange={reload} />
      </section>
    </>
  );
}

function ScoreCard({ title, note, score, checks, busy, onFix }) {
  const tone = score >= 80 ? styles.good : score >= 50 ? styles.fair : "";
  return (
    <section className={`card ${styles.score}`}>
      <div className={styles.scoreHead}>
        <div className={`${styles.ring} ${tone}`} style={{ "--value": score }} role="img"
          aria-label={`${title}: ${score} out of 100`}>
          <span>{score}</span>
        </div>
        <div>
          <h2>{title}</h2>
          <p className="muted">{note}</p>
        </div>
      </div>
      <ul className={styles.checks}>
        {checks.map((check) => (
          <li key={check.key}>
            {check.ok ? <Check size={18} className={styles.ok} aria-label="Done" />
              : <X size={18} className={styles.bad} aria-label="To do" />}
            <span>
              {check.label}
              {!check.ok && <small>{check.tip}</small>}
            </span>
            {check.fix && (
              <button className={`btn btn-outline ${admin.small}`} disabled={Boolean(busy)}
                onClick={() => onFix(check.fix)}>
                Turn on
              </button>
            )}
          </li>
        ))}
      </ul>
    </section>
  );
}

function Traffic({ traffic, days }) {
  const dates = Array.from({ length: days }, (_, i) => {
    const day = new Date();
    day.setDate(day.getDate() - (days - 1 - i));
    return day.toISOString().slice(0, 10);
  });
  const perDay = dates.map((day) => traffic.referrals_by_day[day] ?? {});
  const highest = Math.max(1, ...perDay.map((day) => KINDS.reduce((sum, [kind]) => sum + (day[kind] ?? 0), 0)));
  const sources = (kind) => traffic.sources.filter((row) => row.kind === kind);
  return (
    <>
      <div className={styles.totals}>
        <div className={`card ${styles.total}`}>
          <strong>{traffic.views_total.toLocaleString()}</strong>
          <span className="muted">Page views</span>
        </div>
        {KINDS.map(([kind, label]) => (
          <div key={kind} className={`card ${styles.total} ${styles[kind]}`}>
            <strong>{(traffic.totals[kind] ?? 0).toLocaleString()}</strong>
            <span className="muted">{label}</span>
          </div>
        ))}
      </div>
      <section className="card">
        <h3 style={{ marginTop: 0 }}>Visits from other sites per day</h3>
        <div className={styles.bars} role="img" aria-label="Visits from search, AI and social sites per day">
          {perDay.map((day, i) => (
            <div key={dates[i]} title={`${dates[i]}: ${KINDS.map(([k, l]) => `${l.replace("From ", "")} ${day[k] ?? 0}`).join(", ")}`}>
              {KINDS.map(([kind]) => (
                <i key={kind} className={styles[kind]}
                  style={{ height: `${((day[kind] ?? 0) / highest) * 100}%`, background: "var(--tone)" }} />
              ))}
            </div>
          ))}
        </div>
        <div className={styles.legend}>
          {KINDS.map(([kind, label]) => <span key={kind} className={styles[kind]}>{label.replace("From ", "")}</span>)}
        </div>
      </section>
      <div className={styles.split}>
        <section className="card">
          <h3 style={{ marginTop: 0 }}>AI engines</h3>
          <SourceTable rows={sources("ai")} empty="No visits from AI engines yet." />
          {traffic.ai_pages.length > 0 && (
            <>
              <h4>Pages AI engines send people to</h4>
              <SourceTable rows={traffic.ai_pages.map((row) => ({ source: row.path, visits: row.visits }))} />
            </>
          )}
        </section>
        <section className="card">
          <h3 style={{ marginTop: 0 }}>Search engines and social sites</h3>
          <SourceTable rows={[...sources("search"), ...sources("social")]} empty="No visits from other sites yet." />
        </section>
      </div>
    </>
  );
}

function SourceTable({ rows, empty = "" }) {
  if (!rows.length) return <p className="muted">{empty}</p>;
  return (
    <table className={admin.table}>
      <tbody>
        {rows.map((row) => (
          <tr key={`${row.kind}-${row.source}`}>
            <td>{row.source}</td>
            <td style={{ textAlign: "right" }}>{row.visits.toLocaleString()}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

// --- AI & GEO -------------------------------------------------------------------

const TASKS = [
  ["geo_llms_enabled", "llms.txt", "A short guide to the site at /llms.txt, with links to every course and page."],
  ["geo_llms_full_enabled", "llms-full.txt", "Every course and lesson as Markdown in one file, for AI tools that read whole sites."],
  ["geo_markdown_copies", "Markdown copy of every page", "/python.md, /python/lists.md … Clean text without the app, linked from each page."],
  ["geo_video_moments", "Video key moments", "Timestamps under videos become chapters (VideoObject + Clip) for Google and AI engines."],
  ["indexnow_enabled", "IndexNow", "After each build, tells Bing (behind ChatGPT search and Copilot), Yandex and others which pages changed."],
];

export function GeoTab() {
  const settings = useApi(`${SEO}/settings/`);
  const bots = useApi(`${SEO}/bots/?page_size=200`);
  if (!settings.data) return <p className="page-loading is-loading">Loading…</p>;
  return (
    <>
      <p className="muted">
        GEO (generative engine optimisation) helps ChatGPT, Claude, Perplexity, Gemini and Copilot read the site, understand
        it and cite it. The site does the jobs below by itself after every change; switch any of them off here.
      </p>
      <AutoTasks site={settings.data} onSaved={settings.reload} />
      <AboutSite key={settings.data.updated_at} site={settings.data} onSaved={settings.reload} />
      <Crawlers list={bots} />
      <FilePreview />
    </>
  );
}

function AutoTasks({ site, onSaved }) {
  const [busy, setBusy] = useState("");
  const [error, setError] = useState("");
  async function toggle(key) {
    setBusy(key);
    setError("");
    try {
      await saveSettings({ [key]: !site[key] });
      onSaved();
    } catch (failure) {
      setError(failure.message);
    } finally {
      setBusy("");
    }
  }
  return (
    <section className={`card ${admin.panel}`}>
      <h2>Automatic GEO tasks</h2>
      {error && <p className="notice notice-error">{error}</p>}
      <ul className={styles.toggles}>
        {TASKS.map(([key, label, help]) => (
          <li key={key}>
            <button type="button" role="switch" aria-checked={Boolean(site[key])} aria-label={label}
              className={styles.switch} disabled={busy === key} onClick={() => toggle(key)} />
            <span>
              <strong>{label}</strong>
              <small>{help}</small>
              {key === "indexnow_enabled" && site.indexnow_key && (
                <small>Key file: <code>/{site.indexnow_key}.txt</code>. {site.indexnow_last_result}</small>
              )}
            </span>
          </li>
        ))}
      </ul>
    </section>
  );
}

function AboutSite({ site, onSaved }) {
  const [values, setValues] = useState({
    geo_site_summary: site.geo_site_summary ?? "",
    geo_llms_details: site.geo_llms_details ?? "",
  });
  const [state, setState] = useState("");
  async function save(event) {
    event.preventDefault();
    setState("Saving…");
    try {
      await saveSettings(values);
      setState("✓ Saved. The next build updates llms.txt.");
      onSaved();
    } catch (failure) {
      setState(failure.message);
    }
  }
  const change = (event) => setValues({ ...values, [event.target.name]: event.target.value });
  return (
    <form className={`card ${admin.panel}`} onSubmit={save}>
      <h2>The site, in words for AI engines</h2>
      <Field as="textarea" name="geo_site_summary" rows={2} maxLength={500} value={values.geo_site_summary}
        onChange={change} placeholder={site.default_description}
        label="Summary (one or two sentences: who the site is for and what it gives)" />
      <Field as="textarea" name="geo_llms_details" rows={4} value={values.geo_llms_details} onChange={change}
        className={admin.code} label="More details for llms.txt (Markdown, optional)"
        placeholder="ainolez teaches Python, web development and AI with hands-on lessons…" />
      <button className="btn btn-primary"><Save /> Save</button> <span>{state}</span>
    </form>
  );
}

function Crawlers({ list }) {
  const [busy, setBusy] = useState(null);
  const [error, setError] = useState("");
  const rows = list.data?.results ?? [];
  async function setAllowed(bots, allowed) {
    setBusy(bots.length === 1 ? bots[0].id : "all");
    setError("");
    try {
      for (const bot of bots) {
        if (bot.allowed !== allowed) {
          await api(`${SEO}/bots/${bot.id}/`, { method: "PATCH", body: { allowed } });
        }
      }
      list.reload();
    } catch (failure) {
      setError(failure.message);
    } finally {
      setBusy(null);
    }
  }
  return (
    <section className={`card ${admin.panel}`}>
      <h2>AI crawlers</h2>
      <p className="muted">
        Each blocked crawler gets a <code>Disallow: /</code> rule in robots.txt at the next build. Search engines
        (Google, Bing) are not affected.
      </p>
      {error && <p className="notice notice-error">{error}</p>}
      {Object.entries(PURPOSES).map(([purpose, [title, help]]) => {
        const group = rows.filter((bot) => bot.purpose === purpose);
        if (!group.length) return null;
        return (
          <div key={purpose}>
            <div className={admin.toolbar}>
              <div>
                <h3 className={styles.purpose}>{title}</h3>
                <small className="muted">{help}</small>
              </div>
              <span>
                <button className={`btn btn-outline ${admin.small}`} disabled={busy !== null}
                  onClick={() => setAllowed(group, true)}>Allow all</button>{" "}
                <button className={`btn btn-outline ${admin.small}`} disabled={busy !== null}
                  onClick={() => setAllowed(group, false)}>Block all</button>
              </span>
            </div>
            <table className={admin.table}>
              <tbody>
                {group.map((bot) => (
                  <tr key={bot.id}>
                    <td style={{ width: 56 }}>
                      <button type="button" role="switch" aria-checked={bot.allowed}
                        aria-label={`${bot.user_agent} allowed`} className={styles.switch}
                        disabled={busy !== null || !bot.is_active} onClick={() => setAllowed([bot], !bot.allowed)} />
                    </td>
                    <td>
                      <strong>{bot.user_agent}</strong> <span className="muted">· {bot.owner}</span>
                      <div className="muted">{bot.notes}</div>
                    </td>
                    <td>{bot.allowed ? "Allowed" : <span className={styles.blocked}>Blocked</span>}</td>
                    <td><StatusBadge row={bot} /></td>
                    <td><RecordActions base={`${SEO}/bots`} row={bot} onChange={list.reload} /></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        );
      })}
      <AddCrawler onAdded={list.reload} />
    </section>
  );
}

function AddCrawler({ onAdded }) {
  const [state, setState] = useState("");
  async function add(event) {
    event.preventDefault();
    const form = event.currentTarget;
    const body = Object.fromEntries(new FormData(form));
    setState("Adding…");
    try {
      await api(`${SEO}/bots/`, { method: "POST", body: { ...body, allowed: true } });
      form.reset();
      setState("");
      onAdded();
    } catch (failure) {
      setState(failure.message);
    }
  }
  return (
    <form className={admin.toolbar} onSubmit={add} style={{ marginTop: 16 }}>
      <input name="user_agent" placeholder="User-agent, e.g. GPTBot" required aria-label="User-agent" />
      <input name="owner" placeholder="Company" aria-label="Company" />
      <select name="purpose" aria-label="Purpose" defaultValue="search">
        <option value="search">AI search</option>
        <option value="user">AI assistant</option>
        <option value="training">Training</option>
      </select>
      <input name="notes" placeholder="Notes" aria-label="Notes" style={{ flex: 1 }} />
      <button className="btn btn-outline"><Plus /> Add crawler</button> <span>{state}</span>
    </form>
  );
}

const FILES = [
  ["llms", "llms.txt", "/llms.txt"],
  ["llms-full", "llms-full.txt", "/llms-full.txt"],
  ["robots", "robots.txt", "/robots.txt"],
];

function FilePreview() {
  const [shown, setShown] = useState(null);
  const [path, setPath] = useState("/python");
  const [error, setError] = useState("");
  async function open(file, query = "") {
    setError("");
    try {
      const { text } = await api(`${SEO}/geo-file/?file=${file}${query}`);
      setShown({ file, text });
    } catch (failure) {
      setError(failure.message);
    }
  }
  return (
    <section className={`card ${admin.panel}`}>
      <h2>What AI engines read</h2>
      <p className="muted">A preview of what the next build writes. The live files are linked.</p>
      <div className={admin.toolbar}>
        {FILES.map(([file, label, url]) => (
          <span key={file}>
            <button className={`btn btn-outline ${admin.small}`} onClick={() => open(file)}><Eye /> {label}</button>{" "}
            <a href={url} target="_blank" rel="noreferrer" className="muted">live</a>
          </span>
        ))}
      </div>
      <form className={admin.toolbar} onSubmit={(e) => { e.preventDefault(); open("markdown", `&path=${encodeURIComponent(path)}`); }}>
        <input value={path} onChange={(e) => setPath(e.target.value)} aria-label="Page path" placeholder="/python/lists" />
        <button className={`btn btn-outline ${admin.small}`}><Eye /> Markdown copy of this page</button>
      </form>
      {error && <p className="notice notice-error">{error}</p>}
      {shown && <pre className={`${admin.code} ${styles.preview}`}>{shown.text}</pre>}
    </section>
  );
}

// --- Change log -------------------------------------------------------------------

const AREAS = [
  ["", "Everything"],
  ["settings", "Settings"],
  ["page", "Page SEO"],
  ["ai_bot", "AI crawlers"],
  ["build", "Builds"],
  ["indexnow", "IndexNow"],
];

export function ChangeLogTab() {
  const [area, setArea] = useState("");
  const [actor, setActor] = useState("");
  const { data, reload } = useApi(`${SEO}/changes/?area=${area}&actor=${actor}`);
  return (
    <>
      <p className="muted">
        Every change made here, and what the site did by itself. Changes made by an admin can be undone.
      </p>
      <div className={admin.toolbar}>
        <select value={area} onChange={(e) => setArea(e.target.value)} aria-label="Area">
          {AREAS.map(([value, label]) => <option key={value} value={value}>{label}</option>)}
        </select>
        <select value={actor} onChange={(e) => setActor(e.target.value)} aria-label="Made by">
          <option value="">By anyone</option>
          <option value="admin">By an admin</option>
          <option value="auto">Automatic</option>
        </select>
      </div>
      {data ? <ChangeTable rows={data} onChange={reload} /> : <p className="page-loading is-loading">Loading…</p>}
    </>
  );
}

function ChangeTable({ rows, onChange }) {
  const [error, setError] = useState("");
  async function undo(row) {
    setError("");
    try {
      await api(`${SEO}/changes/${row.id}/undo/`, { method: "POST" });
      onChange();
    } catch (failure) {
      setError(failure.message);
    }
  }
  if (!rows.length) return <p className="muted">No changes yet.</p>;
  return (
    <>
      {error && <p className="notice notice-error">{error}</p>}
      <table className={admin.table}>
        <thead>
          <tr><th>When</th><th>By</th><th>Change</th><th /></tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr key={row.id} className={row.undone_at ? styles.undone : undefined}>
              <td>{new Date(row.created_at).toLocaleString()}</td>
              <td>{row.actor === "auto" ? <span className="muted">Automatic</span> : row.user || "Admin"}</td>
              <td>
                <strong>{row.summary}</strong>
                {row.target && <span className="muted"> · {row.target}</span>}
                {row.changes?.length > 0 && (
                  <ul className={styles.diff}>
                    {row.changes.map((item) => (
                      <li key={item.field}>
                        {item.field}: {show(item.old)} → {show(item.new)}
                      </li>
                    ))}
                  </ul>
                )}
                {row.undone_at && <div className="muted">Undone {new Date(row.undone_at).toLocaleString()}</div>}
              </td>
              <td>
                {row.can_undo && (
                  <button className={`btn btn-outline ${admin.small}`} onClick={() => undo(row)}>
                    <RotateCcw /> Undo
                  </button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </>
  );
}

function show(value) {
  if (value === null || value === undefined || value === "") return "(empty)";
  if (typeof value === "boolean") return value ? "on" : "off";
  const text = typeof value === "string" ? value : JSON.stringify(value);
  return text.length > 80 ? `${text.slice(0, 80)}…` : text;
}
