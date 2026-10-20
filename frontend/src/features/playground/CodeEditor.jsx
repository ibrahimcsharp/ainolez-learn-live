import { Compartment } from "@codemirror/state";
import { basicSetup, EditorView } from "codemirror";
import { useEffect, useRef } from "react";

// Each language mode downloads only when a lesson needs it.
// CSS examples are whole HTML pages with a <style> tag, so they use the HTML mode.
const LANGUAGES = {
  html: () => import("@codemirror/lang-html").then((m) => m.html()),
  css: () => import("@codemirror/lang-html").then((m) => m.html()),
  javascript: () => import("@codemirror/lang-javascript").then((m) => m.javascript()),
  python: () => import("@codemirror/lang-python").then((m) => m.python()),
  sql: () => import("@codemirror/lang-sql").then((m) => m.sql()),
};

/** CodeMirror 6 editor. Loaded lazily (see TryIt) because it is the biggest dependency. */
export default function CodeEditor({ value, onChange, language }) {
  const host = useRef(null);
  const view = useRef(null);
  const changed = useRef(onChange);
  changed.current = onChange;

  useEffect(() => {
    const mode = new Compartment();
    const editor = new EditorView({
      doc: value,
      parent: host.current,
      extensions: [
        basicSetup,
        mode.of([]),
        EditorView.updateListener.of((update) => {
          if (update.docChanged) changed.current(update.state.doc.toString());
        }),
      ],
    });
    view.current = editor;
    LANGUAGES[language]?.().then((support) => editor.dispatch({ effects: mode.reconfigure(support) }));
    return () => editor.destroy();
  }, [language]); // `value` is synced by the next effect, not by rebuilding the editor

  // Outside changes (e.g. "Reset") replace the editor text.
  useEffect(() => {
    const editor = view.current;
    if (editor && editor.state.doc.toString() !== value) {
      editor.dispatch({ changes: { from: 0, to: editor.state.doc.length, insert: value } });
    }
  }, [value]);

  return <div ref={host} />;
}
