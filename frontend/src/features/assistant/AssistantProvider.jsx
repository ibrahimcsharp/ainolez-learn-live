import { createContext, useContext, useEffect, useState } from "react";
import { useAuth } from "../../app/AuthProvider";
import { api } from "../../shared/api/client";
import { useApi } from "../../shared/hooks/useApi";

const AssistantContext = createContext(null);
const STORAGE_KEY = "ainolez.chat";

/** Saved in the browser only: a random id for visitors and the open conversation. */
function loadSaved() {
  try {
    const saved = JSON.parse(localStorage.getItem(STORAGE_KEY)) ?? {};
    return { session: saved.session ?? crypto.randomUUID(), conversationId: saved.conversationId ?? null };
  } catch {
    return { session: crypto.randomUUID(), conversationId: null };
  }
}

function save(state) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  } catch {
    // private mode: the chat still works, it is just not remembered
  }
}

/** The AI tutor's state, shared by the floating chat, the /ai page and "Ask AI" buttons. */
export function AssistantProvider({ children }) {
  const { data: config } = useApi("/assistant/config/");
  const [saved, setSaved] = useState(loadSaved);
  const [messages, setMessages] = useState([]);
  const [open, setOpen] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState(null);
  const [lessonId, setLessonId] = useState(null);
  const headers = { "X-Chat-Session": saved.session };

  useEffect(() => {
    save(saved);
  }, [saved]);

  // Reload the open conversation after a page refresh. A chat started before
  // logging in or out belongs to someone else now, so it is simply forgotten.
  const { session, conversationId } = saved;
  const { ready, user } = useAuth();
  const userId = user?.id ?? null;
  const [owner, setOwner] = useState(undefined); // who the shown chat belongs to

  useEffect(() => {
    if (!ready || owner === userId) return;
    if (owner !== undefined) {
      setMessages([]); // logged in or out: start a fresh chat
      setSaved((s) => ({ ...s, conversationId: null }));
    }
    setOwner(userId);
  }, [ready, userId, owner]);

  useEffect(() => {
    if (!ready || !conversationId || messages.length) return;
    api(`/assistant/conversations/${conversationId}/`, { headers: { "X-Chat-Session": session } })
      .then((data) => setMessages(data.messages))
      .catch(() => setSaved((s) => ({ ...s, conversationId: null })));
  }, [ready, conversationId, session, messages.length]);

  async function ask(question, { code = "", language = "" } = {}) {
    setOpen(true);
    setError(null);
    setBusy(true);
    setMessages((list) => [...list, { id: `q${Date.now()}`, role: "user", content_html: escapeHtml(question) }]);
    try {
      const data = await api("/assistant/messages/", {
        method: "POST",
        headers,
        body: { question, conversation_id: conversationId, lesson_id: lessonId, code, language },
      });
      setSaved((s) => ({ ...s, conversationId: data.conversation_id }));
      setMessages((list) => [...list, data.answer]);
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  async function feedback(messageId, value) {
    await api(`/assistant/messages/${messageId}/feedback/`, { method: "POST", headers, body: { value } });
    setMessages((list) => list.map((m) => (m.id === messageId ? { ...m, feedback: value } : m)));
  }

  function newChat() {
    setMessages([]);
    setError(null);
    setSaved((s) => ({ ...s, conversationId: null }));
  }

  const value = { config, messages, open, setOpen, busy, error, ask, feedback, newChat, lessonId, setLessonId };
  return <AssistantContext.Provider value={value}>{children}</AssistantContext.Provider>;
}

export const useAssistant = () => useContext(AssistantContext);

function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return `<p>${div.innerHTML}</p>`;
}
