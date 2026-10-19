import { useState } from "react";
import { Link, useSearchParams } from "react-router";
import { ApiError, api } from "../../shared/api/client";
import { useFormFields, useSubmit } from "../../shared/hooks/useForm";
import { Field, FormError } from "../../shared/ui/Field";
import { AuthCard } from "./AuthCard";

export function ResetPasswordPage() {
  const token = useSearchParams()[0].get("token");
  const [form, onChange] = useFormFields({ password: "", confirm: "" });
  const [done, setDone] = useState(false);
  const { submit, busy, error } = useSubmit(async () => {
    if (form.password !== form.confirm) {
      throw new ApiError(400, { confirm: ["The two passwords do not match."] });
    }
    await api("/auth/reset-password/", { method: "POST", body: { token, password: form.password } });
    setDone(true);
  });

  if (done) {
    return (
      <AuthCard title="Password changed">
        <p className="notice notice-success">You can now log in with your new password.</p>
        <Link to="/login" className="btn btn-primary btn-block">
          Log in
        </Link>
      </AuthCard>
    );
  }

  return (
    <AuthCard title="Choose a new password">
      <FormError error={error} />
      <form onSubmit={submit}>
        <Field label="New password" name="password" type="password" autoComplete="new-password"
          required minLength={8} value={form.password} onChange={onChange} error={error} />
        <Field label="Repeat new password" name="confirm" type="password" autoComplete="new-password"
          required value={form.confirm} onChange={onChange} error={error} />
        <button className="btn btn-primary btn-block" disabled={busy}>
          Save new password
        </button>
      </form>
    </AuthCard>
  );
}
