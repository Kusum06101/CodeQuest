from rest_framework import serializers

from .models import (
    AIHint,
    AdaptiveDifficultyLog,
    Badge,
    BattleParticipant,
    Challenge,
    CodeSubmission,
    LeaderboardEntry,
    LearningPath,
    LearningProgress,
    Lesson,
    MultiplayerBattle,
    Notification,
    ProgrammingLanguage,
    Quiz,
    QuizAnswer,
    QuizAttempt,
    QuizChoice,
    QuizQuestion,
    User,
    UserBadge,
    UserProfile,
)


class UserPublicSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="get_full_name", read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "role",
            "profile_image",
            "total_xp",
            "current_level",
            "is_verified",
        )
        read_only_fields = ("id", "total_xp", "current_level", "is_verified")


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserPublicSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = (
            "id",
            "user",
            "bio",
            "preferred_language",
            "learning_goal",
            "daily_goal_minutes",
            "streak_count",
            "longest_streak",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "streak_count", "longest_streak", "created_at", "updated_at")


class ProgrammingLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgrammingLanguage
        fields = (
            "id",
            "name",
            "slug",
            "version",
            "compiler_key",
            "description",
            "icon",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")


class LearningPathSerializer(serializers.ModelSerializer):
    language_detail = ProgrammingLanguageSerializer(source="language", read_only=True)

    class Meta:
        model = LearningPath
        fields = (
            "id",
            "language",
            "language_detail",
            "title",
            "slug",
            "description",
            "difficulty",
            "estimated_hours",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")


class LessonSerializer(serializers.ModelSerializer):
    learning_path_detail = LearningPathSerializer(source="learning_path", read_only=True)

    class Meta:
        model = Lesson
        fields = (
            "id",
            "learning_path",
            "learning_path_detail",
            "title",
            "slug",
            "theory_content",
            "example_code",
            "xp_reward",
            "order",
            "is_locked",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")


class ChallengeSerializer(serializers.ModelSerializer):
    language_detail = ProgrammingLanguageSerializer(source="language", read_only=True)
    created_by_detail = UserPublicSerializer(source="created_by", read_only=True)

    class Meta:
        model = Challenge
        fields = (
            "id",
            "lesson",
            "language",
            "language_detail",
            "created_by",
            "created_by_detail",
            "title",
            "slug",
            "challenge_type",
            "difficulty",
            "problem_statement",
            "starter_code",
            "buggy_code",
            "expected_output",
            "test_cases",
            "constraints_text",
            "xp_reward",
            "time_limit_seconds",
            "memory_limit_mb",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_by", "created_at", "updated_at")


class CodeSubmissionSerializer(serializers.ModelSerializer):
    user = UserPublicSerializer(read_only=True)

    class Meta:
        model = CodeSubmission
        fields = (
            "id",
            "user",
            "challenge",
            "submitted_code",
            "status",
            "passed_test_cases",
            "total_test_cases",
            "score",
            "execution_time_ms",
            "memory_used_kb",
            "output",
            "error_message",
            "judged_at",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "user",
            "status",
            "passed_test_cases",
            "total_test_cases",
            "score",
            "execution_time_ms",
            "memory_used_kb",
            "output",
            "error_message",
            "judged_at",
            "created_at",
            "updated_at",
        )


class QuizChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizChoice
        fields = ("id", "question", "choice_text", "is_correct", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")
        extra_kwargs = {"is_correct": {"write_only": True}}


class QuizQuestionSerializer(serializers.ModelSerializer):
    choices = QuizChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = QuizQuestion
        fields = (
            "id",
            "quiz",
            "question_text",
            "explanation",
            "order",
            "choices",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")


class QuizSerializer(serializers.ModelSerializer):
    questions = QuizQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = (
            "id",
            "lesson",
            "title",
            "time_limit_minutes",
            "xp_reward",
            "is_active",
            "questions",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")


class QuizAttemptSerializer(serializers.ModelSerializer):
    user = UserPublicSerializer(read_only=True)

    class Meta:
        model = QuizAttempt
        fields = (
            "id",
            "user",
            "quiz",
            "score",
            "xp_earned",
            "started_at",
            "submitted_at",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "user",
            "score",
            "xp_earned",
            "started_at",
            "submitted_at",
            "created_at",
            "updated_at",
        )


class QuizAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizAnswer
        fields = (
            "id",
            "attempt",
            "question",
            "selected_choice",
            "is_correct",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "is_correct", "created_at", "updated_at")

    def validate(self, attrs):
        question = attrs.get("question") or getattr(self.instance, "question", None)
        selected_choice = attrs.get("selected_choice")

        if selected_choice and question and selected_choice.question_id != question.id:
            raise serializers.ValidationError(
                {"selected_choice": "Selected choice must belong to the question."}
            )

        return attrs


class LearningProgressSerializer(serializers.ModelSerializer):
    user = UserPublicSerializer(read_only=True)

    class Meta:
        model = LearningProgress
        fields = (
            "id",
            "user",
            "learning_path",
            "completed_lessons",
            "progress_percent",
            "completed_at",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "user", "created_at", "updated_at")

    def validate(self, attrs):
        learning_path = attrs.get("learning_path") or getattr(self.instance, "learning_path", None)
        completed_lessons = attrs.get("completed_lessons", [])

        if learning_path and completed_lessons:
            invalid_lessons = [
                lesson.id for lesson in completed_lessons if lesson.learning_path_id != learning_path.id
            ]
            if invalid_lessons:
                raise serializers.ValidationError(
                    {"completed_lessons": "All completed lessons must belong to the learning path."}
                )

        return attrs


class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = ("id", "name", "description", "icon", "xp_required", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")


class UserBadgeSerializer(serializers.ModelSerializer):
    user = UserPublicSerializer(read_only=True)
    badge_detail = BadgeSerializer(source="badge", read_only=True)

    class Meta:
        model = UserBadge
        fields = ("id", "user", "badge", "badge_detail", "awarded_at", "created_at", "updated_at")
        read_only_fields = ("id", "user", "awarded_at", "created_at", "updated_at")


class MultiplayerBattleSerializer(serializers.ModelSerializer):
    host = UserPublicSerializer(read_only=True)
    participant_count = serializers.IntegerField(source="participants.count", read_only=True)

    class Meta:
        model = MultiplayerBattle
        fields = (
            "id",
            "challenge",
            "host",
            "status",
            "participant_count",
            "started_at",
            "completed_at",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "host", "started_at", "completed_at", "created_at", "updated_at")


class BattleParticipantSerializer(serializers.ModelSerializer):
    user = UserPublicSerializer(read_only=True)

    class Meta:
        model = BattleParticipant
        fields = (
            "id",
            "battle",
            "user",
            "submission",
            "score",
            "rank",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "user", "score", "rank", "created_at", "updated_at")


class AIHintSerializer(serializers.ModelSerializer):
    user = UserPublicSerializer(read_only=True)

    class Meta:
        model = AIHint
        fields = (
            "id",
            "challenge",
            "user",
            "prompt_context",
            "hint_text",
            "used_at",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "user", "hint_text", "used_at", "created_at", "updated_at")


class AdaptiveDifficultyLogSerializer(serializers.ModelSerializer):
    user = UserPublicSerializer(read_only=True)

    class Meta:
        model = AdaptiveDifficultyLog
        fields = (
            "id",
            "user",
            "previous_difficulty",
            "new_difficulty",
            "reason",
            "metrics",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "user", "created_at", "updated_at")


class LeaderboardEntrySerializer(serializers.ModelSerializer):
    user = UserPublicSerializer(read_only=True)

    class Meta:
        model = LeaderboardEntry
        fields = (
            "id",
            "user",
            "period",
            "period_start",
            "period_end",
            "xp_points",
            "challenge_points",
            "battle_points",
            "quiz_points",
            "total_points",
            "rank",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "user", "total_points", "rank", "created_at", "updated_at")


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = (
            "id",
            "recipient",
            "notification_type",
            "title",
            "message",
            "is_read",
            "metadata",
            "read_at",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "recipient",
            "notification_type",
            "title",
            "message",
            "metadata",
            "read_at",
            "created_at",
            "updated_at",
        )