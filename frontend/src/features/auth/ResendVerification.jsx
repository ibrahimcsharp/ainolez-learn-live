import { useState } from "react";
import { api } from "../../shared/api/client";

export function ResendVerification({ email }) {
  const [sent, setSent] = useState(false);

  async function resend() {
    await api("/auth/resend-verification/", { method: "POST", body: { email } }).catch(() => {});
    setSent(true);
  }

  if (sent) return <p className="notice notice-info">A new verification email is on its way.</p>;
  return (
    <p>
      <button type="button" className="btn btn-outline" onClick={resend}>
        Send the verification email again
      </button>
    </p>
  );
}
