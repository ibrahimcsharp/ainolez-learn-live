import { lazy, Suspense } from "react";
import { Route, Routes } from "react-router";
import { ForgotPasswordPage } from "../features/auth/ForgotPasswordPage";
import { LoginPage } from "../features/auth/LoginPage";
import { RegisterPage } from "../features/auth/RegisterPage";
import { ResetPasswordPage } from "../features/auth/ResetPasswordPage";
import { VerifyEmailPage } from "../features/auth/VerifyEmailPage";
import { AIPage } from "../features/assistant/AIPage";
import { CatalogPage } from "../features/catalog/CatalogPage";
import { CommunityPage } from "../features/community/CommunityPage";
import { PostPage } from "../features/community/PostPage";
import { CertificatePage } from "../features/certificates/CertificatePage";
import { LeaderboardPage } from "../features/gamification/LeaderboardPage";
import { CoursePage } from "../features/catalog/CoursePage";
import { HomePage } from "../features/home/HomePage";
import { LessonPage } from "../features/lesson/LessonPage";
import { SearchPage } from "../features/search/SearchPage";
import { PortalLayout } from "./layouts/PortalLayout";
import { PublicLayout } from "./layouts/PublicLayout";
import { NotFound } from "./NotFound";
import { RequireRole } from "./RequireRole";
import { PageLoader } from "../shared/ui/Loader";

/*
 * The learner portal and the admin panel load only when opened, so a visitor's first
 * download carries just the public website.
 */
function lazyPage(load, name) {
  const Page = lazy(() => load().then((module) => ({ default: module[name] })));
  return function LazyPage() {
    return (
      <Suspense fallback={<PageLoader />}>
        <Page />
      </Suspense>
    );
  };
}
const ProfilePage = lazyPage(() => import("../features/account/ProfilePage"), "ProfilePage");
const AdminDashboardPage = lazyPage(() => import("../features/admin/AdminDashboardPage"), "AdminDashboardPage");
const AnalyticsPage = lazyPage(() => import("../features/admin/analytics/AnalyticsPage"), "AnalyticsPage");
const CourseGeneratorPage = lazyPage(() => import("../features/admin/ai-authoring/CourseGeneratorPage"), "CourseGeneratorPage");
const AIPanelPage = lazyPage(() => import("../features/admin/assistant/AIPanelPage"), "AIPanelPage");
const QuizEditPage = lazyPage(() => import("../features/admin/assessment/QuizEditPage"), "QuizEditPage");
const ModerationPage = lazyPage(() => import("../features/admin/community/ModerationPage"), "ModerationPage");
const CertificatesPage = lazyPage(() => import("../features/admin/certification/CertificatesPage"), "CertificatesPage");
const GamificationPage = lazyPage(() => import("../features/admin/gamification/GamificationPage"), "GamificationPage");
const CategoriesPage = lazyPage(() => import("../features/admin/catalog/CategoriesPage"), "CategoriesPage");
const CourseEditPage = lazyPage(() => import("../features/admin/catalog/CourseEditPage"), "CourseEditPage");
const CoursesPage = lazyPage(() => import("../features/admin/catalog/CoursesPage"), "CoursesPage");
const LessonEditPage = lazyPage(() => import("../features/admin/catalog/LessonEditPage"), "LessonEditPage");
const PathsPage = lazyPage(() => import("../features/admin/catalog/PathsPage"), "PathsPage");
const MarkdownToolPage = lazyPage(() => import("../features/admin/content-tools/MarkdownToolPage"), "MarkdownToolPage");
const MediaPage = lazyPage(() => import("../features/admin/media/MediaPage"), "MediaPage");
const SeoPage = lazyPage(() => import("../features/admin/seo/SeoPage"), "SeoPage");
const TrashPage = lazyPage(() => import("../features/admin/trash/TrashPage"), "TrashPage");
const MenusPage = lazyPage(() => import("../features/admin/website/MenusPage"), "MenusPage");
const PageEditPage = lazyPage(() => import("../features/admin/website/PageEditPage"), "PageEditPage");
const PagesPage = lazyPage(() => import("../features/admin/website/PagesPage"), "PagesPage");
const DashboardPage = lazyPage(() => import("../features/learning/DashboardPage"), "DashboardPage");

export function AppRoutes() {
  return (
    <Routes>
      {/* Public website. Fixed paths win over the /:courseSlug patterns.
          /:courseSlug also shows site pages (Admin -> Pages) when no course has that slug. */}
      <Route element={<PublicLayout />}>
        <Route index element={<HomePage />} />
        <Route path="login" element={<LoginPage />} />
        <Route path="register" element={<RegisterPage />} />
        <Route path="verify-email" element={<VerifyEmailPage />} />
        <Route path="forgot-password" element={<ForgotPasswordPage />} />
        <Route path="reset-password" element={<ResetPasswordPage />} />
        <Route path="courses" element={<CatalogPage />} />
        <Route path="search" element={<SearchPage />} />
        <Route path="leaderboard" element={<LeaderboardPage />} />
        <Route path="community" element={<CommunityPage />} />
        <Route path="community/posts/:id" element={<PostPage />} />
        <Route path="ai" element={<AIPage />} />
        <Route path="certificates/:code" element={<CertificatePage />} />
        <Route path=":courseSlug" element={<CoursePage />} />
        <Route path=":courseSlug/:lessonSlug" element={<LessonPage />} />
        <Route path="*" element={<NotFound />} />
      </Route>

      {/* Learner portal */}
      <Route
        path="dashboard"
        element={
          <RequireRole role="learner">
            <PortalLayout area="learner" />
          </RequireRole>
        }
      >
        <Route index element={<DashboardPage />} />
        <Route path="profile" element={<ProfilePage />} />
      </Route>

      {/* Super admin panel */}
      <Route
        path="admin"
        element={
          <RequireRole role="super_admin">
            <PortalLayout area="admin" />
          </RequireRole>
        }
      >
        <Route index element={<AdminDashboardPage />} />
        <Route path="categories" element={<CategoriesPage />} />
        <Route path="courses" element={<CoursesPage />} />
        <Route path="courses/:id" element={<CourseEditPage />} />
        <Route path="lessons/:id" element={<LessonEditPage />} />
        <Route path="quizzes/:id" element={<QuizEditPage />} />
        <Route path="paths" element={<PathsPage />} />
        <Route path="certificates" element={<CertificatesPage />} />
        <Route path="gamification" element={<GamificationPage />} />
        <Route path="moderation" element={<ModerationPage />} />
        <Route path="ai" element={<AIPanelPage />} />
        <Route path="course-generator" element={<CourseGeneratorPage />} />
        <Route path="analytics" element={<AnalyticsPage />} />
        <Route path="pages" element={<PagesPage />} />
        <Route path="pages/:id" element={<PageEditPage />} />
        <Route path="menus" element={<MenusPage />} />
        <Route path="seo" element={<SeoPage />} />
        <Route path="media" element={<MediaPage />} />
        <Route path="markdown" element={<MarkdownToolPage />} />
        <Route path="trash" element={<TrashPage />} />
      </Route>
    </Routes>
  );
}
