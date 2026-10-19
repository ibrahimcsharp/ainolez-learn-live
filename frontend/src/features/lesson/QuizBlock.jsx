import { useState } from "react";
import { Link } from "react-router";
import { api } from "../../shared/api/client";
import styles from "./LessonContent.module.css";

/** A quiz inside a lesson. The server grades it and returns the right answers afterwards. */
export function QuizBlock({ quiz, learner }) {
  const [answers, setAnswers] = useState({}); // {question_id: [option ids]}
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const best = learner?.quizResults?.[quiz.id];

  function choose(question, optionId, checked) {
    const current = answers[question.id] ?? [];
    const next =
      question.type === "multiple"
        ? checked ? [...current, optionId] : current.filter((id) => id !== optionId)
        : [optionId];
    setAnswers({ ...answers, [question.id]: next });
  }

  async function submit(event) {
    event.preventDefault();
    setError(null);
    try {
      const data = await api(`/learner/quizzes/${quiz.id}/attempts/`, { method: "POST", body: { answers } });
      setResult(data);
      learner.onProgress(data);
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <form className={styles.quiz} onSubmit={submit}>
      <h3>
        {quiz.is_final ? "Final quiz: " : "Quiz: "}
        {quiz.title}
      </h3>
      <p className="muted">
        Pass mark {quiz.pass_percentage}%.
        {best && ` Your best: ${Math.round(best.percentage)}%${best.passed ? " ✓ passed" : ""}.`}
      </p>
      {quiz.questions.map((question, index) => {
        const feedback = result?.questions[question.id];
        return (
          <fieldset key={question.id} className={styles.question} disabled={Boolean(result)}>
            <legend>
              {index + 1}. {question.text}
              {question.type === "multiple" && <span className="muted"> (choose all that apply)</span>}
            </legend>
            {question.code_snippet && <pre>{question.code_snippet}</pre>}
            {question.options.map((option) => {
              const right = feedback?.correct_option_ids.includes(option.id);
              const chosen = (answers[question.id] ?? []).includes(option.id);
              return (
                <label key={option.id} className={result ? (right ? styles.right : chosen ? styles.wrong : "") : ""}>
                  <input
                    type={question.type === "multiple" ? "checkbox" : "radio"}
                    name={`q${question.id}`}
                    checked={chosen}
                    onChange={(e) => choose(question, option.id, e.target.checked)}
                  />{" "}
                  {option.text}
                </label>
              );
            })}
            {feedback?.explanation && <p className="muted">{feedback.explanation}</p>}
          </fieldset>
        );
      })}
      {error && <p className="notice notice-error">{error}</p>}
      {result ? (
        <div className={`notice ${result.passed ? "notice-success" : "notice-error"}`}>
          You scored {Math.round(result.percentage)}% — {result.passed ? "passed! 🎉" : "not passed yet."}{" "}
          <button type="button" className="btn btn-outline" onClick={() => { setResult(null); setAnswers({}); }}>
            Try again
          </button>
        </div>
      ) : learner?.loggedIn ? (
        <button className="btn btn-primary">Submit answers</button>
      ) : (
        learner && <Link to="/login">Log in to take the quiz</Link>
      )}
    </form>
  );
}
