import {
  ArrowRight,
  Award,
  BookOpen,
  Bot,
  Braces,
  Brain,
  Check,
  Code,
  Database,
  FileCode2,
  Gift,
  Palette,
  Play,
  Terminal,
  Trophy,
} from "lucide-react";
import { Link } from "react-router";
import { useAuth, homeFor } from "../../app/AuthProvider";
import { useApi } from "../../shared/hooks/useApi";
import { CourseCard } from "../catalog/CatalogPage";
import styles from "./HomePage.module.css";

const TOPICS = [
  ["html", "HTML", "Structure every web page.", FileCode2, "#e34c26"],
  ["css", "CSS", "Style and lay out pages.", Palette, "#2965f1"],
  ["javascript", "JavaScript", "Make pages interactive.", Braces, "#d4a500"],
  ["python", "Python", "The friendliest first language.", Terminal, "#3776ab"],
  ["sql", "SQL", "Ask questions of data.", Database, "#00758f"],
  ["intro-to-ai", "AI", "How machines learn.", Brain, "#7c3aed"],
];
const STEPS = [
  [BookOpen, "Read", "Short, clear lessons with examples you can change."],
  [Code, "Code", "Run every example and exercise right in the page."],
  [Award, "Certify", "Finish the course and share a free, verifiable certificate."],
];
const FEATURES = [
  [Gift, "Free, forever", "Every course, quiz and certificate costs nothing. No trials, no paywalls."],
  [Play, "Code in your browser", "HTML, JavaScript, Python and SQL run inside each lesson. Nothing to install."],
  [Bot, "An AI tutor beside you", "Stuck? Ask about any lesson or your own code and get a clear answer."],
  [Trophy, "Stay motivated", "Points, streaks, badges and a leaderboard keep you coming back."],
];

export function HomePage() {
  const { user } = useAuth();
  const courses = useApi("/public/courses/");
  const count = courses.data?.length;

  return (
    <>
      <section className={styles.hero}>
        <div className={`container ${styles.heroInner}`}>
          <div>
            <span className={styles.eyebrow}>100% free · No credit card</span>
            <h1 className={styles.slogan}>
              Learn it. Code it. <span>Own it.</span>
            </h1>
            <p className={styles.lead}>
              Coding and AI courses with a live code editor and an AI tutor, free for everyone.
            </p>
            <div className={styles.actions}>
              {user ? (
                <Link to={homeFor(user)} className="btn btn-neon">
                  Continue learning <ArrowRight />
                </Link>
              ) : (
                <Link to="/register" className="btn btn-neon">
                  Start learning free <ArrowRight />
                </Link>
              )}
              <Link to="/courses" className="btn btn-outline">
                Browse courses
              </Link>
            </div>
            <ul className={styles.checks}>
              {["Free certificates", "Runs in your browser", "AI tutor included"].map((text) => (
                <li key={text}>
                  <Check /> {text}
                </li>
              ))}
            </ul>
          </div>
          <CodeWindow />
        </div>
      </section>

      <section className={styles.stats} aria-label="ainolez in numbers">
        <div className={`container ${styles.statsInner}`}>
          <Stat value={count ? `${count}+` : "10+"} label="Free courses" />
          <Stat value="6" label="Topics, from HTML to AI" />
          <Stat value="5" label="Languages you can run" />
          <Stat value="$0" label="Forever" />
        </div>
      </section>

      <section className={`container ${styles.section}`}>
        <SectionHead title="Pick a topic" text="Start anywhere. Every course begins from zero." />
        <div className={styles.topics}>
          {TOPICS.map(([slug, name, text, Icon, color]) => (
            <Link key={slug} to={`/${slug}`} className={styles.topic} style={{ "--accent": color }}>
              <span className={styles.topicIcon}>
                <Icon size={22} />
              </span>
              <span>
                <strong>{name}</strong>
                <span className="muted">{text}</span>
              </span>
              <ArrowRight className={styles.topicArrow} size={18} />
            </Link>
          ))}
        </div>
      </section>

      <section className={styles.band}>
        <div className={`container ${styles.section}`}>
          <SectionHead title="How it works" text="Three steps from your first line of code to a certificate." />
          <ol className={styles.steps}>
            {STEPS.map(([Icon, title, text], i) => (
              <li key={title}>
                <span className={styles.stepIcon}>
                  <Icon size={22} />
                </span>
                <span className={styles.stepNumber}>Step {i + 1}</span>
                <h3>{title}</h3>
                <p className="muted">{text}</p>
              </li>
            ))}
          </ol>
        </div>
      </section>

      {count > 0 && (
        <section className={`container ${styles.section}`}>
          <SectionHead
            title="Popular courses"
            text="Hand-written lessons, exercises and quizzes."
            link={<Link to="/courses">See all courses <ArrowRight size={16} /></Link>}
          />
          <div className={styles.courses}>
            {courses.data.slice(0, 6).map((course) => (
              <CourseCard key={course.slug} course={course} />
            ))}
          </div>
        </section>
      )}

      <section className={`container ${styles.section}`}>
        <SectionHead title="Everything you need to learn" />
        <div className={styles.features}>
          {FEATURES.map(([Icon, title, text]) => (
            <article key={title} className={styles.feature}>
              <span className={styles.featureIcon}>
                <Icon size={22} />
              </span>
              <h3>{title}</h3>
              <p className="muted">{text}</p>
            </article>
          ))}
        </div>
      </section>

      <section className={`container ${styles.section}`}>
        <div className={styles.cta}>
          <div>
            <h2>Write your first line of code today</h2>
            <p>Join free. Learn at your own pace, on any device.</p>
          </div>
          <Link to={user ? homeFor(user) : "/register"} className="btn btn-neon">
            {user ? "Go to my dashboard" : "Create a free account"} <ArrowRight />
          </Link>
        </div>
      </section>
    </>
  );
}

function SectionHead({ title, text, link }) {
  return (
    <div className={styles.sectionHead}>
      <div>
        <h2>{title}</h2>
        {text && <p className="muted">{text}</p>}
      </div>
      {link}
    </div>
  );
}

function Stat({ value, label }) {
  return (
    <div className={styles.stat}>
      <strong>{value}</strong>
      <span>{label}</span>
    </div>
  );
}

/** A static picture of the Try-it editor. */
function CodeWindow() {
  return (
    <figure className={styles.window} aria-label="Example of the Try-it editor">
      <div className={styles.windowBar}>
        <span />
        <span />
        <span />
        <em>hello.py</em>
        <b>
          <Play size={12} /> Run
        </b>
      </div>
      <pre className={styles.code}>
        <code>
          <i>names</i> = [<s>"Ada"</s>, <s>"Linus"</s>, <s>"Grace"</s>]{"\n"}
          <u>for</u> name <u>in</u> names:{"\n"}
          {"    "}<i>print</i>(<s>f"Hello, </s>{"{name}"}<s>!"</s>)
        </code>
      </pre>
      <div className={styles.output}>
        <span>Output</span>
        Hello, Ada!{"\n"}Hello, Linus!{"\n"}Hello, Grace!
      </div>
    </figure>
  );
}
