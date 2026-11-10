import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router";
import { afterEach, beforeEach, expect, test, vi } from "vitest";
import { CoursesPage, matches } from "./CoursesPage";

const api = vi.fn();
vi.mock("../../../shared/api/client", () => ({ api: (...args) => api(...args) }));

const course = (id, title, status = "published") => ({
  id, title, slug: title.toLowerCase().replace(/ /g, "-"), category_name: "Programming", status, is_active: true,
});

beforeEach(() => {
  api.mockReset();
});
afterEach(cleanup);

test("search matches title, address, category and status words", () => {
  const row = course(1, "Python Basics", "draft");
  expect(matches(row, "python")).toBe(true);
  expect(matches(row, "basics draft")).toBe(true);
  expect(matches(row, "programming")).toBe(true);
  expect(matches(row, "sql")).toBe(false);
});

test("shows a loader, then the list, and searches without asking the API again", async () => {
  api.mockResolvedValue({ results: [course(1, "Python Basics"), course(2, "SQL Intro", "draft")] });
  render(<MemoryRouter><CoursesPage /></MemoryRouter>);
  expect(screen.getByRole("status", { name: "Loading courses" })).toBeTruthy();

  expect(await screen.findByText("Python Basics")).toBeTruthy();
  expect(screen.queryByRole("status", { name: "Loading courses" })).toBeNull();
  expect(api).toHaveBeenCalledWith("/admin/catalog/courses/?page_size=500");

  fireEvent.change(screen.getByPlaceholderText("Search courses"), { target: { value: "sql" } });
  expect(screen.queryByText("Python Basics")).toBeNull();
  expect(screen.getByText("SQL Intro")).toBeTruthy();
  fireEvent.change(screen.getByPlaceholderText("Search courses"), { target: { value: "rust" } });
  expect(screen.getByText("No course matches “rust”.")).toBeTruthy();
  expect(api).toHaveBeenCalledTimes(1);
});
