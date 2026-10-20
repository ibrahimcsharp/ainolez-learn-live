import { useState } from "react";
import { useAuth } from "../../app/AuthProvider";
import { api } from "../../shared/api/client";
import { useFormFields, useSubmit } from "../../shared/hooks/useForm";
import { Field, FormError } from "../../shared/ui/Field";

export function ProfilePage() {
  const { user, setUser } = useAuth();
  const [form, onChange] = useFormFields({
    full_name: user.full_name,
    headline: user.headline,
    bio: user.bio,
    country: user.country,
    show_on_leaderboard: user.show_on_leaderboard,
  });
  const [saved, setSaved] = useState(false);
  const { submit, busy, error } = useSubmit(async () => {
    setSaved(false);
    const body = { ...form, country: form.country.toUpperCase() };
    setUser(await api("/auth/me/", { method: "PATCH", body }));
    setSaved(true);
  });

  return (
    <section className="card" style={{ maxWidth: 560 }}>
      <h1>Your profile</h1>
      <p className="muted">{user.email}</p>
      {saved && <p className="notice notice-success">Profile saved.</p>}
      <FormError error={error} />
      <form onSubmit={submit}>
        <Field label="Full name" name="full_name" value={form.full_name} onChange={onChange} error={error} />
        <Field label="Headline" name="headline" placeholder="e.g. Aspiring Python developer"
          value={form.headline} onChange={onChange} error={error} />
        <Field label="Bio" name="bio" as="textarea" rows={4} value={form.bio} onChange={onChange} error={error} />
        <Field label="Country code" name="country" placeholder="e.g. BD" maxLength={2}
          value={form.country} onChange={onChange} error={error} />
        <label style={{ display: "block", marginBottom: 16 }}>
          <input type="checkbox" checked={form.show_on_leaderboard}
            onChange={(e) => onChange({ target: { name: "show_on_leaderboard", value: e.target.checked } })} />{" "}
          Show me on the public leaderboard
        </label>
        <button className="btn btn-primary" disabled={busy}>
          {busy ? "Saving…" : "Save profile"}
        </button>
      </form>
    </section>
  );
}
