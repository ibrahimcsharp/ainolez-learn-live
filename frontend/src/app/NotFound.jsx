import { Link } from "react-router";

export function NotFound() {
  return (
    <div className="container page-loading">
      <h1>Page not found</h1>
      <Link to="/">Back to the home page</Link>
    </div>
  );
}
