import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router";
import { afterEach, beforeEach, expect, test, vi } from "vitest";
import { ChangeLogTab, GeoTab, OverviewTab } from "./Center";

const api = vi.fn();
vi.mock("../../../shared/api/client", () => ({ api: (...args) => api(...args) }));

const check = (key, ok, fix = "") => ({ key, ok, label: `Check ${key}`, tip: `Tip ${key}`, fix: ok ? "" : fix });
const overview = {
  seo: { score: 72, pages: 10, pages_ok: 7, checks: [check("google", false)] },
  geo: { score: 91, checks: [check("llms", true), check("indexnow", false, "indexnow_enabled")] },
  fix_next: [
    { kind: "geo", label: "IndexNow tells Bing about changes", tip: "Bing hears sooner.", fix: "indexnow_enabled", count: null },
    { kind: "page", label: "No description", tip: "Open the report.", fix: "", count: 3 },
  ],
  traffic: {
    views_by_day: {}, views_total: 1234, referrals_by_day: {}, totals: { search: 40, ai: 5, social: 2 },
    sources: [{ kind: "ai", source: "ChatGPT", visits: 5 }], ai_pages: [{ path: "/python", visits: 5 }],
  },
  build: { last_build_at: null, pages: 0, indexnow_enabled: false },
  recent_changes: [],
  days: 30,
};
const change = {
  id: 7, created_at: "2026-11-09T10:00:00Z", actor: "admin", user: "admin@example.com", area: "ai_bot",
  target: "GPTBot", summary: "Blocked GPTBot", changes: [{ field: "allowed", old: true, new: false }],
  undone_at: null, can_undo: true,
};

beforeEach(() => {
  api.mockReset();
});
afterEach(cleanup);

test("overview shows both scores, what to fix next and AI visits, and turns a task on", async () => {
  api.mockImplementation(async (path) => (path.startsWith("/admin/seo/overview/") ? overview : {}));
  render(<MemoryRouter><OverviewTab onTab={() => {}} /></MemoryRouter>);
  expect(await screen.findByRole("img", { name: "SEO score: 72 out of 100" })).toBeTruthy();
  expect(screen.getByRole("img", { name: "GEO score: 91 out of 100" })).toBeTruthy();
  expect(screen.getByText("3 × No description")).toBeTruthy();
  expect(screen.getByText("ChatGPT")).toBeTruthy();
  expect(screen.getByText("1,234")).toBeTruthy();

  fireEvent.click(screen.getAllByRole("button", { name: /Turn on/ })[0]);
  await waitFor(() =>
    expect(api).toHaveBeenCalledWith("/admin/seo/settings/", { method: "PATCH", body: { indexnow_enabled: true } }),
  );
});

test("AI & GEO blocks one crawler", async () => {
  const bots = [
    { id: 1, user_agent: "GPTBot", owner: "OpenAI", purpose: "training", allowed: true, notes: "", is_active: true },
    { id: 2, user_agent: "OAI-SearchBot", owner: "OpenAI", purpose: "search", allowed: true, notes: "", is_active: true },
  ];
  api.mockImplementation(async (path) => {
    if (path.startsWith("/admin/seo/settings/")) return { geo_llms_enabled: true, geo_site_summary: "", updated_at: "x" };
    if (path.startsWith("/admin/seo/bots/?")) return { results: bots };
    return {};
  });
  render(<MemoryRouter><GeoTab /></MemoryRouter>);
  fireEvent.click(await screen.findByRole("switch", { name: "GPTBot allowed" }));
  await waitFor(() =>
    expect(api).toHaveBeenCalledWith("/admin/seo/bots/1/", { method: "PATCH", body: { allowed: false } }),
  );
  expect(screen.getByRole("switch", { name: "llms.txt" }).getAttribute("aria-checked")).toBe("true");
});

test("change log shows what changed and undoes it", async () => {
  api.mockImplementation(async (path) => (path.startsWith("/admin/seo/changes/?") ? [change] : {}));
  render(<MemoryRouter><ChangeLogTab /></MemoryRouter>);
  expect(await screen.findByText("Blocked GPTBot")).toBeTruthy();
  expect(screen.getByText("allowed: on → off")).toBeTruthy();
  fireEvent.click(screen.getByRole("button", { name: /Undo/ }));
  await waitFor(() => expect(api).toHaveBeenCalledWith("/admin/seo/changes/7/undo/", { method: "POST" }));
});
