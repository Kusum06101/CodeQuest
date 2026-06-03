from django.http import HttpResponse
from django.urls import include, path
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

from . import views


router = DefaultRouter()
router.register(r"users", views.UserViewSet, basename="api-user")
router.register(r"profiles", views.UserProfileViewSet, basename="api-user-profile")
router.register(r"languages", views.ProgrammingLanguageViewSet, basename="api-programming-language")
router.register(r"learning-paths", views.LearningPathViewSet, basename="api-learning-path")
router.register(r"lessons", views.LessonViewSet, basename="api-lesson")
router.register(r"challenges", views.ChallengeViewSet, basename="api-challenge")
router.register(r"submissions", views.CodeSubmissionViewSet, basename="api-code-submission")
router.register(r"quizzes", views.QuizViewSet, basename="api-quiz")
router.register(r"quiz-questions", views.QuizQuestionViewSet, basename="api-quiz-question")
router.register(r"quiz-choices", views.QuizChoiceViewSet, basename="api-quiz-choice")
router.register(r"quiz-attempts", views.QuizAttemptViewSet, basename="api-quiz-attempt")
router.register(r"quiz-answers", views.QuizAnswerViewSet, basename="api-quiz-answer")
router.register(r"progress", views.LearningProgressViewSet, basename="api-learning-progress")
router.register(r"badges", views.BadgeViewSet, basename="api-badge")
router.register(r"user-badges", views.UserBadgeViewSet, basename="api-user-badge")
router.register(r"battles", views.MultiplayerBattleViewSet, basename="api-multiplayer-battle")
router.register(r"battle-participants", views.BattleParticipantViewSet, basename="api-battle-participant")
router.register(r"ai-hints", views.AIHintViewSet, basename="api-ai-hint")
router.register(
    r"difficulty-logs",
    views.AdaptiveDifficultyLogViewSet,
    basename="api-adaptive-difficulty-log",
)
router.register(r"leaderboard", views.LeaderboardEntryViewSet, basename="api-leaderboard-entry")
router.register(r"notifications", views.NotificationViewSet, basename="api-notification")


urlpatterns = [
    # ============================================
    # SIMPLE DEBUG VIEWS (No styling)
    # ============================================
    path("simple-course/<slug:slug>/", views.simple_course_view, name="simple_course"),
    path("simple-lesson/<slug:path_slug>/<slug:lesson_slug>/", views.simple_lesson_view, name="simple_lesson"),
    path("test/<slug:path_slug>/<slug:lesson_slug>/", 
         lambda request, path_slug, lesson_slug: HttpResponse(f"path_slug={path_slug}, lesson_slug={lesson_slug}")),
    
    # ============================================
    # PUBLIC PAGES (No Login Required)
    # ============================================
    
    # Home page
    path("", views.HomeView.as_view(), name="home"),
    
    # Redirect for /languages/
    path("languages/", RedirectView.as_view(pattern_name="learning_paths", permanent=False)),
    
    # Authentication
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),
    
    # ============================================
    # LESSON URLS (MUST COME FIRST)
    # ============================================
    path("learn/<slug:path_slug>/lesson/<slug:lesson_slug>/", 
         views.lesson_detail_view, name="lesson_detail"),
    
    path("learn/<slug:path_slug>/lessons/", 
         views.LearningPathLessonsView.as_view(), name="learning_path_lessons"),
    
    path("lesson/<uuid:lesson_id>/complete/", 
         views.CompleteLessonView.as_view(), name="complete_lesson"),
    
    # ============================================
    # LEARNING PATH URLS
    # ============================================
    path("learn/", views.LearningPathsListView.as_view(), name="learning_paths"),
    path("learn/<path:slug>/", views.PublicLearningPathDetailView.as_view(), name="learning_path_detail"),
    
    # ============================================
    # AUTHENTICATED PAGES (Login Required)
    # ============================================
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("profile/edit/", views.ProfileEditView.as_view(), name="profile_edit"),
    path("profile/change-password/", views.ChangePasswordView.as_view(), name="change_password"),
    
    # ============================================
    # REAL TIME / LIVE LEARNING
    # ============================================
    path("realtime/", views.realtime_learning_view, name="realtime_learning"),
    
    # ============================================
    # QUIZZES
    # ============================================
    path("quiz/<uuid:quiz_id>/", views.TakeQuizView.as_view(), name="take_quiz"),
    path("quiz/result/<uuid:attempt_id>/", views.QuizResultView.as_view(), name="quiz_result"),
    path("quizzes/", views.PublicQuizListView.as_view(), name="quizzes"),
    path("all-quizzes/", views.AllQuizzesListView.as_view(), name="all_quizzes"),  # NEW: Show all quizzes
    
    # ============================================
    # CHALLENGES
    # ============================================
    path("challenges/", views.PublicChallengeListView.as_view(), name="challenges"),
    path("challenges/<uuid:pk>/", views.PublicChallengeDetailView.as_view(), name="challenge_detail"),
    path("challenges/<uuid:challenge_id>/submit/", views.SubmitChallengeView.as_view(), name="submit_challenge"),
    
    # ============================================
    # LEADERBOARD & SEARCH
    # ============================================
    path("leaderboard/", views.LeaderboardView.as_view(), name="leaderboard"),
    path("search/", views.SearchView.as_view(), name="search"),
    
    # ============================================
    # API ROUTES
    # ============================================
    path("api/", include(router.urls)),
    path("api/auth/", include('rest_framework.urls')),
    
    # ============================================
    # SIMPLE ADMIN ROUTES (Only essential ones)
    # ============================================
    path("admin/learning-paths/", views.LearningPathListView.as_view(), name="learning-path-list"),
    path("admin/learning-paths/create/", views.LearningPathCreateView.as_view(), name="learning-path-create"),
    path("admin/lessons/", views.LessonListView.as_view(), name="lesson-list"),
    path("admin/lessons/create/", views.LessonCreateView.as_view(), name="lesson-create"),
    path("admin/challenges/", views.ChallengeListView.as_view(), name="challenge-list"),
    path("admin/challenges/create/", views.ChallengeCreateView.as_view(), name="challenge-create"),
    path("admin/quizzes/", views.QuizListView.as_view(), name="quiz-list"),
    path("admin/quizzes/create/", views.QuizCreateView.as_view(), name="quiz-create"),
    path("admin/badges/", views.BadgeListView.as_view(), name="badge-list"),
    path("admin/badges/create/", views.BadgeCreateView.as_view(), name="badge-create"),
    path("admin/users/", views.UserListView.as_view(), name="user-list"),
    path("admin/users/create/", views.UserCreateView.as_view(), name="user-create"),
    path("admin/languages/", views.ProgrammingLanguageListView.as_view(), name="programming-language-list"),
    path("admin/languages/create/", views.ProgrammingLanguageCreateView.as_view(), name="programming-language-create"),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)