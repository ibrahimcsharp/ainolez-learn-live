import { afterEach, beforeEach, expect, test, vi } from "vitest";

const json = (data) => ({
  ok: true,
  status: 200,
  headers: new Headers({ "content-type": "application/json" }),
  json: async () => data,
});
const missing = { ok: false, status: 404, headers: new Headers({ "content-type": "text/html" }) };

let client;
beforeEach(async () => {
  vi.resetModules();
  localStorage.clear();
  client = await import("./client");
});
afterEach(() => vi.unstubAllGlobals());

test("public course, lesson, page, menu and catalog reads have static copies", () => {
  const { staticCopy } = client;
  expect(staticCopy("/public/courses/python/")).toBe("/data/courses/python.json");
  expect(staticCopy("/public/courses/python/lessons/lists/")).toBe("/data/courses/python/lessons/lists.json");
  expect(staticCopy("/public/site/pages/about/")).toBe("/data/site/pages/about.json");
  expect(staticCopy("/public/site/menus/")).toBe("/data/site/menus.json");
  expect(staticCopy("/public/catalog/")).toBe("/data/catalog.json");
  expect(staticCopy("/public/courses/?category=web")).toBeNull();
  expect(staticCopy("/public/seo/?path=/python")).toBeNull(); // it also counts page views
  expect(staticCopy("/learner/courses/1/progress/")).toBeNull();
});

test("a GET uses the static copy and skips the API", async () => {
  const fetch = vi.fn(async () => json({ title: "Python" }));
  vi.stubGlobal("fetch", fetch);
  expect(await client.api("/public/courses/python/")).toEqual({ title: "Python" });
  expect(fetch).toHaveBeenCalledTimes(1);
  expect(fetch.mock.calls[0][0]).toBe("/data/courses/python.json");
});

test("without a copy the API answers", async () => {
  const fetch = vi.fn(async (url) => (url.startsWith("/data/") ? missing : json({ title: "New" })));
  vi.stubGlobal("fetch", fetch);
  expect(await client.api("/public/courses/new/")).toEqual({ title: "New" });
  expect(fetch.mock.calls.map(([url]) => url)).toEqual(["/data/courses/new.json", "/api/v1/public/courses/new/"]);
});

test("a browser that was signed out remembers it", async () => {
  vi.stubGlobal("fetch", vi.fn(async () => ({ ok: false, status: 401 })));
  expect(client.signedInBefore()).toBeNull();
  await client.refreshAccess();
  expect(client.signedInBefore()).toBe(false);
  client.setAccessToken("token");
  expect(client.signedInBefore()).toBe(true);
});
