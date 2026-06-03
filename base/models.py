from django.db import models
import uuid
from decimal import Decimal

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


class UUIDTimeStampedModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    class Role(models.TextChoices):
        LEARNER = "LEARNER", "Learner"
        INSTRUCTOR = "INSTRUCTOR", "Instructor"
        ADMIN = "ADMIN", "Admin"

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=30, choices=Role.choices, default=Role.LEARNER)
    profile_image = models.ImageField(upload_to="users/profile_images/", blank=True, null=True)
    total_xp = models.PositiveIntegerField(default=0)
    current_level = models.PositiveIntegerField(default=1)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.get_full_name() or self.username


class UserProfile(UUIDTimeStampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(blank=True)
    preferred_language = models.ForeignKey(
        "ProgrammingLanguage",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="preferred_by_users",
    )
    learning_goal = models.TextField(blank=True)
    daily_goal_minutes = models.PositiveIntegerField(default=30)
    streak_count = models.PositiveIntegerField(default=0)
    longest_streak = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Profile of {self.user}"


class ProgrammingLanguage(UUIDTimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    version = models.CharField(max_length=40, blank=True)
    compiler_key = models.CharField(max_length=80, blank=True)
    description = models.TextField(blank=True)
    icon = models.ImageField(upload_to="languages/icons/", blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class LearningPath(UUIDTimeStampedModel):
    class Difficulty(models.TextChoices):
        BEGINNER = "BEGINNER", "Beginner"
        INTERMEDIATE = "INTERMEDIATE", "Intermediate"
        ADVANCED = "ADVANCED", "Advanced"

    language = models.ForeignKey(ProgrammingLanguage, on_delete=models.CASCADE, related_name="learning_paths")
    title = models.CharField(max_length=180)
    slug = models.SlugField(max_length=220, unique=True)
    description = models.TextField(blank=True)
    difficulty = models.CharField(max_length=30, choices=Difficulty.choices, default=Difficulty.BEGINNER)
    estimated_hours = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["language", "title"]

    def __str__(self):
        return self.title


class Lesson(UUIDTimeStampedModel):
    learning_path = models.ForeignKey(LearningPath, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=180)
    slug = models.SlugField(max_length=220)
    
    # ========== COMPLETE COURSE CONTENT FIELDS ==========
    # Main content
    theory_content = models.TextField(blank=True, help_text="Main lesson content with HTML formatting")
    example_code = models.TextField(blank=True, help_text="Code examples with syntax highlighting")
    
    # NEW FIELDS FOR COMPREHENSIVE LEARNING
    learning_objectives = models.TextField(blank=True, help_text="What students will learn in this lesson")
    key_concepts = models.TextField(blank=True, help_text="List of key concepts, one per line or comma-separated")
    practice_exercises = models.TextField(blank=True, help_text="Practice exercises for students")
    additional_resources = models.TextField(blank=True, help_text="Links to additional learning resources")
    common_mistakes = models.TextField(blank=True, help_text="Common mistakes and how to avoid them")
    quiz_questions_json = models.JSONField(default=list, blank=True, help_text="JSON array of quiz questions for this lesson")
    
    # Existing fields
    xp_reward = models.PositiveIntegerField(default=10)
    order = models.PositiveIntegerField(default=0)
    is_locked = models.BooleanField(default=False)
    
    class Meta:
        ordering = ["learning_path", "order"]
        constraints = [
            models.UniqueConstraint(fields=["learning_path", "slug"], name="unique_lesson_slug_per_path"),
            models.UniqueConstraint(fields=["learning_path", "order"], name="unique_lesson_order_per_path"),
        ]

    def __str__(self):
        return self.title
    
    def get_key_concepts_list(self):
        """Return key concepts as a list"""
        if not self.key_concepts:
            return []
        # Split by newline or comma
        import re
        concepts = re.split(r'[\n,]+', self.key_concepts)
        return [c.strip() for c in concepts if c.strip()]
    
    def get_practice_exercises_list(self):
        """Return practice exercises as a list"""
        if not self.practice_exercises:
            return []
        exercises = self.practice_exercises.split('\n')
        return [e.strip() for e in exercises if e.strip()]


class Challenge(UUIDTimeStampedModel):
    class ChallengeType(models.TextChoices):
        CODING = "CODING", "Coding Challenge"
        DEBUG = "DEBUG", "Debug Arena"
        QUIZ = "QUIZ", "Quiz"
        BATTLE = "BATTLE", "Battle"

    class Difficulty(models.TextChoices):
        EASY = "EASY", "Easy"
        MEDIUM = "MEDIUM", "Medium"
        HARD = "HARD", "Hard"
        EXPERT = "EXPERT", "Expert"

    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True, blank=True, related_name="challenges")
    language = models.ForeignKey(ProgrammingLanguage, on_delete=models.CASCADE, related_name="challenges")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="created_challenges")
    title = models.CharField(max_length=180)
    slug = models.SlugField(max_length=220, unique=True)
    challenge_type = models.CharField(max_length=20, choices=ChallengeType.choices, default=ChallengeType.CODING)
    difficulty = models.CharField(max_length=20, choices=Difficulty.choices, default=Difficulty.EASY)
    problem_statement = models.TextField()
    starter_code = models.TextField(blank=True)
    buggy_code = models.TextField(blank=True)
    expected_output = models.TextField(blank=True)
    test_cases = models.JSONField(default=list, blank=True)
    constraints_text = models.TextField(blank=True)
    xp_reward = models.PositiveIntegerField(default=50)
    time_limit_seconds = models.PositiveIntegerField(default=2)
    memory_limit_mb = models.PositiveIntegerField(default=128)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["difficulty", "title"]
        indexes = [
            models.Index(fields=["language", "difficulty"]),
            models.Index(fields=["challenge_type", "is_active"]),
        ]

    def __str__(self):
        return self.title


class CodeSubmission(UUIDTimeStampedModel):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        RUNNING = "RUNNING", "Running"
        ACCEPTED = "ACCEPTED", "Accepted"
        WRONG_ANSWER = "WRONG_ANSWER", "Wrong Answer"
        RUNTIME_ERROR = "RUNTIME_ERROR", "Runtime Error"
        TIME_LIMIT_EXCEEDED = "TIME_LIMIT_EXCEEDED", "Time Limit Exceeded"
        COMPILATION_ERROR = "COMPILATION_ERROR", "Compilation Error"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="code_submissions")
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name="submissions")
    submitted_code = models.TextField()
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.PENDING)
    passed_test_cases = models.PositiveIntegerField(default=0)
    total_test_cases = models.PositiveIntegerField(default=0)
    score = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("0.00"))
    execution_time_ms = models.PositiveIntegerField(default=0)
    memory_used_kb = models.PositiveIntegerField(default=0)
    output = models.TextField(blank=True)
    error_message = models.TextField(blank=True)
    judged_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "status"]),
            models.Index(fields=["challenge", "status"]),
        ]

    def __str__(self):
        return f"{self.user} - {self.challenge} - {self.status}"


class Quiz(UUIDTimeStampedModel):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="quizzes")
    title = models.CharField(max_length=180)
    description = models.TextField(blank=True, help_text="Description of the quiz")
    time_limit_minutes = models.PositiveIntegerField(default=10)
    xp_reward = models.PositiveIntegerField(default=20)
    passing_score = models.PositiveIntegerField(default=70, help_text="Minimum score percentage to pass")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class QuizQuestion(UUIDTimeStampedModel):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    question_text = models.TextField()
    explanation = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["quiz", "order"]

    def __str__(self):
        return self.question_text[:80]


class QuizChoice(UUIDTimeStampedModel):
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE, related_name="choices")
    choice_text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text


class QuizAttempt(UUIDTimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="quiz_attempts")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="attempts")
    score = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("0.00"))
    xp_earned = models.PositiveIntegerField(default=0)
    started_at = models.DateTimeField(default=timezone.now)
    submitted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.quiz}"


class QuizAnswer(UUIDTimeStampedModel):
    attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE, related_name="answers")
    selected_choice = models.ForeignKey(QuizChoice, on_delete=models.SET_NULL, null=True, blank=True)
    is_correct = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["attempt", "question"], name="unique_quiz_answer_per_question")
        ]

    def __str__(self):
        return f"Answer for {self.question}"


class LearningProgress(UUIDTimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="learning_progress")
    learning_path = models.ForeignKey(LearningPath, on_delete=models.CASCADE, related_name="progress_records")
    completed_lessons = models.ManyToManyField(Lesson, blank=True, related_name="completed_by_users")
    progress_percent = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "learning_path"], name="unique_learning_progress_per_user_path")
        ]

    def __str__(self):
        return f"{self.user} - {self.learning_path}"


class Badge(UUIDTimeStampedModel):
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    icon = models.ImageField(upload_to="badges/icons/", blank=True, null=True)
    xp_required = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class UserBadge(UUIDTimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="badges")
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name="user_badges")
    awarded_at = models.DateTimeField(default=timezone.now)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "badge"], name="unique_badge_per_user")
        ]

    def __str__(self):
        return f"{self.user} - {self.badge}"


class MultiplayerBattle(UUIDTimeStampedModel):
    class Status(models.TextChoices):
        WAITING = "WAITING", "Waiting"
        ACTIVE = "ACTIVE", "Active"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"

    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name="battles")
    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="hosted_battles")
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, through="BattleParticipant", related_name="battles")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.WAITING)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Battle - {self.challenge}"


class BattleParticipant(UUIDTimeStampedModel):
    battle = models.ForeignKey(MultiplayerBattle, on_delete=models.CASCADE, related_name="battle_participants")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="battle_participations")
    submission = models.ForeignKey(CodeSubmission, on_delete=models.SET_NULL, null=True, blank=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("0.00"))
    rank = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["battle", "user"], name="unique_battle_participant")
        ]

    def __str__(self):
        return f"{self.user} in {self.battle}"


class AIHint(UUIDTimeStampedModel):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name="ai_hints")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ai_hints")
    prompt_context = models.JSONField(default=dict, blank=True)
    hint_text = models.TextField()
    used_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Hint for {self.user} - {self.challenge}"


class AdaptiveDifficultyLog(UUIDTimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="difficulty_logs")
    previous_difficulty = models.CharField(max_length=20, choices=Challenge.Difficulty.choices)
    new_difficulty = models.CharField(max_length=20, choices=Challenge.Difficulty.choices)
    reason = models.TextField(blank=True)
    metrics = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"{self.user}: {self.previous_difficulty} -> {self.new_difficulty}"


class LeaderboardEntry(UUIDTimeStampedModel):
    class Period(models.TextChoices):
        DAILY = "DAILY", "Daily"
        WEEKLY = "WEEKLY", "Weekly"
        MONTHLY = "MONTHLY", "Monthly"
        ALL_TIME = "ALL_TIME", "All Time"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="leaderboard_entries")
    period = models.CharField(max_length=20, choices=Period.choices)
    period_start = models.DateField()
    period_end = models.DateField()
    xp_points = models.PositiveIntegerField(default=0)
    challenge_points = models.PositiveIntegerField(default=0)
    battle_points = models.PositiveIntegerField(default=0)
    quiz_points = models.PositiveIntegerField(default=0)
    total_points = models.PositiveIntegerField(default=0)
    rank = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        ordering = ["rank", "-total_points"]
        constraints = [
            models.UniqueConstraint(fields=["user", "period", "period_start", "period_end"], name="unique_leaderboard_entry")
        ]

    def save(self, *args, **kwargs):
        self.total_points = self.xp_points + self.challenge_points + self.battle_points + self.quiz_points
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} - {self.total_points}"


class Notification(UUIDTimeStampedModel):
    class Type(models.TextChoices):
        CHALLENGE_COMPLETED = "CHALLENGE_COMPLETED", "Challenge Completed"
        BADGE_UNLOCKED = "BADGE_UNLOCKED", "Badge Unlocked"
        BATTLE_INVITE = "BATTLE_INVITE", "Battle Invite"
        LEVEL_UP = "LEVEL_UP", "Level Up"
        AI_HINT_READY = "AI_HINT_READY", "AI Hint Ready"
        SYSTEM = "SYSTEM", "System"

    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    notification_type = models.CharField(max_length=40, choices=Type.choices)
    title = models.CharField(max_length=180)
    message = models.TextField(blank=True)
    is_read = models.BooleanField(default=False)
    metadata = models.JSONField(default=dict, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["recipient", "is_read"])]

    def mark_as_read(self):
        self.is_read = True
        self.read_at = timezone.now()
        self.save(update_fields=["is_read", "read_at", "updated_at"])

    def __str__(self):
        return self.title