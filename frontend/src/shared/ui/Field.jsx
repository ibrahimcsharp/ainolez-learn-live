/** Labelled input. `error` is the ApiError from useSubmit; its message for this field is shown. */
export function Field({ label, name, error, as: Control = "input", ...inputProps }) {
  const message = error?.fields?.[name]?.[0];
  return (
    <div className="field">
      <label htmlFor={name}>{label}</label>
      <Control id={name} name={name} aria-invalid={Boolean(message)} {...inputProps} />
      {message && <span className="field-error">{message}</span>}
    </div>
  );
}

/** Shows the error message unless it is already shown next to a field. */
export function FormError({ error }) {
  if (!error) return null;
  const isFieldError = Object.keys(error.fields).some((key) => key !== "detail" && key !== "code");
  return isFieldError ? null : <p className="notice notice-error">{error.message}</p>;
}
