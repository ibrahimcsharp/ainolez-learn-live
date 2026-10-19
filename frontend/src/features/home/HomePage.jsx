import { Link } from "react-router";
import styles from "./HomePage.module.css";

const TOPICS = ["HTML", "CSS", "JavaScript", "Python", "SQL", "AI"];
const PROMISES = [
  ["Free, forever", "Every course, quiz and certificate costs nothing."],
  ["Code in your browser", "Run HTML, JavaScript, Python and SQL right inside each lesson."],
  ["An AI tutor beside you", "Ask about any lesson and get a clear answer straight away."],
];

export function HomePage() {
  return (
    <>
      <section className={styles.hero}>
        <div className="container">
          <h1 className={styles.slogan}>
            Learn it. Code it. <span>Own it.</span>
          </h1>
          <p className={styles.lead}>
            Free coding and AI courses, a live code editor, and an AI tutor, for everyone.
          </p>
          <div className={styles.actions}>
            <Link to="/register" className="btn btn-neon">
              Start learning, it's free
            </Link>
            <Link to="/login" className="btn btn-outline">
              Log in
            </Link>
          </div>
          <ul className={styles.topics} aria-label="Topics">
            {TOPICS.map((topic) => (
              <li key={topic}>
                <Link to="/courses">{topic}</Link>
              </li>
            ))}
          </ul>
        </div>
      </section>

      <section className={`container ${styles.promises}`}>
        {PROMISES.map(([title, text]) => (
          <article key={title} className="card">
            <h3>{title}</h3>
            <p className="muted">{text}</p>
          </article>
        ))}
      </section>
    </>
  );
}
