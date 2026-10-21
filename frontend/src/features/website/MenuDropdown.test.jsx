import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router";
import { afterEach, expect, test } from "vitest";
import { MenuDropdown } from "./MenuDropdown";

afterEach(cleanup);

const children = [
  { label: "Python", url: "/python", new_tab: false },
  { label: "GitHub", url: "https://github.com/ainolez", new_tab: true },
];
const show = (link) => render(<MemoryRouter><MenuDropdown link={{ new_tab: false, children, ...link }} /></MemoryRouter>);

test("a heading opens and closes its sub-menu", () => {
  show({ label: "Learn", url: null });
  const toggle = screen.getByRole("button", { name: "Learn" });
  expect(toggle.getAttribute("aria-expanded")).toBe("false");
  expect(screen.queryByRole("link", { name: "Learn" })).toBeNull();

  fireEvent.click(toggle);
  expect(toggle.getAttribute("aria-expanded")).toBe("true");
  expect(screen.getByRole("link", { name: "Python" }).getAttribute("href")).toBe("/python");
  expect(screen.getByRole("link", { name: "GitHub" }).getAttribute("target")).toBe("_blank");

  fireEvent.keyDown(document, { key: "Escape" });
  expect(toggle.getAttribute("aria-expanded")).toBe("false");
});

test("a link with a sub-menu keeps its own link and gets an arrow button", () => {
  show({ label: "Courses", url: "/courses" });
  expect(screen.getByRole("link", { name: "Courses" }).getAttribute("href")).toBe("/courses");
  fireEvent.click(screen.getByRole("button", { name: "Courses menu" }));
  fireEvent.pointerDown(document.body); // a click outside closes it
  expect(screen.getByRole("button", { name: "Courses menu" }).getAttribute("aria-expanded")).toBe("false");
});

test("a header menu dropdown shows sub-links under their heading", () => {
  show({
    label: "Games",
    url: null,
    children: [
      { label: "Tic Tac Toe", url: "/tic-tac-toe", new_tab: false },
      { label: "More", url: null, new_tab: false, children: [{ label: "Chess", url: "/chess", new_tab: false }] },
    ],
  });
  fireEvent.click(screen.getByRole("button", { name: "Games" }));
  expect(screen.getByRole("link", { name: "Tic Tac Toe" }).getAttribute("href")).toBe("/tic-tac-toe");
  expect(screen.getByText("More").tagName).toBe("SPAN");
  expect(screen.getByRole("link", { name: "Chess" }).closest("ul").className).toMatch(/nested/);
});
