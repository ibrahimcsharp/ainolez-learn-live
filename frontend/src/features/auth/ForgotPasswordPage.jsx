import { useState } from "react";
import { Link } from "react-router";
import { api } from "../../shared/api/client";
import { useFormFields, useSubmit } from "../../shared/hooks/useForm";
import { Field, FormError } from "../../shared/ui/Field";
import { AuthCard } from "./AuthCard";

export function ForgotPasswordPage() {
  const [form, onChange] = useFormFields({ email: "" });
  const [message, setMessage] = useState(null);
  const { submit, busy, error } = useSubmit(async () => {
    const data = await api("/auth/forgot-password/", { method: "POST", body: form });
    setMessage(data.detail);
  });

  return (
    <AuthCard title="Reset your password" footer={<Link to="/login">Back to log in</Link>}>
      {message ? (
        <p className="notice notice-success">{message}</p>
      ) : (
        <form onSubmit={submit}>
          <FormError error={error} />
          <Field label="Email" name="email" type="email" autoComplete="email" required
            value={form.email} onChange={onChange} error={error} />
          <button className="btn btn-primary btn-block" disabled={busy}>
            Send reset link
          </button>
        </form>
      )}
    </AuthCard>
  );
}
