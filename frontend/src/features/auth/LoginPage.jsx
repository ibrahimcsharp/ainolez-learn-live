import { Link, useLocation, useNavigate } from "react-router";
import { homeFor, useAuth } from "../../app/AuthProvider";
import { useFormFields, useSubmit } from "../../shared/hooks/useForm";
import { Field, FormError } from "../../shared/ui/Field";
import { AuthCard } from "./AuthCard";
import { ResendVerification } from "./ResendVerification";

export function LoginPage() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const from = useLocation().state?.from;
  const [form, onChange] = useFormFields({ email: "", password: "" });
  const { submit, busy, error } = useSubmit(async () => {
    const user = await login(form.email, form.password);
    navigate(from ?? homeFor(user), { replace: true });
  });

  return (
    <AuthCard
      title="Welcome back"
      footer={
        <>
          New to ainolez? <Link to="/register">Create a free account</Link>
        </>
      }
    >
      <FormError error={error} />
      {error?.code === "email_not_verified" && <ResendVerification email={form.email} />}
      <form onSubmit={submit}>
        <Field label="Email" name="email" type="email" autoComplete="email" required
          value={form.email} onChange={onChange} error={error} />
        <Field label="Password" name="password" type="password" autoComplete="current-password" required
          value={form.password} onChange={onChange} error={error} />
        <p>
          <Link to="/forgot-password">Forgot your password?</Link>
        </p>
        <button className="btn btn-primary btn-block" disabled={busy}>
          {busy ? "Logging in…" : "Log in"}
        </button>
      </form>
    </AuthCard>
  );
}
