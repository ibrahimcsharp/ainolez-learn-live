import { useEffect, useRef, useState } from "react";
import { Link, useSearchParams } from "react-router";
import { api } from "../../shared/api/client";
import { AuthCard } from "./AuthCard";

export function VerifyEmailPage() {
  const token = useSearchParams()[0].get("token");
  const [result, setResult] = useState({ status: "working" });
  const sent = useRef(false); // tokens are single-use: never send twice

  useEffect(() => {
    if (sent.current) return;
    sent.current = true;
    api("/auth/verify-email/", { method: "POST", body: { token } })
      .then((data) => setResult({ status: "ok", message: data.detail }))
      .catch((err) => setResult({ status: "error", message: err.message }));
  }, [token]);

  return (
    <AuthCard title="Email verification">
      {result.status === "working" && <p className="muted">Checking your link…</p>}
      {result.status === "ok" && (
        <>
          <p className="notice notice-success">{result.message}</p>
          <Link to="/login" className="btn btn-primary btn-block">
            Log in
          </Link>
        </>
      )}
      {result.status === "error" && <p className="notice notice-error">{result.message}</p>}
    </AuthCard>
  );
}
