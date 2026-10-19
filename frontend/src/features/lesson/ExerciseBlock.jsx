import { useState } from "react";
import { Link } from "react-router";
import { api } from "../../shared/api/client";
import { TryIt } from "../playground/TryIt";
import styles from "./LessonContent.module.css";

/** A coding task. The code runs in the browser; the server checks the code or its output. */
export function ExerciseBlock({ exercise, learner }) {
  const [feedback, setFeedback] = useState(null);
  const [showHint, setShowHint] = useState(false);
  const solved = feedback?.is_correct || learner?.solvedIds.has(exercise.id);

  async function submit(code, result) {
    try {
      const body = { code, output: result?.output ?? "" };
      setFeedback(await api(`/learner/exercises/${exercise.id}/submit/`, { method: "POST", body }));
    } catch (error) {
      setFeedback({ is_correct: false, message: error.message });
    }
  }

  return (
    <section className={styles.exercise}>
      <h3>
        Exercise{exercise.title && `: ${exercise.title}`} {solved && <span className={styles.done}>✓ Solved</span>}
      </h3>
      <div dangerouslySetInnerHTML={{ __html: exercise.prompt_html }} />
      {exercise.check_type === "output" && (
        <p className="muted">Press Run first: your answer is checked by what the code prints.</p>
      )}
      <TryIt language={exercise.language} starterCode={exercise.starter_code}>
        {(code, result) =>
          learner?.loggedIn ? (
            <button className="btn btn-neon" onClick={() => submit(code, result)}>
              Check my answer
            </button>
          ) : (
            learner && <Link to="/login">Log in to check your answer and earn points</Link>
          )
        }
      </TryIt>
      {feedback && (
        <p className={`notice ${feedback.is_correct ? "notice-success" : "notice-error"}`}>{feedback.message}</p>
      )}
      {exercise.hint && (
        <p>
          <button className="btn btn-outline" onClick={() => setShowHint(!showHint)}>
            {showHint ? "Hide hint" : "Show hint"}
          </button>{" "}
          {showHint && <span>{exercise.hint}</span>}
        </p>
      )}
    </section>
  );
}
