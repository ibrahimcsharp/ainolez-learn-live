import styles from "./Logo.module.css";

/*
 * The ainolez wordmark (PLANNING.md §1.1):
 * the dot of the "i" is a neon code cursor, the "o" is a nearly closed progress ring.
 * Same drawing as public/brand/logo-*.svg.
 */
const VARIANTS = {
  full: { text: "#05192D", ring: "#04AA6D", cursor: "#03EF62" },
  reversed: { text: "#FFFFFF", ring: "#03EF62", cursor: "#03EF62" },
  mono: { text: "#05192D", ring: "#05192D", cursor: "#05192D" },
};
const LETTERS = [
  ["a", 19],
  ["ı", 49], // dotless i: the cursor is its dot
  ["n", 79],
  ["l", 152],
  ["e", 181.5],
  ["z", 218.5],
];

export function Logo({ variant = "full", height = 32 }) {
  const color = VARIANTS[variant];
  return (
    <svg
      className={styles.logo}
      viewBox="0 0 238 84"
      height={height}
      role="img"
      aria-label="ainolez"
    >
      <g fill={color.text} fontFamily="Poppins, 'Segoe UI', Arial, sans-serif" fontWeight="600" fontSize="64" textAnchor="middle">
        {LETTERS.map(([letter, x]) => (
          <text key={x} x={x} y="66">
            {letter}
          </text>
        ))}
      </g>
      <circle
        cx="121"
        cy="48.5"
        r="15.5"
        fill="none"
        stroke={color.ring}
        strokeWidth="8"
        strokeLinecap="round"
        strokeDasharray="84 13.4"
        transform="rotate(-30 121 48.5)"
      />
      <rect className={styles.cursor} x="43.5" y="10" width="11" height="11" rx="1.5" fill={color.cursor} />
    </svg>
  );
}
