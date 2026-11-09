import { afterEach, expect, test, vi } from "vitest";

afterEach(() => {
  vi.resetModules();
  vi.restoreAllMocks();
});

test("the first page of a visit says where the visitor came from, later pages do not", async () => {
  vi.spyOn(document, "referrer", "get").mockReturnValue("https://chatgpt.com/c/123?x=1");
  window.history.replaceState(null, "", "/python?utm_source=chatgpt.com");
  const { arrival } = await import("./SeoManager");
  expect(arrival()).toBe("&ref=https%3A%2F%2Fchatgpt.com%2Fc%2F123&utm=chatgpt.com");
  expect(arrival()).toBe("");
});

test("a visit from inside the site sends nothing", async () => {
  vi.spyOn(document, "referrer", "get").mockReturnValue(`${window.location.origin}/courses`);
  window.history.replaceState(null, "", "/python");
  const { arrival } = await import("./SeoManager");
  expect(arrival()).toBe("");
});
