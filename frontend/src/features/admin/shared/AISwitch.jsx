import { api } from "../../../shared/api/client";
import { useApi } from "../../../shared/hooks/useApi";
import { useSubmit } from "../../../shared/hooks/useForm";
import { FormError } from "../../../shared/ui/Field";
import styles from "./admin.module.css";

const SETTINGS = "/admin/assistant/settings/";

/** An on/off card for one switch of the AI settings, saved as soon as it is flipped. */
export function AISwitch({ name, icon: Icon, title, on: onText, off: offText }) {
  const { data, reload } = useApi(SETTINGS);
  const flip = useSubmit(async () => {
    await api(SETTINGS, { method: "PATCH", body: { [name]: !data[name] } });
    reload();
  });
  if (!data) return null;
  const on = data[name];

  return (
    <section className={`card ${styles.switchCard}`} data-on={on}>
      <span className={styles.switchIcon}>
        <Icon size={22} />
      </span>
      <div className={styles.grow}>
        <strong>
          {title} is {on ? "on" : "off"}
        </strong>
        <p className="muted">{on ? onText : offText}</p>
        <FormError error={flip.error} />
      </div>
      <button type="button" role="switch" aria-checked={on} aria-label={title} className={styles.switch}
        disabled={flip.busy} onClick={flip.submit} />
    </section>
  );
}
