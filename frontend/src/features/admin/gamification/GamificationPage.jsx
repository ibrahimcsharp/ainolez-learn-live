import { useState } from "react";
import { useApi } from "../../../shared/hooks/useApi";
import { Field } from "../../../shared/ui/Field";
import { EditPanel, useResourceForm } from "../shared/EditPanel";
import { RecordActions, StatusBadge } from "../shared/RecordActions";
import styles from "../shared/admin.module.css";

const RULES = "/admin/gamification/points-rules";
const BADGES = "/admin/gamification/badges";
const RULE_TYPES = { points: "Total points", lessons: "Lessons finished", courses: "Courses finished", streak: "Longest streak (days)" };
const NEW_BADGE = { name: "", description: "", icon: "🏅", rule: { type: "lessons", threshold: 10 } };

/** Points rules and badges, the levers of the reward system. */
export function GamificationPage() {
  const rules = useApi(`${RULES}/?page_size=500`);
  const badges = useApi(`${BADGES}/?page_size=500`);
  const [editingRule, setEditingRule] = useState(null);
  const [editingBadge, setEditingBadge] = useState(null);

  return (
    <>
      <h1>Points and badges</h1>
      <h2>Points rules</h2>
      <p className="muted">Points are given once per lesson, exercise, quiz or course, and never taken back.</p>
      {editingRule && (
        <RuleForm key={editingRule.id} initial={editingRule}
          onSaved={() => { setEditingRule(null); rules.reload(); }} onCancel={() => setEditingRule(null)} />
      )}
      <table className={styles.table}>
        <thead>
          <tr><th>Event</th><th>Points</th><th>Daily cap</th><th /></tr>
        </thead>
        <tbody>
          {(rules.data?.results ?? []).map((rule) => (
            <tr key={rule.id}>
              <td>
                {rule.description} <code className="muted">{rule.event_key}</code> <StatusBadge row={rule} />
              </td>
              <td><strong>+{rule.points}</strong></td>
              <td>{rule.daily_cap ?? "—"}</td>
              <td><RecordActions base={RULES} row={rule} onChange={rules.reload} onEdit={setEditingRule} /></td>
            </tr>
          ))}
        </tbody>
      </table>

      <div className={styles.toolbar} style={{ marginTop: 32 }}>
        <h2>Badges</h2>
        <button className="btn btn-primary" onClick={() => setEditingBadge(NEW_BADGE)}>New badge</button>
      </div>
      {editingBadge && (
        <BadgeForm key={editingBadge.id ?? "new"} initial={editingBadge}
          onSaved={() => { setEditingBadge(null); badges.reload(); }} onCancel={() => setEditingBadge(null)} />
      )}
      <table className={styles.table}>
        <tbody>
          {(badges.data?.results ?? []).map((badge) => (
            <tr key={badge.id}>
              <td style={{ fontSize: 28, width: 48 }}>{badge.icon}</td>
              <td>
                <strong>{badge.name}</strong> <StatusBadge row={badge} />
                <div className="muted">
                  {RULE_TYPES[badge.rule.type]} ≥ {badge.rule.threshold} · {badge.description}
                </div>
              </td>
              <td><RecordActions base={BADGES} row={badge} onChange={badges.reload} onEdit={setEditingBadge} /></td>
            </tr>
          ))}
        </tbody>
      </table>
    </>
  );
}

function RuleForm({ initial, onSaved, onCancel }) {
  const toBody = (v) => ({ points: v.points, daily_cap: v.daily_cap || null, description: v.description });
  const form = useResourceForm(RULES, initial, onSaved, toBody);
  const { values, onChange, error } = form;
  return (
    <EditPanel title={`Edit “${initial.event_key}”`} form={form} onCancel={onCancel}>
      <Field label="Points" name="points" type="number" value={values.points} onChange={onChange} error={error} />
      <Field label="Daily cap (blank = none)" name="daily_cap" type="number" min="0"
        value={values.daily_cap ?? ""} onChange={onChange} error={error} />
      <Field label="Description" name="description" value={values.description} onChange={onChange} error={error} />
    </EditPanel>
  );
}

function BadgeForm({ initial, onSaved, onCancel }) {
  const flat = { ...initial, rule_type: initial.rule.type, threshold: initial.rule.threshold };
  const toBody = ({ rule_type, threshold, ...v }) => ({
    name: v.name, slug: v.slug, description: v.description, icon: v.icon,
    rule: { type: rule_type, threshold: Number(threshold) },
  });
  const form = useResourceForm(BADGES, flat, onSaved, toBody);
  const { values, onChange, error } = form;
  return (
    <EditPanel title={initial.id ? "Edit badge" : "New badge"} form={form} onCancel={onCancel}>
      <Field label="Name" name="name" required value={values.name} onChange={onChange} error={error} />
      <Field label="Icon (emoji)" name="icon" value={values.icon} onChange={onChange} error={error} />
      <Field label="Earned when" name="rule_type" as="select" value={values.rule_type} onChange={onChange}>
        {Object.entries(RULE_TYPES).map(([key, label]) => <option key={key} value={key}>{label}</option>)}
      </Field>
      <Field label="reaches at least" name="threshold" type="number" min="1" value={values.threshold}
        onChange={onChange} error={error} />
      <Field label="Description" name="description" value={values.description} onChange={onChange} error={error} />
    </EditPanel>
  );
}
