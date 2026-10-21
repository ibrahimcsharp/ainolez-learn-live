import { Route, Routes } from "react-router";
import { ProfilePage } from "../features/account/ProfilePage";
import { AdminDashboardPage } from "../features/admin/AdminDashboardPage";
import { AnalyticsPage } from "../features/admin/analytics/AnalyticsPage";
import { CourseGeneratorPage } from "../features/admin/ai-authoring/CourseGeneratorPage";
import { AIPanelPage } from "../features/admin/assistant/AIPanelPage";
import { QuizEditPage } from "../features/admin/assessment/QuizEditPage";
import { ModerationPage } from "../features/admin/community/ModerationPage";
import { CertificatesPage } from "../features/admin/certification/CertificatesPage";
import { GamificationPage } from "../features/admin/gamification/GamificationPage";
import { CategoriesPage } from "../features/admin/catalog/CategoriesPage";
import { CourseEditPage } from "../features/admin/catalog/CourseEditPage";
import { CoursesPage } from "../features/admin/catalog/CoursesPage";
import { LessonEditPage } from "../features/admin/catalog/LessonEditPage";
import { PathsPage } from "../features/admin/catalog/PathsPage";
import { MarkdownToolPage } from "../features/admin/content-tools/MarkdownToolPage";
import { MediaPage } from "../features/admin/media/MediaPage";
import { SeoPage } from "../features/admin/seo/SeoPage";
import { TrashPage } from "../features/admin/trash/TrashPage";
import { MenusPage } from "../features/admin/website/MenusPage";
import { PageEditPage } from "../features/admin/website/PageEditPage";
import { PagesPage } from "../features/admin/website/PagesPage";
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
import { DashboardPage } from "../features/learning/DashboardPage";
import { LessonPage } from "../features/lesson/LessonPage";
import { SearchPage } from "../features/search/SearchPage";
import { PortalLayout } from "./layouts/PortalLayout";
import { PublicLayout } from "./layouts/PublicLayout";
import { NotFound } from "./NotFound";
import { RequireRole } from "./RequireRole";

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
