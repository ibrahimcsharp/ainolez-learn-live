import { Link, Outlet, useNavigate } from "react-router";
import { ChatLauncher } from "../../features/assistant/ChatLauncher";
import { Logo } from "../../shared/ui/Logo";
import { homeFor, useAuth } from "../AuthProvider";
import styles from "./Layouts.module.css";

export function PublicLayout() {
  return (
    <div className={styles.page}>
      <SiteHeader />
      <main className={styles.main}>
        <Outlet />
      </main>
      <SiteFooter />
      <ChatLauncher />
    </div>
  );
}

function SiteHeader() {
  const { user, logout } = useAuth();
  return (
    <header className={styles.header}>
      <div className={`container ${styles.headerInner}`}>
        <Link to="/" aria-label="ainolez home">
          <Logo variant="reversed" height={30} />
        </Link>
        <nav className={styles.headerNav}>
          <Link to="/courses">Courses</Link>
          <Link to="/community">Community</Link>
          <Link to="/ai">AI tutor</Link>
          <Link to="/leaderboard">Leaderboard</Link>
          <SearchBox />
          {user ? (
            <>
              <Link to={homeFor(user)}>{user.role === "super_admin" ? "Admin panel" : "My dashboard"}</Link>
              <button className="btn btn-outline" onClick={logout}>
                Log out
              </button>
            </>
          ) : (
            <>
              <Link to="/login">Log in</Link>
              <Link to="/register" className="btn btn-neon">
                Sign up free
              </Link>
            </>
          )}
        </nav>
      </div>
    </header>
  );
}

function SearchBox() {
  const navigate = useNavigate();
  function search(event) {
    event.preventDefault();
    const q = new FormData(event.currentTarget).get("q").trim();
    if (q) navigate(`/search?q=${encodeURIComponent(q)}`);
  }
  return (
    <form role="search" onSubmit={search}>
      <input name="q" type="search" placeholder="Search lessons" aria-label="Search lessons"
        className={styles.search} />
    </form>
  );
}

const FOOTER_LINKS = [
  ["Learn", [["/courses", "All courses"], ["/python", "Python"], ["/html", "HTML"], ["/intro-to-ai", "AI"]]],
  ["Community", [["/community", "Forum"], ["/leaderboard", "Leaderboard"], ["/ai", "AI tutor"]]],
  ["Account", [["/register", "Sign up free"], ["/login", "Log in"], ["/dashboard", "My dashboard"]]],
];

function SiteFooter() {
  return (
    <footer className={styles.footer}>
      <div className={`container ${styles.footerInner}`}>
        <div className={styles.footerBrand}>
          <Logo variant="reversed" height={26} />
          <p>Learn it. Code it. Own it.</p>
          <p className={styles.footerSmall}>Free coding and AI courses for everyone, forever.</p>
        </div>
        {FOOTER_LINKS.map(([title, links]) => (
          <nav key={title} aria-label={title} className={styles.footerCol}>
            <strong>{title}</strong>
            {links.map(([to, label]) => (
              <Link key={to} to={to}>{label}</Link>
            ))}
          </nav>
        ))}
      </div>
      <div className={`container ${styles.footerBottom}`}>© {new Date().getFullYear()} ainolez</div>
    </footer>
  );
}
