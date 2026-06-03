# base/admin.py
from django.contrib import admin
from .models import (
    ProgrammingLanguage,
    LearningPath,
    Lesson,
    Challenge,
    Quiz,
    QuizQuestion,
    QuizChoice,
    QuizAttempt,
    QuizAnswer,
    CodeSubmission,
    LearningProgress,
    Badge,
    UserBadge,
    UserProfile,
    MultiplayerBattle,
    BattleParticipant,
    AIHint,
    AdaptiveDifficultyLog,
    LeaderboardEntry,
    Notification,
)

@admin.register(ProgrammingLanguage)
class ProgrammingLanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'version', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('is_active',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(LearningPath)
class LearningPathAdmin(admin.ModelAdmin):
    list_display = ('title', 'language', 'difficulty', 'estimated_hours', 'is_active')
    search_fields = ('title', 'description')
    list_filter = ('language', 'difficulty', 'is_active')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ()

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'learning_path', 'order', 'xp_reward', 'is_locked')
    search_fields = ('title', 'theory_content')
    list_filter = ('learning_path', 'is_locked')
    ordering = ('learning_path', 'order')

@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('title', 'language', 'difficulty', 'challenge_type', 'xp_reward', 'is_active')
    search_fields = ('title', 'problem_statement')
    list_filter = ('language', 'difficulty', 'challenge_type', 'is_active')

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'lesson', 'time_limit_minutes', 'xp_reward', 'is_active')
    search_fields = ('title',)
    list_filter = ('lesson', 'is_active')

@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'question_text', 'order')
    search_fields = ('question_text',)
    list_filter = ('quiz',)

@admin.register(QuizChoice)
class QuizChoiceAdmin(admin.ModelAdmin):
    list_display = ('question', 'choice_text', 'is_correct')
    search_fields = ('choice_text',)
    list_filter = ('is_correct',)

@admin.register(CodeSubmission)
class CodeSubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'challenge', 'status', 'score', 'created_at')
    search_fields = ('user__username', 'challenge__title')
    list_filter = ('status',)

@admin.register(LearningProgress)
class LearningProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'learning_path', 'progress_percent', 'completed_at')
    search_fields = ('user__username', 'learning_path__title')
    list_filter = ('learning_path',)

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'xp_required')
    search_fields = ('name',)

@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ('user', 'badge', 'awarded_at')
    search_fields = ('user__username', 'badge__name')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'preferred_language', 'daily_goal_minutes', 'streak_count')
    search_fields = ('user__username', 'bio')

@admin.register(MultiplayerBattle)
class MultiplayerBattleAdmin(admin.ModelAdmin):
    list_display = ('challenge', 'host', 'status', 'started_at')
    list_filter = ('status',)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'notification_type', 'title', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read')
    search_fields = ('recipient__username', 'title')