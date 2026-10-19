import { Navigate, useLocation } from "react-router";
import { homeFor, useAuth } from "./AuthProvider";

/** Shows children only to a logged-in user with the given role. */
export function RequireRole({ role, children }) {
  const { user, ready } = useAuth();
  const location = useLocation();

  if (!ready) return <p className="page-loading">Loading…</p>;
  if (!user) return <Navigate to="/login" replace state={{ from: location.pathname }} />;
  if (user.role !== role) return <Navigate to={homeFor(user)} replace />;
  return children;
}
