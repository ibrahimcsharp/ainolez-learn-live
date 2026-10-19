import { useState } from "react";
import { useApi } from "../../../shared/hooks/useApi";
import styles from "./Analytics.module.css";

const METRICS = [
  ["page_views", "Page views"],
  ["signups", "New learners"],
  ["enrolments", "Enrolments"],
  ["lessons_completed", "Lessons completed"],
  ["courses_completed", "Courses completed"],
];
const PERIODS = [7, 30, 90];

export function AnalyticsPage() {
  const [days, setDays] = useState(30);
  const [metric, setMetric] = useState("page_views");
  const { data, error } = useApi(`/admin/platform/analytics/?days=${days}`);

  return (
    <>
      <div className={styles.head}>
        <h1>Analytics</h1>
        <div className={styles.periods} role="group" aria-label="Period">
          {PERIODS.map((n) => (
            <button
              key={n}
              type="button"
              className={n === days ? styles.periodActive : styles.period}
              aria-pressed={n === days}
              onClick={() => setDays(n)}
            >
              {n} days
            </button>
          ))}
        </div>
      </div>
      {error && <p className="notice notice-error">{error.message}</p>}
      {!data ? (
        !error && <p className="page-loading">Loading…</p>
      ) : (
        <>
          <div className={styles.totals}>
            {METRICS.map(([key, label]) => (
              <button
                key={key}
                type="button"
                className={`card ${key === metric ? styles.totalActive : styles.total}`}
                aria-pressed={key === metric}
                onClick={() => setMetric(key)}
              >
                <span className={styles.value}>{data.totals[key].toLocaleString()}</span>
                <span className="muted">{label}</span>
              </button>
            ))}
          </div>
          <section className="card">
            <h2 className={styles.chartTitle}>
              {METRICS.find(([key]) => key === metric)[1]} per day
            </h2>
            <DailyBars days={data.days} values={data.series[metric]} />
          </section>
          <div className={styles.tables}>
            <section className="card">
              <h2 className={styles.chartTitle}>Most viewed pages</h2>
              <Table
                columns={["Page", "Views"]}
                rows={data.top_pages.map((p) => [<a key="p" href={p.path}>{p.path}</a>, p.views])}
              />
            </section>
            <section className="card">
              <h2 className={styles.chartTitle}>Most joined courses</h2>
              <Table
                columns={["Course", "Enrolments", "Completed"]}
                rows={data.top_courses.map((c) => [c.title, c.enrolments, c.completions])}
              />
            </section>
          </div>
          <p className="muted">
            Page views count public pages, without cookies. Each figure covers the last {days} days.
          </p>
        </>
      )}
    </>
  );
}

/** One bar per day; hover a bar for its date and value. */
function DailyBars({ days, values }) {
  const max = Math.max(1, ...values);
  const width = 720;
  const height = 200;
  const step = width / values.length;
  const gap = values.length > 40 ? 1 : 3;
  return (
    <figure className={styles.chart}>
      <svg viewBox={`0 0 ${width} ${height + 24}`} role="img" aria-label="Values per day">
        <line x1="0" y1={height} x2={width} y2={height} className={styles.axis} />
        {values.map((value, i) => {
          const h = (value / max) * (height - 16);
          return (
            <rect
              key={days[i]}
              x={i * step + gap / 2}
              y={height - h}
              width={step - gap}
              height={Math.max(h, value ? 2 : 0)}
              rx="2"
              className={styles.bar}
            >
              <title>{`${days[i]}: ${value.toLocaleString()}`}</title>
            </rect>
          );
        })}
        <text x="0" y={height + 18} className={styles.label}>{days[0]}</text>
        <text x={width} y={height + 18} textAnchor="end" className={styles.label}>
          {days[days.length - 1]}
        </text>
        <text x="0" y="10" className={styles.label}>max {max.toLocaleString()}</text>
      </svg>
    </figure>
  );
}

function Table({ columns, rows }) {
  if (!rows.length) return <p className="muted">No data for this period yet.</p>;
  return (
    <table className={styles.table}>
      <thead>
        <tr>{columns.map((c) => <th key={c}>{c}</th>)}</tr>
      </thead>
      <tbody>
        {rows.map((row, i) => (
          <tr key={i}>{row.map((cell, j) => <td key={j}>{cell}</td>)}</tr>
        ))}
      </tbody>
    </table>
  );
}
