import { BookmarkPlus, Check, PlugZap, Plus, RefreshCw, Save, Search } from "lucide-react";
import { useState } from "react";
import { api } from "../../../shared/api/client";
import { useApi } from "../../../shared/hooks/useApi";
import { useFormFields, useSubmit } from "../../../shared/hooks/useForm";
import { Field, FormError } from "../../../shared/ui/Field";
import { EditPanel, useResourceForm } from "../shared/EditPanel";
import { RecordActions, StatusBadge } from "../shared/RecordActions";
import styles from "../shared/admin.module.css";

const ADMIN = "/admin/assistant";
const TABS = {
  settings: ["General and model", SettingsTab],
  prompt: ["Persona and rules", PromptTab],
  knowledge: ["Knowledge base", KnowledgeTab],
  faq: ["Curated FAQ", FaqTab],
  chats: ["Conversations", ConversationsTab],
  usage: ["Usage and cost", UsageTab],
};

/** The AI tutor control panel (PLANNING.md 6.6). */
export function AIPanelPage() {
  const [tab, setTab] = useState("settings");
  const Tab = TABS[tab][1];
  return (
    <>
      <h1>AI tutor</h1>
      <div className={styles.tabs}>
        {Object.entries(TABS).map(([key, [label]]) => (
          <button key={key} className={`btn btn-outline ${styles.small}`} aria-pressed={tab === key} onClick={() => setTab(key)}>
            {label}
          </button>
        ))}
      </div>
      <Tab />
    </>
  );
}

function SettingsTab() {
  const { data, reload } = useApi(`${ADMIN}/settings/`);
  const [test, setTest] = useState(null);
  if (!data) return <p className="page-loading">Loading…</p>;

  async function runTest() {
    setTest({ detail: "Testing…" });
    setTest(await api(`${ADMIN}/test/`, { method: "POST" }));
  }

  return (
    <>
      <SettingsForm key={data.updated_at} initial={data} onSaved={reload} />
      <section className="card">
        <h3>API connection</h3>
        <p className="muted">The Anthropic API key lives in the server's .env file (ANTHROPIC_API_KEY), never in the browser.</p>
        <button className="btn btn-outline" onClick={runTest}><PlugZap /> Test connection</button>{" "}
        {test && (
          <span className={test.ok === false ? styles.danger : ""}>
            {test.ok ? `✓ ${test.model} answered in ${test.latency_ms} ms` : test.detail}
          </span>
        )}
      </section>
    </>
  );
}

function SettingsForm({ initial, onSaved }) {
  const flat = { ...initial, starter_questions: initial.starter_questions.join("\n") };
  const toBody = ({ models, updated_at, ...v }) => ({
    ...v, starter_questions: v.starter_questions.split("\n").map((q) => q.trim()).filter(Boolean),
  });
  const [values, onChange, setValues] = useFormFields(flat);
  const { submit, busy, error } = useSubmit(async () => {
    await api(`${ADMIN}/settings/`, { method: "PATCH", body: toBody(values) });
    onSaved();
  });
  const check = (name, label) => (
    <label key={name} style={{ display: "block" }}>
      <input type="checkbox" checked={values[name]} onChange={(e) => setValues({ ...values, [name]: e.target.checked })} /> {label}
    </label>
  );
  const field = (label, name, props = {}) => (
    <Field label={label} name={name} value={values[name]} onChange={onChange} error={error} {...props} />
  );

  return (
    <form className={`card ${styles.panel}`} onSubmit={submit}>
      <FormError error={error} />
      <div className={styles.formGrid}>
        <div>
          {check("enabled", "Tutor switched on")}
          {check("enabled_for_visitors", "Visitors can chat")}
          {check("enabled_for_learners", "Learners can chat")}
        </div>
        {field("Bot name", "bot_name")}
        {field("Model", "model", { as: "select", children: initial.models.map((m) => <option key={m}>{m}</option>) })}
        {field("Effort (higher = deeper, slower)", "effort", {
          as: "select", children: ["low", "medium", "high"].map((e) => <option key={e}>{e}</option>),
        })}
        {field("Max answer tokens", "max_output_tokens", { type: "number", min: 200 })}
        {field("Questions per visitor per day", "visitor_daily_limit", { type: "number", min: 0 })}
        {field("Questions per learner per day", "learner_daily_limit", { type: "number", min: 0 })}
        {field("Monthly token budget (0 = none)", "monthly_token_budget", { type: "number", min: 0 })}
        {field("Keep chats for (days)", "log_retention_days", { type: "number", min: 1 })}
        <div style={{ gridColumn: "1 / -1" }}>
          {field("Welcome message", "welcome_message", { as: "textarea", rows: 2 })}
          {field("Starter questions (one per line)", "starter_questions", { as: "textarea", rows: 3 })}
        </div>
      </div>
      <button className="btn btn-primary" disabled={busy}><Save /> {busy ? "Saving…" : "Save settings"}</button>
    </form>
  );
}

function PromptTab() {
  const versions = useApi(`${ADMIN}/prompts/`);
  const current = versions.data?.find((v) => v.is_current);
  const [text, setText] = useState(null);
  const [notes, setNotes] = useState("");
  const { submit, busy, error } = useSubmit(async () => {
    await api(`${ADMIN}/prompts/`, { method: "POST", body: { system_prompt: text, notes, make_current: true } });
    setText(null);
    setNotes("");
    versions.reload();
  });
  if (!versions.data) return <p className="page-loading">Loading…</p>;

  async function activate(version) {
    await api(`${ADMIN}/prompts/${version.id}/activate/`, { method: "POST" });
    versions.reload();
  }

  return (
    <>
      <form className={`card ${styles.panel}`} onSubmit={submit}>
        <h3>Instructions in use: version {current?.version_no}</h3>
        <p className="muted">Saving creates a new version, so you can always roll back.</p>
        <FormError error={error} />
        <textarea className={styles.code} rows={16} style={{ width: "100%" }} value={text ?? current?.system_prompt ?? ""}
          onChange={(e) => setText(e.target.value)} aria-label="System prompt" />
        <input placeholder="What changed?" value={notes} onChange={(e) => setNotes(e.target.value)} style={{ width: "100%", margin: "8px 0" }} />
        <button className="btn btn-primary" disabled={busy || text === null}><Save /> Save as new version</button>
      </form>
      <table className={styles.table}>
        <tbody>
          {versions.data.map((version) => (
            <tr key={version.id}>
              <td>v{version.version_no} {version.is_current && <strong>(in use)</strong>}</td>
              <td>{version.notes}</td>
              <td>{new Date(version.created_at).toLocaleString()}</td>
              <td>{!version.is_current && <button className={`btn btn-outline ${styles.small}`} onClick={() => activate(version)}><Check /> Use this version</button>}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </>
  );
}

function KnowledgeTab() {
  const BASE = `${ADMIN}/sources`;
  const list = useApi(`${BASE}/?page_size=500`);
  const [editing, setEditing] = useState(null);
  const [query, setQuery] = useState("");
  const [results, setResults] = useState(null);
  const [message, setMessage] = useState(null);

  async function reindexAll() {
    setMessage((await api(`${BASE}/reindex-all/`, { method: "POST" })).detail);
  }

  async function search(event) {
    event.preventDefault();
    setResults(await api(`${BASE}/search/?q=${encodeURIComponent(query)}`));
  }

  return (
    <>
      <div className={styles.toolbar}>
        <p className="muted" style={{ margin: 0 }}>
          Published lessons are added and updated automatically. Add documents for anything else the tutor should know.
        </p>
        <div className={styles.actions}>
          <button className="btn btn-outline" onClick={reindexAll}><RefreshCw /> Re-index everything</button>
          <button className="btn btn-primary" onClick={() => setEditing({ title: "", url: "", body: "" })}><Plus /> Add document</button>
        </div>
      </div>
      {message && <p className="notice notice-info">{message}</p>}
      {editing && (
        <DocumentForm key={editing.id ?? "new"} base={BASE} initial={editing}
          onSaved={() => { setEditing(null); list.reload(); }} onCancel={() => setEditing(null)} />
      )}
      <form onSubmit={search} className={`card ${styles.panel}`}>
        <h3>Test search</h3>
        <div className={styles.actions} style={{ justifyContent: "flex-start" }}>
          <input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="A question a learner might ask" style={{ flex: 1 }} />
          <button className="btn btn-outline"><Search /> Search</button>
        </div>
        {results?.length === 0 && <p className="muted">Nothing found: the tutor would answer from general knowledge.</p>}
        {results?.map((r, i) => (
          <p key={i}><strong>[{i + 1}] {r.title}</strong> <span className="muted">{r.text.slice(0, 220)}…</span></p>
        ))}
      </form>
      <table className={styles.table}>
        <thead><tr><th>Source</th><th>Type</th><th>Chunks</th><th>Indexed</th><th /></tr></thead>
        <tbody>
          {(list.data?.results ?? []).map((source) => (
            <tr key={source.id}>
              <td>{source.title} <StatusBadge row={source} /> {source.status === "failed" && <span className={styles.danger}>{source.error}</span>}</td>
              <td>{source.type}</td>
              <td>{source.chunk_count}</td>
              <td>{source.last_indexed_at ? new Date(source.last_indexed_at).toLocaleString() : source.status}</td>
              <td>
                <RecordActions base={BASE} row={source} onChange={list.reload}
                  onEdit={source.type === "document" ? setEditing : undefined}>
                  <button className={`btn btn-outline ${styles.small}`}
                    onClick={() => api(`${BASE}/${source.id}/reindex/`, { method: "POST" }).then((d) => setMessage(d.detail))}>
                    <RefreshCw /> Re-index
                  </button>
                </RecordActions>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </>
  );
}

function DocumentForm({ base, initial, onSaved, onCancel }) {
  const form = useResourceForm(base, initial, onSaved);
  const { values, onChange, error } = form;
  return (
    <EditPanel title={initial.id ? "Edit document" : "New document"} form={form} onCancel={onCancel}>
      <Field label="Title" name="title" required value={values.title} onChange={onChange} error={error} />
      <Field label="Link to cite (optional)" name="url" value={values.url} onChange={onChange} error={error} />
      <div style={{ gridColumn: "1 / -1" }}>
        <Field label="Text or Markdown" name="body" as="textarea" rows={10} required value={values.body ?? ""}
          onChange={onChange} error={error} />
      </div>
    </EditPanel>
  );
}

function FaqTab() {
  const BASE = `${ADMIN}/faq`;
  const list = useApi(`${BASE}/?page_size=500`);
  const [editing, setEditing] = useState(null);
  return (
    <>
      <div className={styles.toolbar}>
        <p className="muted" style={{ margin: 0 }}>A question close to one of these gets the curated answer, free and instant.</p>
        <button className="btn btn-primary" onClick={() => setEditing({ question: "", answer_md: "", keywords: "" })}><Plus /> New FAQ</button>
      </div>
      {editing && <FaqForm key={editing.id ?? "new"} base={BASE} initial={editing}
        onSaved={() => { setEditing(null); list.reload(); }} onCancel={() => setEditing(null)} />}
      <table className={styles.table}>
        <tbody>
          {(list.data?.results ?? []).map((faq) => (
            <tr key={faq.id}>
              <td><strong>{faq.question}</strong> <StatusBadge row={faq} /><div className="muted">{faq.answer_md.slice(0, 140)}</div></td>
              <td>{faq.hit_count} uses</td>
              <td><RecordActions base={BASE} row={faq} onChange={list.reload} onEdit={setEditing} /></td>
            </tr>
          ))}
        </tbody>
      </table>
    </>
  );
}

export function FaqForm({ base, initial, onSaved, onCancel }) {
  const form = useResourceForm(base, initial, onSaved);
  const { values, onChange, error } = form;
  return (
    <EditPanel title={initial.id ? "Edit FAQ" : "New FAQ"} form={form} onCancel={onCancel}>
      <Field label="Question" name="question" required value={values.question} onChange={onChange} error={error} />
      <Field label="Other ways to ask (separate with |)" name="keywords" value={values.keywords} onChange={onChange} error={error} />
      <div style={{ gridColumn: "1 / -1" }}>
        <Field label="Answer (Markdown)" name="answer_md" as="textarea" rows={6} required value={values.answer_md}
          onChange={onChange} error={error} />
      </div>
    </EditPanel>
  );
}

function ConversationsTab() {
  const [negative, setNegative] = useState(false);
  const list = useApi(`${ADMIN}/conversations/?negative=${negative ? 1 : 0}`);
  const [openId, setOpenId] = useState(null);
  const [faqDraft, setFaqDraft] = useState(null);
  const chat = useApi(openId ? `${ADMIN}/conversations/${openId}/` : null);

  function toFaq(index) {
    const messages = chat.data.messages;
    const question = messages[index - 1]?.content_html.replace(/<[^>]+>/g, "") ?? "";
    const answer = messages[index].content_html.replace(/<[^>]+>/g, "");
    setFaqDraft({ question: question.slice(0, 300), answer_md: answer, keywords: "" });
  }

  return (
    <>
      <label>
        <input type="checkbox" checked={negative} onChange={(e) => setNegative(e.target.checked)} /> Only chats with 👎 answers
      </label>
      {faqDraft && <FaqForm base={`${ADMIN}/faq`} initial={faqDraft} onSaved={() => setFaqDraft(null)} onCancel={() => setFaqDraft(null)} />}
      <div className={styles.split} style={{ marginTop: 12 }}>
        <table className={styles.table}>
          <tbody>
            {(list.data ?? []).map((c) => (
              <tr key={c.id} onClick={() => setOpenId(c.id)} style={{ cursor: "pointer" }}>
                <td>{c.title}<div className="muted">{c.who} · {c.message_count} messages {c.thumbs_down > 0 && `· 👎 ${c.thumbs_down}`}</div></td>
                <td>{new Date(c.updated_at).toLocaleDateString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
        <div className={styles.preview}>
          {!chat.data && <p className="muted">Pick a conversation.</p>}
          {chat.data?.messages.map((m, i) => (
            <div key={m.id} style={{ marginBottom: 12 }}>
              <strong>{m.role === "user" ? "Learner" : `Tutor (${m.answered_by})`}</strong> {m.feedback === "down" && "👎"}{m.feedback === "up" && "👍"}
              <div className="lesson-content" dangerouslySetInnerHTML={{ __html: m.content_html }} />
              {m.role === "assistant" && (
                <button className={`btn btn-outline ${styles.small}`} onClick={() => toFaq(i)}><BookmarkPlus /> Save as FAQ</button>
              )}
            </div>
          ))}
        </div>
      </div>
    </>
  );
}

function UsageTab() {
  const { data } = useApi(`${ADMIN}/usage/`);
  if (!data) return <p className="page-loading">Loading…</p>;
  const used = data.month.tokens_in + data.month.tokens_out;
  const budget = data.monthly_token_budget;
  return (
    <>
      <div className={styles.formGrid}>
        <div className="card"><strong>{data.month.requests}</strong><div className="muted">model answers this month</div></div>
        <div className="card"><strong>{used.toLocaleString()}</strong><div className="muted">tokens this month{budget ? ` of ${budget.toLocaleString()}` : ""}</div></div>
        <div className="card"><strong>${data.month.cost.toFixed(2)}</strong><div className="muted">estimated cost this month</div></div>
        <div className="card"><strong>👍 {data.feedback.up} · 👎 {data.feedback.down}</strong><div className="muted">answer feedback</div></div>
      </div>
      <table className={styles.table} style={{ marginTop: 16 }}>
        <thead><tr><th>Date</th><th>Model</th><th>Who</th><th>Answers</th><th>Tokens in / out</th><th>Cost</th></tr></thead>
        <tbody>
          {data.days.map((d, i) => (
            <tr key={i}>
              <td>{d.date}</td><td>{d.model}</td><td>{d.audience}</td><td>{d.requests}</td>
              <td>{d.tokens_in.toLocaleString()} / {d.tokens_out.toLocaleString()}</td><td>${d.est_cost.toFixed(4)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </>
  );
}
