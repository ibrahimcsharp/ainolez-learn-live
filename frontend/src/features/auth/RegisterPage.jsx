import { useState } from "react";
import { Link } from "react-router";
import { api } from "../../shared/api/client";
import { useFormFields, useSubmit } from "../../shared/hooks/useForm";
import { Field, FormError } from "../../shared/ui/Field";
import { AuthCard } from "./AuthCard";
import { ResendVerification } from "./ResendVerification";

export function RegisterPage() {
  const [form, onChange] = useFormFields({ full_name: "", username: "", email: "", password: "" });
  const [done, setDone] = useState(false);
  const { submit, busy, error } = useSubmit(async () => {
    await api("/auth/register/", { method: "POST", body: form });
    setDone(true);
  });

  if (done) {
    return (
      <AuthCard title="Check your email">
        <p>
          We sent a verification link to <strong>{form.email}</strong>. Open it to activate your
          account.
        </p>
        <ResendVerification email={form.email} />
      </AuthCard>
    );
  }

  return (
    <AuthCard
      title="Create your free account"
      footer={
        <>
          Already have an account? <Link to="/login">Log in</Link>
        </>
      }
    >
      <FormError error={error} />
      <form onSubmit={submit}>
        <Field label="Full name" name="full_name" autoComplete="name"
          value={form.full_name} onChange={onChange} error={error} />
        <Field label="Username" name="username" autoComplete="username" required
          value={form.username} onChange={onChange} error={error} />
        <Field label="Email" name="email" type="email" autoComplete="email" required
          value={form.email} onChange={onChange} error={error} />
        <Field label="Password" name="password" type="password" autoComplete="new-password" required
          minLength={8} value={form.password} onChange={onChange} error={error} />
        <button className="btn btn-primary btn-block" disabled={busy}>
          {busy ? "Creating account…" : "Sign up free"}
        </button>
      </form>
    </AuthCard>
  );
}
