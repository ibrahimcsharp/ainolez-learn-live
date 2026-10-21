import {
  Award,
  BookOpen,
  Bot,
  ChartColumn,
  ExternalLink,
  FileCode,
  FileText,
  FolderTree,
  Globe,
  Image,
  LayoutDashboard,
  LogOut,
  Menu,
  MessagesSquare,
  Route,
  Sparkles,
  Trash2,
  Trophy,
  UserCircle,
} from "lucide-react";
import { Link, NavLink, Outlet } from "react-router";
import { ChatLauncher } from "../../features/assistant/ChatLauncher";
import { Logo } from "../../shared/ui/Logo";
import { useAuth } from "../AuthProvider";
import styles from "./Layouts.module.css";

const MENUS = {
  learner: [
    {
      items: [
        { to: "/dashboard", label: "Dashboard", icon: LayoutDashboard, end: true },
        { to: "/dashboard/profile", label: "Profile", icon: UserCircle },
      ],
    },
  ],
  admin: [
    {
      title: "Overview",
      items: [
        { to: "/admin", label: "Dashboard", icon: LayoutDashboard, end: true },
        { to: "/admin/analytics", label: "Analytics", icon: ChartColumn },
      ],
    },
    {
      title: "Content",
      items: [
        { to: "/admin/categories", label: "Categories", icon: FolderTree },
        { to: "/admin/courses", label: "Courses", icon: BookOpen },
        { to: "/admin/paths", label: "Learning paths", icon: Route },
        { to: "/admin/media", label: "Media", icon: Image },
        { to: "/admin/markdown", label: "Markdown converter", icon: FileCode },
      ],
    },
    {
      title: "Learners",
      items: [
        { to: "/admin/certificates", label: "Certificates", icon: Award },
        { to: "/admin/gamification", label: "Points and badges", icon: Trophy },
        { to: "/admin/moderation", label: "Community", icon: MessagesSquare },
      ],
    },
    {
      title: "AI",
      items: [
        { to: "/admin/ai", label: "AI tutor", icon: Bot },
        { to: "/admin/course-generator", label: "AI course generator", icon: Sparkles },
      ],
    },
    {
      title: "Site",
      items: [
        { to: "/admin/pages", label: "Pages", icon: FileText },
        { to: "/admin/menus", label: "Menus", icon: Menu },
        { to: "/admin/seo", label: "SEO", icon: Globe },
        { to: "/admin/trash", label: "Trash", icon: Trash2 },
      ],
    },
  ],
};

/** Sidebar layout shared by the learner portal and the admin panel. */
export function PortalLayout({ area }) {
  const { user, logout } = useAuth();
  const name = user.full_name || user.username;
  return (
    <div className={`${styles.portal} ${area === "admin" ? styles.admin : ""}`}>
      <aside className={area === "admin" ? styles.sidebarAdmin : styles.sidebar}>
        <Link to="/" aria-label="ainolez home" className={styles.sidebarLogo}>
          <Logo variant={area === "admin" ? "reversed" : "full"} height={26} />
        </Link>
        {area === "admin" && <span className={styles.badge}>Super Admin</span>}
        <nav className={styles.sideNav}>
          {MENUS[area].map((group, i) => (
            <div key={group.title ?? i} className={styles.navGroup}>
              {group.title && <span className={styles.navTitle}>{group.title}</span>}
              {group.items.map(({ to, label, icon: Icon, end }) => (
                <NavLink key={to} to={to} end={end}>
                  <Icon size={18} strokeWidth={1.8} />
                  {label}
                </NavLink>
              ))}
            </div>
          ))}
        </nav>
      </aside>
      <div className={styles.portalBody}>
        <header className={styles.topbar}>
          <Link to="/" className={styles.topbarLink}>
            <ExternalLink size={16} /> View site
          </Link>
          <span className={styles.user}>
            <span className={styles.avatar} aria-hidden="true">
              {name.charAt(0).toUpperCase()}
            </span>
            {name}
          </span>
          <button className="btn btn-outline" onClick={logout}>
            <LogOut /> Log out
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
