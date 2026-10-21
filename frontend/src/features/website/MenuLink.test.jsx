import { cleanup, render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router";
import { afterEach, expect, test } from "vitest";
import { MenuLink } from "./MenuLink";

afterEach(cleanup);

const show = (link) => render(<MemoryRouter><MenuLink link={link} /></MemoryRouter>);

test("site paths stay in the app", () => {
  show({ label: "About", url: "/about", new_tab: false });
  const link = screen.getByRole("link", { name: "About" });
  expect(link.getAttribute("href")).toBe("/about");
  expect(link.getAttribute("target")).toBeNull();
});

test("new-tab links open safely in a new tab", () => {
  show({ label: "GitHub", url: "https://github.com/ainolez", new_tab: true });
  const link = screen.getByRole("link", { name: "GitHub" });
  expect(link.getAttribute("target")).toBe("_blank");
  expect(link.getAttribute("rel")).toBe("noopener noreferrer");
});
