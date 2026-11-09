import { act, cleanup, fireEvent, render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router";
import { afterEach, beforeEach, expect, test, vi } from "vitest";

const web = { name: "Web", slug: "web", description: "", icon: "", color: "#e34f26" };
const data = { name: "Data", slug: "data", description: "", icon: "", color: "#00758f" };
const course = (slug, title, category, level = "beginner") => ({
  id: slug,
  slug,
  title,
  category,
  level,
  short_description: `${title} from zero`,
  language_key: "other",
  estimated_minutes: 90,
  lesson_count: 8,
  thumbnail_url: null,
});
const catalog = {
  categories: [web, data],
  courses: [course("html", "HTML", web), course("sql", "SQL", data, "intermediate")],
  paths: [],
};

const api = vi.fn();
vi.mock("../../shared/api/client", () => ({ api: (...args) => api(...args) }));

beforeEach(() => {
  vi.resetModules();
  localStorage.clear();
  api.mockReset();
});
afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
});

async function renderPage() {
  const { CatalogPage } = await import("./CatalogPage");
  render(
    <MemoryRouter initialEntries={["/courses"]}>
      <CatalogPage />
    </MemoryRouter>,
  );
}

test("shows placeholders, then the courses from catalog.json, and filters them", async () => {
  let reply;
  vi.stubGlobal("fetch", vi.fn(() => new Promise((resolve) => (reply = resolve))));
  await renderPage();
  expect(screen.getByRole("status", { name: "Loading courses" })).toBeTruthy();

  await act(async () => reply({ ok: true, json: async () => catalog }));
  expect(screen.getByText("2 courses", { selector: "p" })).toBeTruthy();
  expect(api).not.toHaveBeenCalled(); // the static file was enough

  fireEvent.change(screen.getByLabelText("Search courses"), { target: { value: "sql" } });
  expect(screen.getByText("1 of 2 courses", { selector: "p", exact: false })).toBeTruthy();
  expect(screen.queryByRole("heading", { name: "HTML" })).toBeNull();

  fireEvent.click(screen.getByRole("button", { name: /Clear filters/ }));
  fireEvent.click(screen.getByRole("button", { name: /Web/ }));
  expect(screen.getByRole("heading", { name: "HTML" })).toBeTruthy();
  expect(screen.queryByRole("heading", { name: "SQL" })).toBeNull();
});

test("asks the API when catalog.json is missing", async () => {
  vi.stubGlobal("fetch", vi.fn(async () => ({ ok: false })));
  api.mockResolvedValue(catalog);
  await renderPage();
  expect(await screen.findByText("2 courses", { selector: "p" })).toBeTruthy();
  expect(api).toHaveBeenCalledWith("/public/catalog/");
});
