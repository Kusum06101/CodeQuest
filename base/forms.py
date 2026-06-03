from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AuthenticationForm
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import (
    Badge,
    BattleParticipant,
    Challenge,
    CodeSubmission,
    LearningPath,
    LearningProgress,
    Lesson,
    MultiplayerBattle,
    Notification,
    ProgrammingLanguage,
    Quiz,
    QuizAnswer,
    QuizChoice,
    QuizQuestion,
    User,
    UserBadge,
    UserProfile,
)


class UserRegistrationForm(UserCreationForm):
    """Enhanced user registration form with better UX"""
    
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your@email.com',
            'autocomplete': 'email'
        })
    )
    first_name = forms.CharField(
        required=True,
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First name'
        })
    )
    last_name = forms.CharField(
        required=True,
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last name'
        })
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username',
            'autocomplete': 'username'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'autocomplete': 'new-password'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm password',
            'autocomplete': 'new-password'
        })
    )
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "first_name", "last_name", "role")
        widgets = {
            'role': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field not in ['password1', 'password2']:
                self.fields[field].widget.attrs.update({'class': 'form-control'})
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('A user with this email already exists.')
        return email


class UserLoginForm(AuthenticationForm):
    """Custom login form with styling"""
    
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username or Email',
            'autocomplete': 'username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'autocomplete': 'current-password'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class UserUpdateForm(UserChangeForm):
    """Form for updating user information"""
    
    password = None
    
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "role", "profile_image", "is_verified")
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'profile_image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_verified': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != 'is_verified':
                self.fields[field].widget.attrs.update({'class': 'form-control'})


class UserProfileForm(forms.ModelForm):
    """Form for user profile with enhanced fields"""
    
    class Meta:
        model = UserProfile
        fields = ("bio", "preferred_language", "learning_goal", "daily_goal_minutes")
        widgets = {
            'bio': forms.Textarea(attrs={
                'rows': 4, 
                'class': 'form-control',
                'placeholder': 'Tell us about yourself and your programming journey...'
            }),
            'preferred_language': forms.Select(attrs={'class': 'form-control'}),
            'learning_goal': forms.Textarea(attrs={
                'rows': 3, 
                'class': 'form-control',
                'placeholder': 'What do you want to achieve? (e.g., "Become a full-stack developer")'
            }),
            'daily_goal_minutes': forms.NumberInput(attrs={
                'class': 'form-control', 
                'min': 5, 
                'max': 480,
                'placeholder': '30'
            }),
        }
    
    def clean_daily_goal_minutes(self):
        minutes = self.cleaned_data.get('daily_goal_minutes')
        if minutes < 5:
            raise forms.ValidationError('Daily goal must be at least 5 minutes.')
        if minutes > 480:
            raise forms.ValidationError('Daily goal cannot exceed 8 hours (480 minutes).')
        return minutes


class ProfileUpdateForm(forms.ModelForm):
    """Form for users to update their own profile"""
    
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    
    class Meta:
        model = UserProfile
        fields = ("bio", "preferred_language", "learning_goal", "daily_goal_minutes")
        widgets = {
            'bio': forms.Textarea(attrs={
                'rows': 4, 
                'class': 'form-control',
                'placeholder': 'Tell us about yourself...'
            }),
            'preferred_language': forms.Select(attrs={'class': 'form-control'}),
            'learning_goal': forms.Textarea(attrs={
                'rows': 3, 
                'class': 'form-control',
                'placeholder': 'What are your learning goals?'
            }),
            'daily_goal_minutes': forms.NumberInput(attrs={
                'class': 'form-control', 
                'min': 5, 
                'max': 480
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
    
    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            profile.save()
            # Update user fields
            user = profile.user
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']
            user.save()
        return profile


class ProgrammingLanguageForm(forms.ModelForm):
    class Meta:
        model = ProgrammingLanguage
        fields = ("name", "slug", "version", "compiler_key", "description", "icon", "is_active")
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'version': forms.TextInput(attrs={'class': 'form-control'}),
            'compiler_key': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'icon': forms.FileInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        if ProgrammingLanguage.objects.exclude(pk=self.instance.pk).filter(slug=slug).exists():
            raise forms.ValidationError('A language with this slug already exists.')
        return slug


class LearningPathForm(forms.ModelForm):
    class Meta:
        model = LearningPath
        fields = ("language", "title", "slug", "description", "difficulty", "estimated_hours", "is_active")
        widgets = {
            'language': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'difficulty': forms.Select(attrs={'class': 'form-control'}),
            'estimated_hours': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def clean_estimated_hours(self):
        hours = self.cleaned_data.get('estimated_hours')
        if hours < 0:
            raise forms.ValidationError('Estimated hours cannot be negative.')
        return hours


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ("learning_path", "title", "slug", "theory_content", "example_code", "xp_reward", "order", "is_locked")
        widgets = {
            'learning_path': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'theory_content': forms.Textarea(attrs={'rows': 20, 'class': 'form-control', 'id': 'theory-editor'}),
            'example_code': forms.Textarea(attrs={'rows': 10, 'class': 'form-control', 'id': 'code-editor'}),
            'xp_reward': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 500}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'is_locked': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def clean_xp_reward(self):
        xp = self.cleaned_data.get('xp_reward')
        if xp < 0:
            raise forms.ValidationError('XP reward cannot be negative.')
        if xp > 500:
            raise forms.ValidationError('XP reward cannot exceed 500.')
        return xp


class ChallengeForm(forms.ModelForm):
    class Meta:
        model = Challenge
        fields = (
            "lesson", "language", "title", "slug", "challenge_type", "difficulty",
            "problem_statement", "starter_code", "buggy_code", "expected_output",
            "test_cases", "constraints_text", "xp_reward", "time_limit_seconds",
            "memory_limit_mb", "is_active"
        )
        widgets = {
            'lesson': forms.Select(attrs={'class': 'form-control'}),
            'language': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'challenge_type': forms.Select(attrs={'class': 'form-control'}),
            'difficulty': forms.Select(attrs={'class': 'form-control'}),
            'problem_statement': forms.Textarea(attrs={'rows': 8, 'class': 'form-control'}),
            'starter_code': forms.Textarea(attrs={'rows': 10, 'class': 'form-control', 'id': 'starter-code-editor'}),
            'buggy_code': forms.Textarea(attrs={'rows': 10, 'class': 'form-control', 'id': 'buggy-code-editor'}),
            'expected_output': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'test_cases': forms.Textarea(attrs={'rows': 8, 'class': 'form-control', 'placeholder': '[{"input": "test", "expected": "output"}]'}),
            'constraints_text': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'xp_reward': forms.NumberInput(attrs={'class': 'form-control', 'min': 10, 'max': 500}),
            'time_limit_seconds': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 10}),
            'memory_limit_mb': forms.NumberInput(attrs={'class': 'form-control', 'min': 16, 'max': 1024}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def clean_test_cases(self):
        test_cases = self.cleaned_data.get('test_cases')
        if test_cases and isinstance(test_cases, str):
            try:
                import json
                test_cases = json.loads(test_cases)
            except json.JSONDecodeError:
                raise forms.ValidationError('Invalid JSON format for test cases.')
        return test_cases


class CodeSubmissionForm(forms.ModelForm):
    class Meta:
        model = CodeSubmission
        fields = ("challenge", "submitted_code")
        widgets = {
            'challenge': forms.HiddenInput(),
            'submitted_code': forms.Textarea(attrs={
                'rows': 16, 
                'spellcheck': 'false', 
                'autocomplete': 'off',
                'class': 'form-control',
                'id': 'code-submission-editor',
                'placeholder': 'Write your solution here...'
            }),
        }


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ("lesson", "title", "time_limit_minutes", "xp_reward", "is_active")
        widgets = {
            'lesson': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'time_limit_minutes': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 120}),
            'xp_reward': forms.NumberInput(attrs={'class': 'form-control', 'min': 10, 'max': 200}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class QuizQuestionForm(forms.ModelForm):
    class Meta:
        model = QuizQuestion
        fields = ("quiz", "question_text", "explanation", "order")
        widgets = {
            'quiz': forms.Select(attrs={'class': 'form-control'}),
            'question_text': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'explanation': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Explain why the answer is correct...'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }


class QuizChoiceForm(forms.ModelForm):
    class Meta:
        model = QuizChoice
        fields = ("question", "choice_text", "is_correct")
        widgets = {
            'question': forms.Select(attrs={'class': 'form-control'}),
            'choice_text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter choice text...'}),
            'is_correct': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class QuizAnswerForm(forms.ModelForm):
    """Form for submitting quiz answers"""
    
    class Meta:
        model = QuizAnswer
        fields = ("question", "selected_choice")
        widgets = {
            'question': forms.HiddenInput(),
            'selected_choice': forms.RadioSelect(attrs={'class': 'quiz-option'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        question = cleaned_data.get("question")
        selected_choice = cleaned_data.get("selected_choice")

        if selected_choice and question and selected_choice.question_id != question.id:
            raise forms.ValidationError("Selected choice must belong to the question.")

        return cleaned_data


class LearningProgressForm(forms.ModelForm):
    class Meta:
        model = LearningProgress
        fields = ("learning_path", "completed_lessons", "progress_percent", "completed_at")
        widgets = {
            'learning_path': forms.Select(attrs={'class': 'form-control'}),
            'completed_lessons': forms.SelectMultiple(attrs={'class': 'form-control', 'size': 10}),
            'progress_percent': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100}),
            'completed_at': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        learning_path = (
            self.cleaned_data.get("learning_path")
            if self.is_bound and hasattr(self, "cleaned_data")
            else self.initial.get("learning_path") or getattr(self.instance, "learning_path", None)
        )
        if learning_path:
            self.fields["completed_lessons"].queryset = Lesson.objects.filter(
                learning_path=learning_path
            )

    def clean(self):
        cleaned_data = super().clean()
        learning_path = cleaned_data.get("learning_path")
        completed_lessons = cleaned_data.get("completed_lessons")

        if learning_path and completed_lessons:
            invalid_lessons = completed_lessons.exclude(learning_path=learning_path)
            if invalid_lessons.exists():
                raise forms.ValidationError(
                    "Completed lessons must belong to the selected learning path."
                )
        
        # Auto-calculate progress percentage
        if learning_path and completed_lessons:
            total_lessons = learning_path.lessons.count()
            if total_lessons > 0:
                progress = int((completed_lessons.count() / total_lessons) * 100)
                cleaned_data['progress_percent'] = progress

        return cleaned_data


class BadgeForm(forms.ModelForm):
    class Meta:
        model = Badge
        fields = ("name", "description", "icon", "xp_required")
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'icon': forms.FileInput(attrs={'class': 'form-control'}),
            'xp_required': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }


class UserBadgeForm(forms.ModelForm):
    class Meta:
        model = UserBadge
        fields = ("user", "badge", "awarded_at")
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'badge': forms.Select(attrs={'class': 'form-control'}),
            'awarded_at': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }


class MultiplayerBattleForm(forms.ModelForm):
    class Meta:
        model = MultiplayerBattle
        fields = ("challenge", "host", "status", "started_at", "completed_at")
        widgets = {
            'challenge': forms.Select(attrs={'class': 'form-control'}),
            'host': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'started_at': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'completed_at': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }


class BattleParticipantForm(forms.ModelForm):
    class Meta:
        model = BattleParticipant
        fields = ("battle", "user", "submission", "score", "rank")
        widgets = {
            'battle': forms.Select(attrs={'class': 'form-control'}),
            'user': forms.Select(attrs={'class': 'form-control'}),
            'submission': forms.Select(attrs={'class': 'form-control'}),
            'score': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': 0, 'max': 100}),
            'rank': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }


class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ("recipient", "notification_type", "title", "message", "is_read", "metadata", "read_at")
        widgets = {
            'recipient': forms.Select(attrs={'class': 'form-control'}),
            'notification_type': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'is_read': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'metadata': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': '{"key": "value"}'}),
            'read_at': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }


# ============================================
# BONUS: Form for quiz taking (dynamic)
# ============================================

class QuizTakingForm(forms.Form):
    """Dynamic form for taking quizzes"""
    
    def __init__(self, quiz, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.quiz = quiz
        
        for question in quiz.questions.all().order_by('order'):
            choices = [(choice.id, choice.choice_text) for choice in question.choices.all()]
            self.fields[f'question_{question.id}'] = forms.ChoiceField(
                choices=choices,
                widget=forms.RadioSelect(attrs={'class': 'quiz-option'}),
                label=question.question_text,
                required=True,
                help_text=f"Question {question.order}"
            )
    
    def clean(self):
        cleaned_data = super().clean()
        # You can add custom validation here if needed
        return cleaned_data


# ============================================
# BONUS: Search Form
# ============================================

class SearchForm(forms.Form):
    """Global search form"""
    
    query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'search-input',
            'placeholder': 'Search lessons, challenges, paths...',
            'autocomplete': 'off'
        })
    )
    category = forms.ChoiceField(
        required=False,
        choices=[('', 'All'), ('lessons', 'Lessons'), ('challenges', 'Challenges'), ('paths', 'Learning Paths')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    difficulty = forms.ChoiceField(
        required=False,
        choices=[('', 'Any Difficulty'), ('BEGINNER', 'Beginner'), ('INTERMEDIATE', 'Intermediate'), ('ADVANCED', 'Advanced')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )