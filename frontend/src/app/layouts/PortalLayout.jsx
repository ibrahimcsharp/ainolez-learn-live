import { Link, NavLink, Outlet } from "react-router";
import { ChatLauncher } from "../../features/assistant/ChatLauncher";
import { Logo } from "../../shared/ui/Logo";
import { useAuth } from "../AuthProvider";
import styles from "./Layouts.module.css";

const MENUS = {
  learner: [
    { to: "/dashboard", label: "Dashboard", end: true },
    { to: "/dashboard/profile", label: "Profile" },
  ],
  admin: [
    { to: "/admin", label: "Dashboard", end: true },
    { to: "/admin/analytics", label: "Analytics" },
    { to: "/admin/categories", label: "Categories" },
    { to: "/admin/courses", label: "Courses" },
    { to: "/admin/paths", label: "Learning paths" },
    { to: "/admin/certificates", label: "Certificates" },
    { to: "/admin/gamification", label: "Points and badges" },
    { to: "/admin/moderation", label: "Community" },
    { to: "/admin/ai", label: "AI tutor" },
    { to: "/admin/course-generator", label: "AI course generator" },
    { to: "/admin/seo", label: "SEO" },
    { to: "/admin/media", label: "Media" },
    { to: "/admin/markdown", label: "Markdown converter" },
    { to: "/admin/trash", label: "Trash" },
  ],
};

/** Sidebar layout shared by the learner portal and the admin panel. */
export function PortalLayout({ area }) {
  const { user, logout } = useAuth();
  return (
    <div className={styles.portal}>
      <aside className={area === "admin" ? styles.sidebarAdmin : styles.sidebar}>
        <Link to="/" aria-label="ainolez home" className={styles.sidebarLogo}>
          <Logo variant={area === "admin" ? "reversed" : "full"} height={26} />
        </Link>
        {area === "admin" && <span className={styles.badge}>Super Admin</span>}
        <nav className={styles.sideNav}>
          {MENUS[area].map((item) => (
            <NavLink key={item.to} to={item.to} end={item.end}>
              {item.label}
            </NavLink>
          ))}
        </nav>
      </aside>
      <div className={styles.portalBody}>
        <header className={styles.topbar}>
          <span>{user.full_name || user.username}</span>
          <button className="btn btn-outline" onClick={logout}>
            Log out
          </button>
        </header>
        <main className={styles.portalMain}>
          <Outlet />
        </main>
      </div>
      {area === "learner" && <ChatLauncher />}
    </div>
  );
}
