import { Link, Outlet, useNavigate } from "react-router";
import { ChatLauncher } from "../../features/assistant/ChatLauncher";
import { MenuDropdown } from "../../features/website/MenuDropdown";
import { MenuLink } from "../../features/website/MenuLink";
import { useMenus } from "../../features/website/menus";
import { Logo } from "../../shared/ui/Logo";
import { homeFor, useAuth } from "../AuthProvider";
import styles from "./Layouts.module.css";

export function PublicLayout() {
  // The header links and footer columns come from Admin -> Menus, ready on first paint.
  const menus = useMenus();
  return (
    <div className={styles.page}>
      <SiteHeader links={menus.header} />
      <main className={styles.main}>
        <Outlet />
      </main>
      <SiteFooter columns={menus.footer} />
      <ChatLauncher />
    </div>
  );
}

function SiteHeader({ links }) {
  const { user, logout } = useAuth();
  return (
    <header className={styles.header}>
      <div className={`container ${styles.headerInner}`}>
        <Link to="/" aria-label="ainolez home">
          <Logo variant="reversed" height={30} />
        </Link>
        <nav className={styles.headerNav}>
          {links.map((link, i) =>
            link.children ? (
              <MenuDropdown key={`${link.label}-${i}`} link={link} />
            ) : (
              <MenuLink key={`${link.url}-${i}`} link={link} />
            ),
          )}
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

function SiteFooter({ columns }) {
  return (
    <footer className={styles.footer}>
      <div className={`container ${styles.footerInner}`}>
        <div className={styles.footerBrand}>
          <Logo variant="reversed" height={26} />
          <p>Learn it. Code it. Own it.</p>
          <p className={styles.footerSmall}>Free coding and AI courses for everyone, forever.</p>
        </div>
        {columns.map((column) => (
          <nav key={column.id} aria-label={column.name} className={styles.footerCol}>
            <strong>{column.name}</strong>
            {column.items.map((link, i) =>
              link.children ? (
                <div key={`${link.label}-${i}`} className={styles.footerGroup}>
                  {link.url ? <MenuLink link={link} /> : <span>{link.label}</span>}
                  <div className={styles.footerSub}>
                    {link.children.map((child, j) => (
                      <MenuLink key={`${child.url}-${j}`} link={child} />
                    ))}
                  </div>
                </div>
              ) : (
                <MenuLink key={`${link.url}-${i}`} link={link} />
              ),
            )}
          </nav>
        ))}
      </div>
      <div className={`container ${styles.footerBottom}`}>© {new Date().getFullYear()} ainolez</div>
    </footer>
  );
}
