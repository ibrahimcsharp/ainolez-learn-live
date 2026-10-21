import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { useState } from "react";
import { afterEach, expect, test, vi } from "vitest";
import { MarkdownEditor } from "./MarkdownEditor";

const uploaded = { id: 7, url: "/media/team.png", alt_text: "team", original_name: "team.png", mime_type: "image/png" };

vi.mock("../../../shared/api/client", () => ({
  api: vi.fn(async (path, { method } = {}) => {
    if (path.startsWith("/admin/content-tools/md-convert/")) return { html: "<p>preview</p>" };
    if (method === "POST") return uploaded; // media upload
    return { results: [] }; // media list
  }),
}));

afterEach(cleanup);

function Editor({ initial }) {
  const [value, setValue] = useState(initial);
  return <MarkdownEditor name="content_md" label="Content" value={value} onChange={(e) => setValue(e.target.value)} />;
}

function select(textarea, start, end) {
  textarea.focus();
  textarea.setSelectionRange(start, end);
}

test("bold wraps the selected words", () => {
  render(<Editor initial="Hello world" />);
  const textarea = screen.getByLabelText("Content");
  select(textarea, 6, 11);
  fireEvent.click(screen.getByLabelText("Bold (Ctrl+B)"));
  expect(textarea.value).toBe("Hello **world**");
});

test("heading and list buttons change whole lines, and pressing again removes them", () => {
  render(<Editor initial={"one\ntwo"} />);
  const textarea = screen.getByLabelText("Content");
  select(textarea, 0, 7);
  fireEvent.click(screen.getByLabelText("Numbered list"));
  expect(textarea.value).toBe("1. one\n2. two");

  select(textarea, 0, 0);
  fireEvent.click(screen.getByLabelText("Heading"));
  expect(textarea.value).toBe("## one\n2. two");
  select(textarea, 0, 0);
  fireEvent.click(screen.getByLabelText("Heading"));
  expect(textarea.value).toBe("one\n2. two");
});

test("note box and code block are inserted on their own lines", () => {
  render(<Editor initial="Intro" />);
  const textarea = screen.getByLabelText("Content");
  select(textarea, 5, 5);
  fireEvent.click(screen.getByLabelText("Note box"));
  fireEvent.click(screen.getByRole("button", { name: "tip" }));
  expect(textarea.value).toBe("Intro\n\n!!! tip\n    Write the note here.\n");

  fireEvent.click(screen.getByLabelText("Code block"));
  expect(textarea.value).toContain("```python\n");
});

test("a pasted image is uploaded to Media and inserted", async () => {
  render(<Editor initial="" />);
  const textarea = screen.getByLabelText("Content");
  const file = new File(["png"], "team.png", { type: "image/png" });
  fireEvent.paste(textarea, { clipboardData: { files: [file] } });
  await waitFor(() => expect(textarea.value).toBe("![team](/media/team.png)\n"));
});
