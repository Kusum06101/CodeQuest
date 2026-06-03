from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.db.models import Q, Sum, Avg, Count
from django.forms import modelform_factory
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView, TemplateView, FormView
from django.views import View
from django.contrib.auth import login
from django.shortcuts import redirect, get_object_or_404, render
import json
from django.views.decorators.cache import never_cache
from django.core.cache import cache
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.utils.decorators import method_decorator

from .forms import (
    BadgeForm,
    BattleParticipantForm,
    ChallengeForm,
    CodeSubmissionForm,
    LearningPathForm,
    LearningProgressForm,
    LessonForm,
    MultiplayerBattleForm,
    NotificationForm,
    ProgrammingLanguageForm,
    QuizAnswerForm,
    QuizChoiceForm,
    QuizForm,
    QuizQuestionForm,
    UserBadgeForm,
    UserProfileForm,
    UserRegistrationForm,
    UserUpdateForm,
    UserLoginForm,
    ProfileUpdateForm,
)
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

try:
    from rest_framework import filters, permissions, viewsets
    from django_filters.rest_framework import DjangoFilterBackend

    from .serializers import (
        AIHintSerializer,
        AdaptiveDifficultyLogSerializer,
        BadgeSerializer,
        BattleParticipantSerializer,
        ChallengeSerializer,
        CodeSubmissionSerializer,
        LeaderboardEntrySerializer,
        LearningPathSerializer,
        LearningProgressSerializer,
        LessonSerializer,
        MultiplayerBattleSerializer,
        NotificationSerializer,
        ProgrammingLanguageSerializer,
        QuizAnswerSerializer,
        QuizAttemptSerializer,
        QuizChoiceSerializer,
        QuizQuestionSerializer,
        QuizSerializer,
        UserBadgeSerializer,
        UserProfileSerializer,
        UserPublicSerializer,
    )

    DRF_AVAILABLE = True
except ImportError:
    DRF_AVAILABLE = False


class SearchFilterMixin:
    search_param = "q"
    search_fields = ()
    filter_fields = ()

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get(self.search_param, "").strip()

        if search_query and self.search_fields:
            search_filter = Q()
            for field in self.search_fields:
                search_filter |= Q(**{f"{field}__icontains": search_query})
            queryset = queryset.filter(search_filter)

        for field in self.filter_fields:
            value = self.request.GET.get(field)
            if value not in (None, ""):
                queryset = queryset.filter(**{field: value})

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get(self.search_param, "").strip()
        context["active_filters"] = {
            field: self.request.GET.get(field, "") for field in self.filter_fields
        }
        return context


class MessageMixin:
    success_message = "Saved successfully."

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the highlighted errors.")
        return super().form_invalid(form)


class RegisterView(MessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        
        # Create user profile
        UserProfile.objects.get_or_create(user=self.object)
        
        # Award welcome badge
        welcome_badge, _ = Badge.objects.get_or_create(
            name="Welcome to CodeQuest",
            defaults={
                "description": "Joined the CodeQuest learning platform",
                "xp_required": 0
            }
        )
        UserBadge.objects.get_or_create(
            user=self.object,
            badge=welcome_badge,
            defaults={"awarded_at": timezone.now()}
        )
        
        messages.success(self.request, f"🎉 Welcome {self.object.username}! Your learning journey begins now!")
        return redirect('dashboard')


class DeleteMessageMixin:
    delete_message = "Deleted successfully."

    def form_valid(self, form):
        messages.success(self.request, self.delete_message)
        return super().form_valid(form)


class OwnedByRequestUserMixin:
    user_field = "user"

    def form_valid(self, form):
        if not getattr(form.instance, f"{self.user_field}_id", None):
            setattr(form.instance, self.user_field, self.request.user)
        return super().form_valid(form)


class CreatedByRequestUserMixin:
    user_field = "created_by"

    def form_valid(self, form):
        if not getattr(form.instance, f"{self.user_field}_id", None):
            setattr(form.instance, self.user_field, self.request.user)
        return super().form_valid(form)


class RecipientRequestUserMixin:
    user_field = "recipient"

    def form_valid(self, form):
        if not getattr(form.instance, f"{self.user_field}_id", None):
            setattr(form.instance, self.user_field, self.request.user)
        return super().form_valid(form)


def default_form_for(model, exclude=()):
    base_exclude = ("id", "created_at", "updated_at")
    return modelform_factory(model, exclude=base_exclude + tuple(exclude))


# ============================================
# LOGOUT VIEW
# ============================================

@method_decorator(csrf_protect, name='dispatch')
@method_decorator(login_required, name='dispatch')
class CustomLogoutView(View):
    def get(self, request):
        auth_logout(request)
        messages.success(request, "✨ You have been successfully logged out! See you soon! 🚀")
        return redirect('home')
    
    def post(self, request):
        auth_logout(request)
        messages.success(request, "✨ You have been successfully logged out! See you soon! 🚀")
        return redirect('home')


# ============================================
# CHANGE PASSWORD VIEW
# ============================================

class ChangePasswordView(LoginRequiredMixin, FormView):
    template_name = "base/change_password.html"
    form_class = PasswordChangeForm
    success_url = reverse_lazy('profile')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, form.user)
        messages.success(self.request, 'Your password has been changed successfully!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)


# ============================================
# PUBLIC VIEWS (No Login Required)
# ============================================

class HomeView(TemplateView):
    template_name = "base/home.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['languages'] = ProgrammingLanguage.objects.filter(is_active=True)[:6]
        context['featured_paths'] = LearningPath.objects.filter(is_active=True)[:6]
        context['popular_challenges'] = Challenge.objects.filter(is_active=True)[:6]
        context['stats'] = {
            'learners': User.objects.filter(role='LEARNER').count(),
            'lessons': Lesson.objects.count(),
            'challenges': Challenge.objects.count(),
            'languages': ProgrammingLanguage.objects.count()
        }
        return context


class LearningPathsListView(SearchFilterMixin, ListView):
    model = LearningPath
    template_name = "base/learning_paths.html"
    context_object_name = "learning_paths"
    paginate_by = 12
    search_fields = ("title", "description", "language__name")
    filter_fields = ("language", "difficulty", "is_active")
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=True).select_related('language')
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['languages'] = ProgrammingLanguage.objects.filter(is_active=True)
        return context


# ============================================
# PUBLIC LEARNING PATH DETAIL VIEW (For Learners)
# ============================================

class PublicLearningPathDetailView(DetailView):
    """PUBLIC view for learning path detail - shows lessons to learners"""
    model = LearningPath
    template_name = "base/learning_path_detail.html"
    context_object_name = "path"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lessons = self.object.lessons.all().order_by('order')
        
        if self.request.user.is_authenticated:
            progress, _ = LearningProgress.objects.get_or_create(
                user=self.request.user,
                learning_path=self.object
            )
            completed_lesson_ids = progress.completed_lessons.values_list('id', flat=True)
            context['progress'] = progress
            context['completed_lesson_ids'] = list(completed_lesson_ids)
        else:
            context['completed_lesson_ids'] = []
        
        context['lessons'] = lessons
        context['total_lessons'] = lessons.count()
        
        # Debug output
        print(f"PublicLearningPathDetailView: {self.object.title} has {lessons.count()} lessons")
        
        return context


@method_decorator(login_required, name='dispatch')
class LearningPathLessonsView(DetailView):
    """View to display all lessons for a specific learning path - requires login"""
    model = LearningPath
    template_name = "base/learning_path_lessons.html"
    context_object_name = "learning_path"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        learning_path = self.get_object()
        
        # Get all lessons for this path
        lessons = learning_path.lessons.all().order_by('order')
        
        # Get user's progress
        progress, created = LearningProgress.objects.get_or_create(
            user=self.request.user,
            learning_path=learning_path
        )
        completed_lesson_ids = progress.completed_lessons.values_list('id', flat=True)
        
        context['lessons'] = lessons
        context['completed_lesson_ids'] = list(completed_lesson_ids)
        context['progress_percent'] = progress.progress_percent
        context['total_lessons'] = lessons.count()
        context['completed_count'] = progress.completed_lessons.count()
        
        return context


class UserLoginView(TemplateView):
    template_name = "registration/login.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = UserLoginForm()
        return context


# ============================================
# AUTHENTICATION REQUIRED VIEWS
# ============================================

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "base/dashboard.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Progress statistics
        total_lessons = Lesson.objects.count()
        completed_lessons = []
        progress_records = LearningProgress.objects.filter(user=user)
        
        for progress in progress_records:
            completed_lessons.extend(progress.completed_lessons.all())
        
        completed_count = len(set(completed_lessons))
        completion_percentage = (completed_count / total_lessons * 100) if total_lessons > 0 else 0
        
        # XP progress for next level
        xp_for_current_level = (user.current_level - 1) * 1000
        xp_for_next_level = user.current_level * 1000
        xp_progress = ((user.total_xp - xp_for_current_level) / 1000) * 100 if user.total_xp > xp_for_current_level else 0
        
        context.update({
            'user': user,
            'completion_percentage': completion_percentage,
            'completed_lessons_count': completed_count,
            'total_lessons': total_lessons,
            'xp_progress': xp_progress,
            'xp_for_next_level': xp_for_next_level,
            'recent_submissions': CodeSubmission.objects.filter(user=user)[:5],
            'recent_quizzes': QuizAttempt.objects.filter(user=user).order_by('-submitted_at')[:5],
            'active_paths': progress_records.filter(progress_percent__lt=100)[:3],
            'completed_paths': progress_records.filter(progress_percent=100)[:3],
            'recent_badges': user.badges.all().order_by('-awarded_at')[:6],
        })
        
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(require_http_methods(["POST"]), name='dispatch')
class CompleteLessonView(View):
    def post(self, request, lesson_id):
        lesson = get_object_or_404(Lesson, id=lesson_id)
        progress, created = LearningProgress.objects.get_or_create(
            user=request.user,
            learning_path=lesson.learning_path
        )
        
        if not progress.completed_lessons.filter(id=lesson.id).exists():
            progress.completed_lessons.add(lesson)
            
            # Award XP
            request.user.total_xp += lesson.xp_reward
            
            # Check level up
            new_level = (request.user.total_xp // 1000) + 1
            if new_level > request.user.current_level:
                request.user.current_level = new_level
                messages.success(request, f"🎉 LEVEL UP! You've reached Level {new_level}! 🎉")
                
                # Award level-up badge
                level_badge, _ = Badge.objects.get_or_create(
                    name=f"Level {new_level} Achiever",
                    defaults={"description": f"Reached level {new_level}", "xp_required": new_level * 1000}
                )
                UserBadge.objects.get_or_create(user=request.user, badge=level_badge)
            
            request.user.save()
            
            # Update progress percentage
            total_lessons = lesson.learning_path.lessons.count()
            completed_count = progress.completed_lessons.count()
            progress.progress_percent = int((completed_count / total_lessons) * 100)
            
            if progress.progress_percent == 100:
                progress.completed_at = timezone.now()
                
                # Award path completion badge
                path_badge, _ = Badge.objects.get_or_create(
                    name=f"{lesson.learning_path.title} Master",
                    defaults={"description": f"Completed the {lesson.learning_path.title} learning path", "xp_required": 500}
                )
                UserBadge.objects.get_or_create(user=request.user, badge=path_badge)
            
            progress.save()
            
            return JsonResponse({
                'success': True,
                'xp_earned': lesson.xp_reward,
                'total_xp': request.user.total_xp,
                'current_level': request.user.current_level,
                'progress_percent': progress.progress_percent,
                'message': f'🎉 +{lesson.xp_reward} XP!'
            })
        
        return JsonResponse({'success': False, 'message': 'Lesson already completed'})


@method_decorator(login_required, name='dispatch')
class TakeQuizView(View):
    template_name = "base/take_quiz.html"
    
    def get(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, id=quiz_id, is_active=True)
        
        # Check if already attempted
        existing_attempt = QuizAttempt.objects.filter(
            user=request.user, 
            quiz=quiz,
            submitted_at__isnull=False
        ).first()
        
        if existing_attempt:
            messages.warning(request, 'You have already completed this quiz!')
            return redirect('lesson_detail', 
                           path_slug=quiz.lesson.learning_path.slug,
                           lesson_slug=quiz.lesson.slug)
        
        questions = quiz.questions.all().order_by('order')
        
        context = {
            'quiz': quiz,
            'questions': questions,
            'total_questions': questions.count(),
            'time_limit_minutes': quiz.time_limit_minutes
        }
        return render(request, self.template_name, context)
    
    def post(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, id=quiz_id, is_active=True)
        
        score = 0
        total_questions = quiz.questions.count()
        answers = []
        
        for question in quiz.questions.all():
            selected_choice_id = request.POST.get(f'question_{question.id}')
            selected_choice = QuizChoice.objects.filter(
                id=selected_choice_id
            ).first() if selected_choice_id else None
            
            is_correct = selected_choice and selected_choice.is_correct
            if is_correct:
                score += 1
            
            answers.append({
                'question': question,
                'selected_choice': selected_choice,
                'is_correct': is_correct
            })
        
        # Calculate percentage score
        score_percentage = (score / total_questions) * 100 if total_questions > 0 else 0
        xp_earned = int((score_percentage / 100) * quiz.xp_reward)
        
        # Save attempt
        attempt = QuizAttempt.objects.create(
            user=request.user,
            quiz=quiz,
            score=score_percentage,
            xp_earned=xp_earned,
            submitted_at=timezone.now()
        )
        
        # Save answers
        for answer in answers:
            QuizAnswer.objects.create(
                attempt=attempt,
                question=answer['question'],
                selected_choice=answer['selected_choice'],
                is_correct=answer['is_correct']
            )
        
        # Award XP
        request.user.total_xp += xp_earned
        request.user.save()
        
        messages.success(
            request, 
            f'📝 Quiz completed! Score: {score}/{total_questions} ({score_percentage:.1f}%) +{xp_earned} XP'
        )
        
        return redirect('quiz_result', attempt_id=attempt.id)


class QuizResultView(LoginRequiredMixin, DetailView):
    model = QuizAttempt
    template_name = "base/quiz_result.html"
    context_object_name = "attempt"
    
    def get_queryset(self):
        return QuizAttempt.objects.filter(user=self.request.user).select_related('quiz', 'quiz__lesson')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['answers'] = QuizAnswer.objects.filter(
            attempt=self.get_object()
        ).select_related('question', 'selected_choice')
        return context


class LeaderboardView(LoginRequiredMixin, TemplateView):
    template_name = "base/leaderboard.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Global leaderboard (all time)
        top_users = User.objects.filter(is_active=True).order_by('-total_xp')[:50]
        
        # Weekly leaderboard
        week_ago = timezone.now() - timezone.timedelta(days=7)
        weekly_top = User.objects.filter(
            is_active=True,
            quiz_attempts__submitted_at__gte=week_ago
        ).annotate(
            weekly_xp=Sum('quiz_attempts__xp_earned')
        ).order_by('-weekly_xp')[:10]
        
        # Path-specific leaderboards
        path_leaderboards = []
        top_paths = LearningPath.objects.filter(is_active=True)[:5]
        for path in top_paths:
            top_learners = User.objects.filter(
                learning_progress__learning_path=path
            ).annotate(
                path_progress=Avg('learning_progress__progress_percent')
            ).order_by('-path_progress')[:5]
            path_leaderboards.append({
                'path': path,
                'top_learners': top_learners
            })
        
        context.update({
            'top_users': top_users,
            'weekly_top': weekly_top,
            'path_leaderboards': path_leaderboards,
            'user_rank': list(top_users).index(self.request.user) + 1 if self.request.user in top_users else None
        })
        
        return context


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "base/profile.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Get profile or create
        profile, created = UserProfile.objects.get_or_create(user=user)
        
        # Statistics
        total_lessons = Lesson.objects.count()
        completed_lessons = []
        for progress in LearningProgress.objects.filter(user=user):
            completed_lessons.extend(progress.completed_lessons.all())
        completed_count = len(set(completed_lessons))
        
        # Quiz statistics
        quiz_attempts = QuizAttempt.objects.filter(user=user)
        avg_quiz_score = quiz_attempts.aggregate(Avg('score'))['score__avg'] or 0
        
        # Challenge statistics
        submissions = CodeSubmission.objects.filter(user=user)
        solved_challenges = submissions.filter(status='ACCEPTED').values('challenge').distinct().count()
        
        context.update({
            'profile': profile,
            'user': user,
            'completed_lessons': completed_count,
            'total_lessons': total_lessons,
            'completion_percentage': (completed_count / total_lessons * 100) if total_lessons > 0 else 0,
            'quiz_attempts_count': quiz_attempts.count(),
            'avg_quiz_score': avg_quiz_score,
            'solved_challenges': solved_challenges,
            'total_submissions': submissions.count(),
            'badges': user.badges.all().select_related('badge'),
            'recent_activity': self.get_recent_activity(user)
        })
        
        return context
    
    def get_recent_activity(self, user):
        activities = []
        
        # Recent quiz attempts
        for attempt in QuizAttempt.objects.filter(user=user)[:5]:
            activities.append({
                'type': 'quiz',
                'title': f"Completed quiz: {attempt.quiz.title}",
                'score': f"{attempt.score:.1f}%",
                'xp': f"+{attempt.xp_earned} XP",
                'date': attempt.submitted_at
            })
        
        # Recent challenge submissions
        for submission in CodeSubmission.objects.filter(user=user)[:5]:
            activities.append({
                'type': 'challenge',
                'title': f"Attempted: {submission.challenge.title}",
                'status': submission.status,
                'xp': f"+{submission.challenge.xp_reward if submission.status == 'ACCEPTED' else 0} XP",
                'date': submission.created_at
            })
        
        # Sort by date
        activities.sort(key=lambda x: x['date'] if x['date'] else timezone.now(), reverse=True)
        return activities[:10]


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = "base/profile_edit.html"
    form_class = UserUpdateForm
    success_url = reverse_lazy('profile')
    
    def get_object(self):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_form'] = ProfileUpdateForm(instance=self.request.user.profile)
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        user_form = UserUpdateForm(request.POST, instance=self.object)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=self.object.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
        
        context = self.get_context_data()
        context['user_form'] = user_form
        context['profile_form'] = profile_form
        return self.render_to_response(context)


# ============================================
# REAL TIME / LIVE LEARNING VIEW
# ============================================

@login_required
def realtime_learning_view(request):
    """Live coding view - real-time code editor"""
    context = {
        'xp_progress': 0,
        'xp_for_next_level': 1000,
        'active_count': 23,
    }
    return render(request, 'base/realtime_learning.html', context)


# ============================================
# SEARCH VIEW
# ============================================

class SearchView(LoginRequiredMixin, TemplateView):
    template_name = "base/search_results.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', '').strip()
        
        if query:
            context['query'] = query
            context['lessons'] = Lesson.objects.filter(
                Q(title__icontains=query) | Q(theory_content__icontains=query)
            )[:10]
            context['challenges'] = Challenge.objects.filter(
                Q(title__icontains=query) | Q(problem_statement__icontains=query)
            )[:10]
            context['learning_paths'] = LearningPath.objects.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )[:10]
            context['total_results'] = (
                context['lessons'].count() + 
                context['challenges'].count() + 
                context['learning_paths'].count()
            )
        
        return context


# ============================================
# PUBLIC CHALLENGES & QUIZZES VIEWS (For Learners)
# ============================================

class PublicChallengeListView(ListView):
    """Public view for challenges - accessible to everyone"""
    model = Challenge
    template_name = "base/challenges.html"
    context_object_name = "challenges"
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Challenge.objects.filter(is_active=True)
        
        # Filter by language
        language = self.request.GET.get('language')
        if language:
            queryset = queryset.filter(language_id=language)
        
        # Filter by difficulty
        difficulty = self.request.GET.get('difficulty')
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        
        return queryset.select_related('language', 'created_by')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['languages'] = ProgrammingLanguage.objects.filter(is_active=True)
        context['difficulty_choices'] = Challenge.Difficulty.choices
        context['page_title'] = "Coding Challenges"
        return context


class PublicChallengeDetailView(DetailView):
    """Public view for single challenge - accessible to everyone"""
    model = Challenge
    template_name = "base/challenge_detail.html"
    context_object_name = "challenge"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        challenge = self.get_object()
        
        if self.request.user.is_authenticated:
            context['user_submission'] = CodeSubmission.objects.filter(
                user=self.request.user,
                challenge=challenge
            ).first()
        else:
            context['user_submission'] = None
        
        return context


@method_decorator(login_required, name='dispatch')
class SubmitChallengeView(View):
    """Handle challenge submissions - requires login"""
    template_name = "base/submit_challenge.html"
    
    def get(self, request, challenge_id):
        challenge = get_object_or_404(Challenge, id=challenge_id, is_active=True)
        return render(request, self.template_name, {'challenge': challenge})
    
    def post(self, request, challenge_id):
        challenge = get_object_or_404(Challenge, id=challenge_id, is_active=True)
        submitted_code = request.POST.get('code', '')
        
        # Create submission
        submission = CodeSubmission.objects.create(
            user=request.user,
            challenge=challenge,
            submitted_code=submitted_code,
            status='PENDING'
        )
        
        # Simple evaluation (in real app, you'd run against test cases)
        submission.status = 'ACCEPTED'
        submission.passed_test_cases = len(challenge.test_cases) if challenge.test_cases else 1
        submission.total_test_cases = len(challenge.test_cases) if challenge.test_cases else 1
        submission.score = 100
        submission.save()
        
        # Award XP
        request.user.total_xp += challenge.xp_reward
        request.user.save()
        
        messages.success(request, f'🎉 Challenge completed! +{challenge.xp_reward} XP')
        return redirect('challenge_detail', pk=challenge_id)


class PublicQuizListView(ListView):
    """Public view for quizzes - accessible to everyone"""
    model = Quiz
    template_name = "base/quizzes.html"
    context_object_name = "quizzes"
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Quiz.objects.filter(is_active=True).select_related('lesson', 'lesson__learning_path')
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lessons'] = Lesson.objects.filter(is_locked=False)
        context['page_title'] = "Quizzes"
        return context


# ============================================
# ALL QUIZZES VIEW (Shows all quizzes)
# ============================================

class AllQuizzesListView(ListView):
    """Show all quizzes in one page - accessible to everyone"""
    model = Quiz
    template_name = "base/all_quizzes.html"
    context_object_name = "quizzes"
    paginate_by = 20
    
    def get_queryset(self):
        return Quiz.objects.filter(is_active=True).select_related('lesson', 'lesson__learning_path').order_by('lesson__learning_path__title', 'title')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "All Quizzes"
        context['total_quizzes'] = self.get_queryset().count()
        return context


# ============================================
# SIMPLE VIEWS FOR DEBUGGING
# ============================================

@login_required
def lesson_detail_view(request, path_slug, lesson_slug):
    """Simple function-based view for lesson detail - requires login"""
    try:
        learning_path = get_object_or_404(LearningPath, slug=path_slug)
        lesson = get_object_or_404(Lesson, slug=lesson_slug, learning_path=learning_path)
        
        is_completed = False
        if request.user.is_authenticated:
            progress, _ = LearningProgress.objects.get_or_create(
                user=request.user,
                learning_path=learning_path
            )
            is_completed = progress.completed_lessons.filter(id=lesson.id).exists()
        
        next_lesson = Lesson.objects.filter(
            learning_path=learning_path,
            order__gt=lesson.order
        ).order_by('order').first()
        
        prev_lesson = Lesson.objects.filter(
            learning_path=learning_path,
            order__lt=lesson.order
        ).order_by('-order').first()
        
        context = {
            'lesson': lesson,
            'is_completed': is_completed,
            'next_lesson': next_lesson,
            'prev_lesson': prev_lesson,
            'quizzes': lesson.quizzes.filter(is_active=True),
        }
        
        return render(request, 'base/lesson_detail.html', context)
        
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)


def simple_course_view(request, slug):
    """Simple view to display course without any admin interference"""
    try:
        path = get_object_or_404(LearningPath, slug=slug, is_active=True)
        lessons = path.lessons.all().order_by('order')
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{path.title} - CodeQuest</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #0a0a2a; color: white; }}
                .container {{ max-width: 1000px; margin: 0 auto; }}
                .header {{ background: linear-gradient(135deg, #b026ff, #00e5ff); padding: 30px; border-radius: 20px; text-align: center; margin-bottom: 30px; }}
                .lesson {{ background: rgba(255,255,255,0.1); padding: 20px; margin: 10px 0; border-radius: 10px; display: flex; justify-content: space-between; align-items: center; }}
                .btn {{ background: #00e5ff; color: #0a0a2a; padding: 10px 20px; border-radius: 8px; text-decoration: none; font-weight: bold; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🐍 {path.title}</h1>
                    <p>{path.description}</p>
                </div>
                <h2>📋 Course Lessons ({lessons.count()})</h2>
        """
        
        for lesson in lessons:
            html += f"""
                <div class="lesson">
                    <div>
                        <strong>{lesson.order}. {lesson.title}</strong>
                        <div style="font-size: 12px; color: #ffd93d;">🎯 {lesson.xp_reward} XP</div>
                    </div>
                    <a href="/simple-lesson/{path.slug}/{lesson.slug}/" class="btn">Start Lesson →</a>
                </div>
            """
        
        if lessons.count() == 0:
            html += '<p>No lessons yet. Add some lessons!</p>'
        
        html += """
            </div>
        </body>
        </html>
        """
        
        return HttpResponse(html)
    except Exception as e:
        return HttpResponse(f"<h1>Course not found</h1><p>Error: {e}</p>", status=404)


def simple_lesson_view(request, path_slug, lesson_slug):
    """Simple view to display lesson without any admin interference"""
    try:
        path = get_object_or_404(LearningPath, slug=path_slug)
        lesson = get_object_or_404(Lesson, slug=lesson_slug, learning_path=path)
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{lesson.title} - CodeQuest</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #0a0a2a; color: white; }}
                .container {{ max-width: 900px; margin: 0 auto; }}
                .header {{ background: linear-gradient(135deg, #b026ff, #00e5ff); padding: 30px; border-radius: 20px; text-align: center; margin-bottom: 30px; }}
                .content {{ background: rgba(255,255,255,0.1); padding: 30px; border-radius: 20px; }}
                pre {{ background: #1a1a3a; padding: 15px; border-radius: 10px; overflow-x: auto; }}
                .back-btn {{ display: inline-block; margin-top: 20px; background: #00e5ff; color: #0a0a2a; padding: 10px 20px; border-radius: 8px; text-decoration: none; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>{lesson.title}</h1>
                    <p>🎯 {lesson.xp_reward} XP</p>
                </div>
                <div class="content">
                    {lesson.theory_content}
                    <h3>💻 Code Example</h3>
                    <pre><code>{lesson.example_code}</code></pre>
                    <a href="/simple-course/{path_slug}/" class="back-btn">← Back to Course</a>
                </div>
            </div>
        </body>
        </html>
        """
        
        return HttpResponse(html)
    except Exception as e:
        return HttpResponse(f"<h1>Lesson not found</h1><p>Error: {e}</p>", status=404)


# ============================================
# ADMIN CRUD VIEWS (Auto-generated - for staff only)
# ============================================

VIEW_CONFIGS = {
    "user": {
        "model": User,
        "form": UserRegistrationForm,
        "update_form": UserUpdateForm,
        "search": ("username", "email", "first_name", "last_name"),
        "filters": ("role", "is_verified", "is_active"),
    },
    "user_profile": {
        "model": UserProfile,
        "form": UserProfileForm,
        "mixins": (OwnedByRequestUserMixin,),
        "search": ("user__username", "bio", "learning_goal"),
        "filters": ("preferred_language",),
    },
    "programming_language": {
        "model": ProgrammingLanguage,
        "form": ProgrammingLanguageForm,
        "search": ("name", "slug", "description", "compiler_key"),
        "filters": ("is_active",),
    },
    "learning_path": {
        "model": LearningPath,
        "form": LearningPathForm,
        "search": ("title", "slug", "description", "language__name"),
        "filters": ("language", "difficulty", "is_active"),
    },
    "lesson": {
        "model": Lesson,
        "form": LessonForm,
        "search": ("title", "slug", "theory_content", "learning_path__title"),
        "filters": ("learning_path", "is_locked"),
    },
    "challenge": {
        "model": Challenge,
        "form": ChallengeForm,
        "mixins": (CreatedByRequestUserMixin,),
        "search": ("title", "slug", "problem_statement", "language__name"),
        "filters": ("language", "challenge_type", "difficulty", "is_active"),
    },
    "code_submission": {
        "model": CodeSubmission,
        "form": CodeSubmissionForm,
        "mixins": (OwnedByRequestUserMixin,),
        "search": ("challenge__title", "submitted_code", "status"),
        "filters": ("challenge", "status"),
    },
    "quiz": {
        "model": Quiz,
        "form": QuizForm,
        "search": ("title", "lesson__title"),
        "filters": ("lesson", "is_active"),
    },
    "quiz_question": {
        "model": QuizQuestion,
        "form": QuizQuestionForm,
        "search": ("question_text", "explanation", "quiz__title"),
        "filters": ("quiz",),
    },
    "quiz_choice": {
        "model": QuizChoice,
        "form": QuizChoiceForm,
        "search": ("choice_text", "question__question_text"),
        "filters": ("question", "is_correct"),
    },
    "quiz_attempt": {
        "model": QuizAttempt,
        "form": default_form_for(
            QuizAttempt,
            exclude=("user", "score", "xp_earned", "submitted_at"),
        ),
        "mixins": (OwnedByRequestUserMixin,),
        "search": ("user__username", "quiz__title"),
        "filters": ("quiz",),
    },
    "quiz_answer": {
        "model": QuizAnswer,
        "form": QuizAnswerForm,
        "search": ("question__question_text",),
        "filters": ("attempt", "question", "is_correct"),
    },
    "learning_progress": {
        "model": LearningProgress,
        "form": LearningProgressForm,
        "mixins": (OwnedByRequestUserMixin,),
        "search": ("user__username", "learning_path__title"),
        "filters": ("learning_path", "progress_percent"),
    },
    "badge": {
        "model": Badge,
        "form": BadgeForm,
        "search": ("name", "description"),
        "filters": (),
    },
    "user_badge": {
        "model": UserBadge,
        "form": UserBadgeForm,
        "search": ("user__username", "badge__name"),
        "filters": ("badge",),
    },
    "multiplayer_battle": {
        "model": MultiplayerBattle,
        "form": MultiplayerBattleForm,
        "search": ("challenge__title", "host__username", "status"),
        "filters": ("challenge", "host", "status"),
    },
    "battle_participant": {
        "model": BattleParticipant,
        "form": BattleParticipantForm,
        "search": ("battle__challenge__title", "user__username"),
        "filters": ("battle", "user", "rank"),
    },
    "ai_hint": {
        "model": AIHint,
        "form": default_form_for(AIHint, exclude=("user", "used_at")),
        "mixins": (OwnedByRequestUserMixin,),
        "search": ("challenge__title", "user__username", "hint_text"),
        "filters": ("challenge",),
    },
    "adaptive_difficulty_log": {
        "model": AdaptiveDifficultyLog,
        "form": default_form_for(AdaptiveDifficultyLog, exclude=("user",)),
        "mixins": (OwnedByRequestUserMixin,),
        "search": ("user__username", "reason"),
        "filters": ("previous_difficulty", "new_difficulty"),
    },
    "leaderboard_entry": {
        "model": LeaderboardEntry,
        "form": default_form_for(LeaderboardEntry, exclude=("total_points",)),
        "search": ("user__username",),
        "filters": ("period", "period_start", "period_end"),
    },
    "notification": {
        "model": Notification,
        "form": NotificationForm,
        "mixins": (RecipientRequestUserMixin,),
        "search": ("title", "message", "recipient__username"),
        "filters": ("notification_type", "is_read"),
    },
}


def build_crud_views(name, config):
    model = config["model"]
    form_class = config["form"]
    update_form_class = config.get("update_form", form_class)
    model_mixins = config.get("mixins", ())
    route_name = name.replace("_", "-")
    title = model._meta.verbose_name.title()

    list_view = type(
        f"{model.__name__}ListView",
        (LoginRequiredMixin, SearchFilterMixin, ListView),
        {
            "model": model,
            "paginate_by": 20,
            "search_fields": config.get("search", ()),
            "filter_fields": config.get("filters", ()),
            "template_name": "crud/list.html",
            "context_object_name": f"{name}_list",
            "extra_context": {
                "page_title": f"{title}s",
                "create_url_name": f"{route_name}-create",
                "detail_url_name": f"{route_name}-detail",
                "update_url_name": f"{route_name}-update",
                "delete_url_name": f"{route_name}-delete",
            },
        },
    )

    # ADMIN detail view - different name to avoid conflict with public view
    detail_view = type(
        f"Admin{model.__name__}DetailView",
        (LoginRequiredMixin, UserPassesTestMixin, DetailView),
        {
            "model": model,
            "template_name": "crud/detail.html",
            "context_object_name": name,
            "extra_context": {
                "page_title": title,
                "list_url_name": f"{route_name}-list",
                "update_url_name": f"{route_name}-update",
                "delete_url_name": f"{route_name}-delete",
            },
            "test_func": lambda self: self.request.user.is_staff,
        },
    )

    create_view = type(
        f"{model.__name__}CreateView",
        (LoginRequiredMixin, UserPassesTestMixin, *model_mixins, MessageMixin, CreateView),
        {
            "model": model,
            "form_class": form_class,
            "template_name": "crud/form.html",
            "success_url": reverse_lazy(f"{route_name}-list"),
            "success_message": f"{title} created successfully.",
            "extra_context": {
                "page_title": f"Create {title}",
                "list_url_name": f"{route_name}-list",
            },
            "test_func": lambda self: self.request.user.is_staff,
        },
    )

    update_view = type(
        f"{model.__name__}UpdateView",
        (LoginRequiredMixin, UserPassesTestMixin, *model_mixins, MessageMixin, UpdateView),
        {
            "model": model,
            "form_class": update_form_class,
            "template_name": "crud/form.html",
            "success_url": reverse_lazy(f"{route_name}-list"),
            "success_message": f"{title} updated successfully.",
            "extra_context": {
                "page_title": f"Update {title}",
                "list_url_name": f"{route_name}-list",
            },
            "test_func": lambda self: self.request.user.is_staff,
        },
    )

    delete_view = type(
        f"{model.__name__}DeleteView",
        (LoginRequiredMixin, UserPassesTestMixin, DeleteMessageMixin, DeleteView),
        {
            "model": model,
            "template_name": "crud/confirm_delete.html",
            "success_url": reverse_lazy(f"{route_name}-list"),
            "delete_message": f"{title} deleted successfully.",
            "extra_context": {
                "page_title": f"Delete {title}",
                "list_url_name": f"{route_name}-list",
            },
            "test_func": lambda self: self.request.user.is_staff,
        },
    )

    return list_view, detail_view, create_view, update_view, delete_view


for view_name, view_config in VIEW_CONFIGS.items():
    list_cls, detail_cls, create_cls, update_cls, delete_cls = build_crud_views(
        view_name,
        view_config,
    )
    class_prefix = "".join(part.title() for part in view_name.split("_"))
    globals()[f"{class_prefix}ListView"] = list_cls
    globals()[f"Admin{class_prefix}DetailView"] = detail_cls  # Renamed with Admin prefix
    globals()[f"{class_prefix}CreateView"] = create_cls
    globals()[f"{class_prefix}UpdateView"] = update_cls
    globals()[f"{class_prefix}DeleteView"] = delete_cls


# ============================================
# DRF VIEWSETS
# ============================================

if DRF_AVAILABLE:

    class BaseModelViewSet(viewsets.ModelViewSet):
        permission_classes = (permissions.IsAuthenticated,)
        search_fields = ()
        filterset_fields = ()
        ordering_fields = ("created_at", "updated_at")
        ordering = ("-created_at",)
        filter_backends = (
            DjangoFilterBackend,
            filters.SearchFilter,
            filters.OrderingFilter,
        )

        def perform_create(self, serializer):
            model_fields = {field.name for field in serializer.Meta.model._meta.fields}

            if "user" in model_fields and "user" not in serializer.validated_data:
                serializer.save(user=self.request.user)
            elif "created_by" in model_fields and "created_by" not in serializer.validated_data:
                serializer.save(created_by=self.request.user)
            elif "host" in model_fields and "host" not in serializer.validated_data:
                serializer.save(host=self.request.user)
            elif "recipient" in model_fields and "recipient" not in serializer.validated_data:
                serializer.save(recipient=self.request.user)
            else:
                serializer.save()


    API_CONFIGS = {
        "UserViewSet": {
            "queryset": User.objects.all(),
            "serializer_class": UserPublicSerializer,
            "search_fields": ("username", "email", "first_name", "last_name"),
            "filterset_fields": ("role", "is_verified", "is_active"),
        },
        "UserProfileViewSet": {
            "queryset": UserProfile.objects.select_related("user", "preferred_language"),
            "serializer_class": UserProfileSerializer,
            "search_fields": ("user__username", "bio", "learning_goal"),
            "filterset_fields": ("preferred_language",),
        },
        "ProgrammingLanguageViewSet": {
            "queryset": ProgrammingLanguage.objects.all(),
            "serializer_class": ProgrammingLanguageSerializer,
            "search_fields": ("name", "slug", "description", "compiler_key"),
            "filterset_fields": ("is_active",),
        },
        "LearningPathViewSet": {
            "queryset": LearningPath.objects.select_related("language"),
            "serializer_class": LearningPathSerializer,
            "search_fields": ("title", "slug", "description", "language__name"),
            "filterset_fields": ("language", "difficulty", "is_active"),
        },
        "LessonViewSet": {
            "queryset": Lesson.objects.select_related("learning_path", "learning_path__language"),
            "serializer_class": LessonSerializer,
            "search_fields": ("title", "slug", "theory_content", "learning_path__title"),
            "filterset_fields": ("learning_path", "is_locked"),
        },
        "ChallengeViewSet": {
            "queryset": Challenge.objects.select_related("lesson", "language", "created_by"),
            "serializer_class": ChallengeSerializer,
            "search_fields": ("title", "slug", "problem_statement", "language__name"),
            "filterset_fields": ("language", "challenge_type", "difficulty", "is_active"),
        },
        "CodeSubmissionViewSet": {
            "queryset": CodeSubmission.objects.select_related("user", "challenge"),
            "serializer_class": CodeSubmissionSerializer,
            "search_fields": ("challenge__title", "submitted_code", "status"),
            "filterset_fields": ("challenge", "status"),
        },
        "QuizViewSet": {
            "queryset": Quiz.objects.select_related("lesson").prefetch_related("questions"),
            "serializer_class": QuizSerializer,
            "search_fields": ("title", "lesson__title"),
            "filterset_fields": ("lesson", "is_active"),
        },
        "QuizQuestionViewSet": {
            "queryset": QuizQuestion.objects.select_related("quiz").prefetch_related("choices"),
            "serializer_class": QuizQuestionSerializer,
            "search_fields": ("question_text", "explanation", "quiz__title"),
            "filterset_fields": ("quiz",),
        },
        "QuizChoiceViewSet": {
            "queryset": QuizChoice.objects.select_related("question"),
            "serializer_class": QuizChoiceSerializer,
            "search_fields": ("choice_text", "question__question_text"),
            "filterset_fields": ("question", "is_correct"),
        },
        "QuizAttemptViewSet": {
            "queryset": QuizAttempt.objects.select_related("user", "quiz"),
            "serializer_class": QuizAttemptSerializer,
            "search_fields": ("user__username", "quiz__title"),
            "filterset_fields": ("quiz",),
        },
        "QuizAnswerViewSet": {
            "queryset": QuizAnswer.objects.select_related("attempt", "question", "selected_choice"),
            "serializer_class": QuizAnswerSerializer,
            "search_fields": ("question__question_text",),
            "filterset_fields": ("attempt", "question", "is_correct"),
        },
        "LearningProgressViewSet": {
            "queryset": LearningProgress.objects.select_related("user", "learning_path").prefetch_related("completed_lessons"),
            "serializer_class": LearningProgressSerializer,
            "search_fields": ("user__username", "learning_path__title"),
            "filterset_fields": ("learning_path", "progress_percent"),
        },
        "BadgeViewSet": {
            "queryset": Badge.objects.all(),
            "serializer_class": BadgeSerializer,
            "search_fields": ("name", "description"),
            "filterset_fields": (),
        },
        "UserBadgeViewSet": {
            "queryset": UserBadge.objects.select_related("user", "badge"),
            "serializer_class": UserBadgeSerializer,
            "search_fields": ("user__username", "badge__name"),
            "filterset_fields": ("badge",),
        },
        "MultiplayerBattleViewSet": {
            "queryset": MultiplayerBattle.objects.select_related("challenge", "host").prefetch_related("participants"),
            "serializer_class": MultiplayerBattleSerializer,
            "search_fields": ("challenge__title", "host__username", "status"),
            "filterset_fields": ("challenge", "host", "status"),
        },
        "BattleParticipantViewSet": {
            "queryset": BattleParticipant.objects.select_related("battle", "user", "submission"),
            "serializer_class": BattleParticipantSerializer,
            "search_fields": ("battle__challenge__title", "user__username"),
            "filterset_fields": ("battle", "user", "rank"),
        },
        "AIHintViewSet": {
            "queryset": AIHint.objects.select_related("challenge", "user"),
            "serializer_class": AIHintSerializer,
            "search_fields": ("challenge__title", "user__username", "hint_text"),
            "filterset_fields": ("challenge",),
        },
        "AdaptiveDifficultyLogViewSet": {
            "queryset": AdaptiveDifficultyLog.objects.select_related("user"),
            "serializer_class": AdaptiveDifficultyLogSerializer,
            "search_fields": ("user__username", "reason"),
            "filterset_fields": ("previous_difficulty", "new_difficulty"),
        },
        "LeaderboardEntryViewSet": {
            "queryset": LeaderboardEntry.objects.select_related("user"),
            "serializer_class": LeaderboardEntrySerializer,
            "search_fields": ("user__username",),
            "filterset_fields": ("period", "period_start", "period_end"),
        },
        "NotificationViewSet": {
            "queryset": Notification.objects.select_related("recipient"),
            "serializer_class": NotificationSerializer,
            "search_fields": ("title", "message", "recipient__username"),
            "filterset_fields": ("notification_type", "is_read"),
        },
    }

    for api_view_name, api_config in API_CONFIGS.items():
        globals()[api_view_name] = type(api_view_name, (BaseModelViewSet,), api_config)