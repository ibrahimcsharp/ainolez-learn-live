import { act, cleanup, render, screen } from "@testing-library/react";
import { afterEach, beforeEach, expect, test, vi } from "vitest";

const fromApi = { header: [{ label: "Fresh", url: "/fresh", new_tab: false }], footer: [] };
let answer;

vi.mock("../../shared/api/client", () => ({ api: vi.fn(() => answer) }));

beforeEach(() => {
  vi.resetModules();
  document.getElementById("site-menus")?.remove();
  localStorage.clear();
});
afterEach(cleanup);

function Header({ useMenus }) {
  return <p>{useMenus().header.map((link) => link.label).join(",")}</p>;
}

test("menus embedded in the prerendered page show on first paint, then the API refreshes them", async () => {
  const script = document.createElement("script");
  script.type = "application/json";
  script.id = "site-menus";
  script.textContent = JSON.stringify({ header: [{ label: "Embedded", url: "/a", new_tab: false }], footer: [] });
  document.head.append(script);
  let reply;
  answer = new Promise((resolve) => (reply = resolve));

  const { useMenus, ready } = await import("./menus");
  render(<Header useMenus={useMenus} />);
  expect(screen.getByText("Embedded")).toBeTruthy();

  await act(async () => {
    reply(fromApi);
    await ready;
  });
  expect(screen.getByText("Fresh")).toBeTruthy();
  expect(JSON.parse(localStorage.getItem("ainolez.menus"))).toEqual(fromApi);
});

test("without an embedded copy the last saved menus are used", async () => {
  localStorage.setItem("ainolez.menus", JSON.stringify({ header: [{ label: "Saved", url: "/s" }], footer: [] }));
  answer = new Promise(() => {}); // API still loading
  const { useMenus } = await import("./menus");
  render(<Header useMenus={useMenus} />);
  expect(screen.getByText("Saved")).toBeTruthy();
});
