import { useEffect, useRef, useState } from "react";
import { Link } from "react-router";
import { useAssistant } from "./AssistantProvider";
import styles from "./Chat.module.css";

/** The conversation with the AI tutor. Answers arrive as sanitised HTML from the server. */
export function ChatPanel({ full = false }) {
  const { config, messages, busy, error, ask, feedback, newChat, lessonId } = useAssistant();
  const [question, setQuestion] = useState("");
  const end = useRef(null);

  useEffect(() => {
    end.current?.scrollIntoView({ block: "end" });
  }, [messages, busy]);

  function submit(event) {
    event.preventDefault();
    if (!question.trim() || busy) return;
    ask(question.trim());
    setQuestion("");
  }

  if (config && !config.enabled) return <p className={styles.note}>The AI tutor is switched off right now.</p>;

  return (
    <div className={`${styles.panel} ${full ? styles.full : ""}`}>
      <header className={styles.head}>
        <strong>✨ {config?.bot_name ?? "ainolez AI"}</strong>
        {lessonId && <span className={styles.context}>knows this lesson</span>}
        {messages.length > 0 && (
          <button className={styles.link} onClick={newChat}>
            New chat
          </button>
        )}
      </header>

      <div className={styles.messages} aria-live="polite">
        {messages.length === 0 && (
          <div className={styles.welcome}>
            <p>{config?.welcome_message}</p>
            {config?.starter_questions?.map((starter) => (
              <button key={starter} className={styles.starter} onClick={() => ask(starter)}>
                {starter}
              </button>
            ))}
          </div>
        )}
        {messages.map((message) => (
          <div key={message.id} className={message.role === "user" ? styles.mine : styles.theirs}>
            <div className="lesson-content" dangerouslySetInnerHTML={{ __html: message.content_html }} />
            {message.sources?.length > 0 && (
              <p className={styles.sources}>
                Read more:{" "}
                {message.sources.map((source, i) => (
                  <Link key={source.url} to={source.url}>
                    [{i + 1}] {source.title}
                  </Link>
                ))}
              </p>
            )}
            {message.role === "assistant" && message.answered_by !== "system" && typeof message.id === "number" && (
              <div className={styles.feedback}>
                {["up", "down"].map((value) => (
                  <button key={value} aria-pressed={message.feedback === value} aria-label={`Answer was ${value === "up" ? "helpful" : "not helpful"}`}
                    onClick={() => feedback(message.id, value)}>
                    {value === "up" ? "👍" : "👎"}
                  </button>
                ))}
              </div>
            )}
          </div>
        ))}
        {busy && <div className={`${styles.theirs} ${styles.typing}`}>Thinking…</div>}
        {error && <p className="notice notice-error">{error}</p>}
        <div ref={end} />
      </div>

      <form className={styles.form} onSubmit={submit}>
        <textarea value={question} onChange={(e) => setQuestion(e.target.value)} rows={2} maxLength={2000}
          placeholder="Ask about code, a lesson, or AI…" aria-label="Your question"
          onKeyDown={(e) => e.key === "Enter" && !e.shiftKey && submit(e)} />
        <button className="btn btn-primary" disabled={busy || !question.trim()}>
          Ask
        </button>
      </form>
      <p className={styles.note}>The tutor can make mistakes. It gives hints, not quiz answers.</p>
    </div>
  );
}
