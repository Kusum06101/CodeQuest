# create_templates.py
import os

# Create templates directory
os.makedirs('templates/base', exist_ok=True)

# Template 1
learning_path_detail = """{% extends 'base/base.html' %}
{% load static %}

{% block title %}{{ path.title }} - CodeQuest{% endblock %}

{% block content %}
<div class="learning-path-container">
    <div class="path-header">
        <a href="{% url 'learning_paths' %}" class="back-link">← Back to Learning Paths</a>
        <h1>{{ path.title }}</h1>
        <p>{{ path.description }}</p>
        <div class="path-meta">
            <span class="language-badge">💻 {{ path.language.name }}</span>
            <span class="difficulty-badge {{ path.difficulty|lower }}">{{ path.get_difficulty_display }}</span>
            <span class="hours-badge">⏱️ {{ path.estimated_hours }} hours</span>
            <span class="lessons-count">📚 {{ total_lessons }} lessons</span>
        </div>
    </div>

    {% if user.is_authenticated and progress %}
    <div class="path-progress">
        <h3>Your Progress</h3>
        <div class="progress-container">
            <div class="progress-bar">
                <div class="progress-fill" style="width: {{ progress.progress_percent }}%"></div>
            </div>
            <span>{{ progress.progress_percent }}% Complete</span>
        </div>
    </div>
    {% endif %}

    <div class="lessons-list">
        <h2>📖 Lessons</h2>
        {% for lesson in lessons %}
        <div class="lesson-item {% if lesson.id in completed_lesson_ids %}completed{% endif %}">
            <div class="lesson-number">{{ forloop.counter }}</div>
            <div class="lesson-content">
                <h3>{{ lesson.title }}</h3>
                <p>🎯 {{ lesson.xp_reward }} XP</p>
            </div>
            <div class="lesson-actions">
                {% if lesson.id in completed_lesson_ids %}
                    <span class="completed-badge">✅ Completed</span>
                {% elif lesson.is_locked and not forloop.first %}
                    <span class="locked-badge">🔒 Locked</span>
                {% else %}
                    <a href="{% url 'lesson_detail' path.slug lesson.slug %}" class="button small">Start Lesson →</a>
                {% endif %}
            </div>
        </div>
        {% endfor %}
    </div>
</div>
{% endblock %}
"""

# Template 2
lesson_detail = """{% extends 'base/base.html' %}
{% load static %}

{% block title %}{{ lesson.title }} - CodeQuest{% endblock %}

{% block content %}
<div class="lesson-container">
    <div class="lesson-nav">
        <a href="{% url 'learning_path_detail' lesson.learning_path.slug %}" class="back-link">← Back to {{ lesson.learning_path.title }}</a>
        <div class="lesson-nav-buttons">
            {% if prev_lesson %}
            <a href="{% url 'lesson_detail' lesson.learning_path.slug prev_lesson.slug %}" class="button secondary">← Previous</a>
            {% endif %}
            {% if next_lesson and not next_lesson.is_locked %}
            <a href="{% url 'lesson_detail' lesson.learning_path.slug next_lesson.slug %}" class="button primary">Next →</a>
            {% endif %}
        </div>
    </div>

    <div class="lesson-header">
        <h1>{{ lesson.title }}</h1>
        <div class="lesson-meta">
            <span class="xp-badge">🎯 {{ lesson.xp_reward }} XP</span>
            {% if is_completed %}
            <span class="completed-badge">✅ Completed</span>
            {% endif %}
        </div>
    </div>

    <div class="lesson-theory">
        {{ lesson.theory_content|safe }}
    </div>

    {% if lesson.example_code %}
    <div class="lesson-example">
        <h3>💻 Example Code</h3>
        <pre><code>{{ lesson.example_code }}</code></pre>
    </div>
    {% endif %}

    {% if quizzes %}
    <div class="lesson-quizzes">
        <h3>📝 Test Your Knowledge</h3>
        {% for quiz in quizzes %}
        <div class="quiz-card">
            <h4>{{ quiz.title }}</h4>
            <p>⏱️ {{ quiz.time_limit_minutes }} min | 🎯 {{ quiz.xp_reward }} XP</p>
            <a href="{% url 'take_quiz' quiz.id %}" class="button primary">Take Quiz →</a>
        </div>
        {% endfor %}
    </div>
    {% endif %}

    {% if not is_completed and not lesson.is_locked %}
    <div class="complete-lesson">
        <form method="post" action="{% url 'complete_lesson' lesson.id %}">
            {% csrf_token %}
            <button type="submit" class="button success large">✅ Mark Complete (+{{ lesson.xp_reward }} XP)</button>
        </form>
    </div>
    {% endif %}
</div>
{% endblock %}
"""

# Template 3
take_quiz = """{% extends 'base/base.html' %}
{% load static %}

{% block title %}{{ quiz.title }} - CodeQuest{% endblock %}

{% block content %}
<div class="quiz-container">
    <div class="quiz-header">
        <h1>{{ quiz.title }}</h1>
        <div class="quiz-info">
            <span>⏱️ {{ time_limit_minutes }} minutes</span>
            <span>🎯 {{ quiz.xp_reward }} XP</span>
            <span>📝 {{ total_questions }} questions</span>
        </div>
    </div>

    <form method="post">
        {% csrf_token %}
        {% for question in questions %}
        <div class="question-card">
            <h3>Question {{ forloop.counter }}</h3>
            <div class="question-text">{{ question.question_text|safe }}</div>
            <div class="choices">
                {% for choice in question.choices.all %}
                <label class="choice-label">
                    <input type="radio" name="question_{{ question.id }}" value="{{ choice.id }}" required>
                    <span>{{ choice.choice_text }}</span>
                </label>
                {% endfor %}
            </div>
        </div>
        {% endfor %}
        <div class="quiz-actions">
            <button type="submit" class="button primary large">Submit Quiz →</button>
        </div>
    </form>
</div>
{% endblock %}
"""

# Template 4
quiz_result = """{% extends 'base/base.html' %}
{% load static %}

{% block title %}Quiz Results - CodeQuest{% endblock %}

{% block content %}
<div class="result-container">
    <div class="result-header {% if attempt.score >= 70 %}success{% else %}warning{% endif %}">
        <h1>📝 Quiz Results</h1>
        <div class="score-circle"><div class="score-value">{{ attempt.score|floatformat:0 }}%</div></div>
        <div class="score-details">
            <p>🎯 Score: {{ attempt.score|floatformat:1 }}%</p>
            <p>⭐ XP Earned: +{{ attempt.xp_earned }} XP</p>
        </div>
    </div>

    <div class="questions-review">
        <h2>📋 Question Review</h2>
        {% for answer in answers %}
        <div class="review-card {% if answer.is_correct %}correct{% else %}incorrect{% endif %}">
            <div class="review-header">
                <span>Question {{ forloop.counter }}</span>
                <span>{% if answer.is_correct %}✅ Correct{% else %}❌ Incorrect{% endif %}</span>
            </div>
            <div class="question-text">{{ answer.question.question_text|safe }}</div>
            <div class="your-answer"><strong>Your Answer:</strong> {{ answer.selected_choice.choice_text|default:"Not answered" }}</div>
            {% if not answer.is_correct %}
            <div class="correct-answer"><strong>Correct Answer:</strong> 
                {% for choice in answer.question.choices.all %}{% if choice.is_correct %}{{ choice.choice_text }}{% endif %}{% endfor %}
            </div>
            {% endif %}
        </div>
        {% endfor %}
    </div>

    <div class="result-actions">
        <a href="{% url 'lesson_detail' attempt.quiz.lesson.learning_path.slug attempt.quiz.lesson.slug %}" class="button primary">📚 Back to Lesson</a>
        <a href="{% url 'learning_paths' %}" class="button secondary">🎯 More Paths</a>
    </div>
</div>
{% endblock %}
"""

# Write all files
with open('templates/base/learning_path_detail.html', 'w', encoding='utf-8') as f:
    f.write(learning_path_detail)
print("✅ Created: templates/base/learning_path_detail.html")

with open('templates/base/lesson_detail.html', 'w', encoding='utf-8') as f:
    f.write(lesson_detail)
print("✅ Created: templates/base/lesson_detail.html")

with open('templates/base/take_quiz.html', 'w', encoding='utf-8') as f:
    f.write(take_quiz)
print("✅ Created: templates/base/take_quiz.html")

with open('templates/base/quiz_result.html', 'w', encoding='utf-8') as f:
    f.write(quiz_result)
print("✅ Created: templates/base/quiz_result.html")

print("\n" + "="*50)
print("🎉 ALL TEMPLATES CREATED SUCCESSFULLY!")
print("="*50)