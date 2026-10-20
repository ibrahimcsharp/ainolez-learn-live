import { useAssistant } from "./AssistantProvider";
import { ChatPanel } from "./ChatPanel";
import styles from "./Chat.module.css";

/** The floating "Ask AI" button on every public page, and the docked chat it opens. */
export function ChatLauncher() {
  const { config, open, setOpen } = useAssistant();
  if (!config?.enabled) return null;

  return (
    <>
      {open && (
        <div className={styles.dock} role="dialog" aria-label="AI tutor">
          <button className={styles.close} onClick={() => setOpen(false)} aria-label="Close the AI tutor">
            ×
          </button>
          <ChatPanel />
        </div>
      )}
      {!open && (
        <button className={styles.launcher} onClick={() => setOpen(true)}>
          ✨ Ask AI
        </button>
      )}
    </>
  );
}
