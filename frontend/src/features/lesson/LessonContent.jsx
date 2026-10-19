import { TryIt } from "../playground/TryIt";
import { ExerciseBlock } from "./ExerciseBlock";
import styles from "./LessonContent.module.css";
import { QuizBlock } from "./QuizBlock";

const LANGUAGE_NAMES = { html: "HTML", css: "CSS", javascript: "JavaScript", python: "Python", sql: "SQL" };

/**
 * Draws a lesson's blocks. content_html is sanitised on the server before it is
 * stored, so it is safe to insert. Example, exercise and quiz blocks are drawn here.
 * `learner` is {loggedIn, solvedIds, quizResults, onProgress} on the public lesson
 * page, and absent in the admin preview.
 */
export function LessonContent({ blocks, learner }) {
  return (
    <div className="lesson-content">
      {blocks.map((block) => {
        if (block.type === "example") return block.example && <ExampleBox key={block.id} example={block.example} />;
        if (block.type === "exercise") {
          return block.exercise && <ExerciseBlock key={block.id} exercise={block.exercise} learner={learner} />;
        }
        if (block.type === "quiz") {
          return block.quiz ? (
            <QuizBlock key={block.id} quiz={block.quiz} learner={learner} />
          ) : (
            <p key={block.id} className="notice notice-info">Quiz #{block.quiz_id} appears here.</p>
          );
        }
        return <div key={block.id} dangerouslySetInnerHTML={{ __html: block.content_html }} />;
      })}
    </div>
  );
}

function ExampleBox({ example }) {
  return (
    <section className={styles.example}>
      <h3>{example.title || `${LANGUAGE_NAMES[example.language]} example`}</h3>
      <TryIt language={example.language} starterCode={example.starter_code} />
    </section>
  );
}
