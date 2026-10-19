import { useState } from "react";

/** Form values plus one onChange handler for every input (matched by `name`). */
export function useFormFields(initial) {
  const [values, setValues] = useState(initial);
  const onChange = (event) => setValues({ ...values, [event.target.name]: event.target.value });
  return [values, onChange, setValues];
}

/** Wraps an async submit: tracks busy state and the last ApiError. */
export function useSubmit(action) {
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState(null);

  async function submit(event) {
    event?.preventDefault();
    setBusy(true);
    setError(null);
    try {
      await action();
    } catch (err) {
      setError(err);
    } finally {
      setBusy(false);
    }
  }

  return { submit, busy, error };
}
