import { Save, X } from "lucide-react";
import { api } from "../../../shared/api/client";
import { useFormFields, useSubmit } from "../../../shared/hooks/useForm";
import { FormError } from "../../../shared/ui/Field";
import styles from "./admin.module.css";

/**
 * Form state for creating (no initial.id) or editing one admin record.
 * `toBody(values)` can reshape the values before they are sent.
 */
export function useResourceForm(base, initial, onSaved, toBody = (values) => values) {
  const [values, onChange, setValues] = useFormFields(initial);
  const { submit, busy, error } = useSubmit(async () => {
    const saved = await api(initial.id ? `${base}/${initial.id}/` : `${base}/`, {
      method: initial.id ? "PATCH" : "POST",
      body: toBody(values),
    });
    onSaved(saved);
  });
  return { values, onChange, setValues, submit, busy, error };
}

export function EditPanel({ title, form, onCancel, children }) {
  return (
    <form className={`card ${styles.panel}`} onSubmit={form.submit}>
      {title && <h3>{title}</h3>}
      <FormError error={form.error} />
      <div className={styles.formGrid}>{children}</div>
      <div className={styles.actions} style={{ justifyContent: "flex-start" }}>
        <button className="btn btn-primary" disabled={form.busy}>
          <Save /> {form.busy ? "Saving…" : "Save"}
        </button>
        {onCancel && (
          <button type="button" className="btn btn-outline" onClick={onCancel}>
            <X /> Cancel
          </button>
        )}
      </div>
    </form>
  );
}
