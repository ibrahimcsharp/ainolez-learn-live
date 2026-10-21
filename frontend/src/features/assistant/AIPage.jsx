import { ChatPanel } from "./ChatPanel";

export function AIPage() {
  return (
    <div className="container page-body" style={{ maxWidth: "calc(820px + 2 * var(--gutter))" }}>
      <h1>Your free AI tutor</h1>
      <p className="muted">
        Ask about any lesson, paste code that does not work, or explore a new topic. Answers point you
        to the ainolez lessons that cover them.
      </p>
      <ChatPanel full />
    </div>
  );
}
