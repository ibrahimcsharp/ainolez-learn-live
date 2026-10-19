import { useState } from "react";
import { Link, useParams } from "react-router";
import { useApi } from "../../../shared/hooks/useApi";
import { Field } from "../../../shared/ui/Field";
import { EditPanel, useResourceForm } from "../shared/EditPanel";
import { RecordActions, StatusBadge } from "../shared/RecordActions";
import { SortableList } from "../shared/SortableList";
import styles from "../shared/admin.module.css";

export const QUIZZES = "/admin/assessment/quizzes";
const QUESTIONS = "/admin/assessment/questions";
const NEW_QUESTION = {
  question_text: "",
  question_type: "single",
  code_snippet: "",
  explanation: "",
  points: 1,
  options: [
    { option_text: "", is_correct: true },
    { option_text: "", is_correct: false },
  ],
};

export function QuizEditPage() {
  const { id } = useParams();
  const quiz = useApi(`${QUIZZES}/${id}/`);
  const questions = useApi(`${QUESTIONS}/?quiz=${id}&page_size=500`);
  const [editing, setEditing] = useState(null);
  if (!quiz.data) return <p className="page-loading">{quiz.error?.message ?? "Loading…"}</p>;

  function saved() {
    setEditing(null);
    questions.reload();
  }

  return (
    <>
      <p>
        <Link to={`/admin/courses/${quiz.data.course_id}`}>← Back to the course</Link>
      </p>
      <h1>{quiz.data.title}</h1>
      <QuizForm key={quiz.data.updated_at} initial={quiz.data} onSaved={quiz.reload} />
      <div className={styles.toolbar}>
        <h2>Questions</h2>
        <button className="btn btn-primary" onClick={() => setEditing({ ...NEW_QUESTION, quiz: Number(id) })}>
          New question
        </button>
      </div>
      {editing && (
        <QuestionForm key={editing.id ?? "new"} initial={editing} onSaved={saved} onCancel={() => setEditing(null)} />
      )}
      <SortableList
        items={questions.data?.results ?? []}
        base={QUESTIONS}
        onChange={questions.reload}
        renderItem={(question) => (
          <div className={styles.toolbar} style={{ margin: 0 }}>
            <span className={styles.grow}>
              <strong>{question.question_text}</strong> <StatusBadge row={question} />
              <div className="muted">
                {question.options.map((o) => `${o.is_correct ? "✓" : "·"} ${o.option_text}`).join("   ")}
              </div>
            </span>
            <RecordActions base={QUESTIONS} row={question} onChange={questions.reload} onEdit={setEditing} />
          </div>
        )}
      />
    </>
  );
}

export function QuizForm({ initial, onSaved, onCancel }) {
  const toBody = (v) => ({ ...v, max_attempts: v.max_attempts || null });
  const form = useResourceForm(QUIZZES, initial, onSaved, toBody);
  const { values, onChange, setValues, error } = form;
  return (
    <EditPanel title={initial.id ? "Quiz settings" : "New quiz"} form={form} onCancel={onCancel}>
      <Field label="Title" name="title" required value={values.title} onChange={onChange} error={error} />
      <Field label="Pass mark (%)" name="pass_percentage" type="number" min="1" max="100"
        value={values.pass_percentage} onChange={onChange} error={error} />
      <Field label="Max attempts (blank = unlimited)" name="max_attempts" type="number" min="1"
        value={values.max_attempts ?? ""} onChange={onChange} error={error} />
      <Field label="Description" name="description" value={values.description} onChange={onChange} error={error} />
      <label style={{ alignSelf: "center" }}>
        <input type="checkbox" checked={values.is_final}
          onChange={(e) => setValues({ ...values, is_final: e.target.checked })} />{" "}
        Final quiz (must be passed to finish the course)
      </label>
    </EditPanel>
  );
}

function QuestionForm({ initial, onSaved, onCancel }) {
  const form = useResourceForm(QUESTIONS, initial, onSaved);
  const { values, onChange, setValues, error } = form;
  const options = values.options;
  const multiple = values.question_type === "multiple";

  function setOption(index, change) {
    let next = options.map((o, i) => (i === index ? { ...o, ...change } : o));
    if (change.is_correct && !multiple) next = next.map((o, i) => ({ ...o, is_correct: i === index }));
    setValues({ ...values, options: next });
  }

  return (
    <EditPanel title={initial.id ? "Edit question" : "New question"} form={form} onCancel={onCancel}>
      <div style={{ gridColumn: "1 / -1" }}>
        <Field label="Question" name="question_text" as="textarea" rows={2} required
          value={values.question_text} onChange={onChange} error={error} />
      </div>
      <Field label="Type" name="question_type" as="select" value={values.question_type} onChange={onChange}>
        <option value="single">One correct answer</option>
        <option value="multiple">Several correct answers</option>
        <option value="true_false">True / false</option>
      </Field>
      <Field label="Points" name="points" type="number" min="1" value={values.points} onChange={onChange} />
      <Field label="Code shown with the question (optional)" name="code_snippet" as="textarea" rows={3}
        className={styles.code} value={values.code_snippet ?? ""} onChange={onChange} />
      <Field label="Explanation (shown after answering)" name="explanation" value={values.explanation}
        onChange={onChange} />
      <fieldset style={{ gridColumn: "1 / -1" }}>
        <legend>Answers (tick the correct one{multiple && "s"})</legend>
        {options.map((option, index) => (
          <div key={index} className={styles.actions} style={{ justifyContent: "flex-start", marginBottom: 6 }}>
            <input type={multiple ? "checkbox" : "radio"} name="correct" checked={option.is_correct}
              aria-label="Correct answer" onChange={(e) => setOption(index, { is_correct: e.target.checked })} />
            <input value={option.option_text} placeholder={`Answer ${index + 1}`} style={{ flex: 1 }}
              onChange={(e) => setOption(index, { option_text: e.target.value })} />
            {options.length > 2 && (
              <button type="button" className={`btn btn-outline ${styles.small}`}
                onClick={() => setValues({ ...values, options: options.filter((_, i) => i !== index) })}>
                Remove
              </button>
            )}
          </div>
        ))}
        <button type="button" className={`btn btn-outline ${styles.small}`}
          onClick={() => setValues({ ...values, options: [...options, { option_text: "", is_correct: false }] })}>
          + Add answer
        </button>
      </fieldset>
    </EditPanel>
  );
}
