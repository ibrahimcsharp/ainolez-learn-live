import { cleanup, render, screen } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router";
import { afterEach, expect, test } from "vitest";
import { AuthContext } from "./AuthProvider";
import { RequireRole } from "./RequireRole";

afterEach(cleanup);

function renderAt(path, user) {
  render(
    <AuthContext.Provider value={{ user, ready: true }}>
      <MemoryRouter initialEntries={[path]}>
        <Routes>
          <Route path="/login" element={<p>login page</p>} />
          <Route path="/dashboard" element={<p>learner dashboard</p>} />
          <Route
            path="/admin"
            element={
              <RequireRole role="super_admin">
                <p>admin panel</p>
              </RequireRole>
            }
          />
        </Routes>
      </MemoryRouter>
    </AuthContext.Provider>,
  );
}

test("visitor is sent to login", () => {
  renderAt("/admin", null);
  expect(screen.getByText("login page")).toBeTruthy();
});

test("learner is sent to their own dashboard", () => {
  renderAt("/admin", { role: "learner" });
  expect(screen.getByText("learner dashboard")).toBeTruthy();
});

test("super admin sees the admin panel", () => {
  renderAt("/admin", { role: "super_admin" });
  expect(screen.getByText("admin panel")).toBeTruthy();
});
