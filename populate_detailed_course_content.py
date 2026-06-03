# populate_detailed_course_content.py
# Run with: python manage.py shell < populate_detailed_course_content.py

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from base.models import LearningPath, Lesson, Quiz, QuizQuestion, QuizChoice

print("=" * 80)
print("ADDING DETAILED CONTENT TO ALL COURSES")
print("=" * 80)

# ============================================
# COURSE CONTENT DATABASE
# ============================================

course_contents = {
    "Python 101": {
        "difficulty": "BEGINNER",
        "lessons": [
            {
                "order": 1,
                "title": "Welcome to Python! Getting Started",
                "xp": 50,
                "theory": """
<h1>Welcome to Python Programming!</h1>

<p>Python is a powerful, easy-to-learn programming language that's perfect for beginners.</p>

<h2>What Makes Python Special?</h2>
<ul>
    <li>Readable Code: Python's syntax is clean and intuitive</li>
    <li>Versatile: Used in web development, data science, AI, automation</li>
    <li>Huge Community: Millions of developers worldwide</li>
</ul>

<h2>Your First Python Program</h2>
<pre><code>
print("Hello, World!")
print("Welcome to Python programming!")
</code></pre>

<h2>Practice Exercise</h2>
<p>Write a program that prints your name and your age.</p>
""",
                "example": 'print("=" * 40)\nprint("WELCOME TO PYTHON")\nprint("=" * 40)\n\nname = input("What is your name? ")\nage = input("How old are you? ")\n\nprint(f"Hello, {name}!")\nprint(f"You are {age} years old")'
            },
            {
                "order": 2,
                "title": "Variables and Data Types",
                "xp": 60,
                "theory": """
<h1>Variables and Data Types in Python</h1>

<p>Variables are containers for storing data values.</p>

<h2>Python Data Types</h2>
<ul>
    <li>int - Whole numbers: 25, -10, 1000</li>
    <li>float - Decimal numbers: 3.14, 2.5</li>
    <li>str - Text: "Hello", 'Python'</li>
    <li>bool - True/False values</li>
</ul>

<pre><code>
name = "Alice"
age = 25
height = 5.6
is_student = True
</code></pre>

<h2>Practice Exercise</h2>
<p>Create variables for your name, age, and height.</p>
""",
                "example": 'print("=" * 50)\nprint("USER PROFILE")\nprint("=" * 50)\n\nname = input("Enter your name: ")\nage = int(input("Enter your age: "))\nheight = float(input("Enter your height: "))\n\nprint(f"Name: {name}")\nprint(f"Age: {age}")\nprint(f"Height: {height}")'
            }
        ]
    }
}

# ============================================
# ADD CONTENT TO COURSES
# ============================================

print("\nAdding detailed content to courses...")

total_lessons_added = 0
total_quizzes_added = 0

for course_title, course_data in course_contents.items():
    try:
        path = LearningPath.objects.get(title=course_title)
        print(f"\nProcessing: {course_title}")
        
        lessons_added = 0
        for lesson_data in course_data["lessons"]:
            lesson, created = Lesson.objects.get_or_create(
                learning_path=path,
                order=lesson_data["order"],
                defaults={
                    "title": lesson_data["title"],
                    "slug": f"{path.slug}-lesson-{lesson_data['order']}",
                    "theory_content": lesson_data["theory"],
                    "example_code": lesson_data["example"],
                    "xp_reward": lesson_data["xp"],
                    "is_locked": lesson_data["order"] > 1
                }
            )
            if created:
                lessons_added += 1
                total_lessons_added += 1
                
                quiz = Quiz.objects.create(
                    lesson=lesson,
                    title=f"Quiz: {lesson.title[:40]}",
                    time_limit_minutes=10,
                    xp_reward=lesson.xp_reward // 2,
                    is_active=True
                )
                total_quizzes_added += 1
                
                for q_num in range(1, 4):
                    question = QuizQuestion.objects.create(
                        quiz=quiz,
                        question_text=f"Question {q_num}: What is a key concept from this lesson?",
                        explanation="Great job! Keep practicing!",
                        order=q_num
                    )
                    
                    for choice_idx in range(4):
                        QuizChoice.objects.create(
                            question=question,
                            choice_text=f"Option {chr(65+choice_idx)}",
                            is_correct=(choice_idx == 0)
                        )
        
        if lessons_added > 0:
            print(f"  Added {lessons_added} new lessons")
            
    except LearningPath.DoesNotExist:
        print(f"  Course not found: {course_title}")

# ============================================
# ADD GENERIC CONTENT TO REMAINING COURSES
# ============================================
print("\nAdding generic content to remaining courses...")

generic_lessons = [
    {
        "order": 1,
        "title": "Course Introduction",
        "xp": 50,
        "theory": """
<h1>Welcome to this Course!</h1>
<p>This course will teach you the fundamentals of programming.</p>

<h2>What You'll Learn</h2>
<ul>
    <li>Core concepts and fundamentals</li>
    <li>Practical applications</li>
    <li>Best practices</li>
</ul>

<h2>Your First Program</h2>
<pre><code>
print("Hello, World!")
print("Welcome to the course!")
</code></pre>

<h2>Practice Exercise</h2>
<p>Write a program that prints your name.</p>
""",
        "example": 'print("=" * 40)\nprint("WELCOME TO THE COURSE")\nprint("=" * 40)\n\nname = input("What is your name? ")\nprint(f"Hello, {name}! Let\'s start learning!")'
    },
    {
        "order": 2,
        "title": "Core Fundamentals",
        "xp": 60,
        "theory": """
<h1>Core Fundamentals</h1>
<p>This section covers the essential building blocks of programming.</p>

<h2>Key Concepts</h2>
<ul>
    <li>Variables and data storage</li>
    <li>Basic operations</li>
    <li>Control flow</li>
</ul>

<h2>Practice Exercise</h2>
<p>Create variables for your name and age.</p>
""",
        "example": 'name = "Student"\nage = 25\nprint(f"Name: {name}")\nprint(f"Age: {age}")'
    },
    {
        "order": 3,
        "title": "Working with Data",
        "xp": 70,
        "theory": """
<h1>Working with Data</h1>
<p>Learn how to store and organize data effectively.</p>

<h2>Data Structures</h2>
<ul>
    <li>Lists for ordered collections</li>
    <li>Dictionaries for key-value pairs</li>
</ul>

<h2>Practice Exercise</h2>
<p>Create a list of your favorite things.</p>
""",
        "example": 'favorites = ["Python", "coding", "learning"]\nprint("My favorites:", favorites)'
    }
]

all_paths = LearningPath.objects.filter(is_active=True)

for path in all_paths:
    if path.lessons.count() < 2:
        print(f"\nAdding generic content to: {path.title}")
        lessons_added = 0
        
        for lesson_data in generic_lessons:
            existing_lesson = path.lessons.filter(order=lesson_data["order"]).first()
            
            if not existing_lesson:
                lesson = Lesson.objects.create(
                    learning_path=path,
                    title=f"{lesson_data['title']} - {path.language.name}",
                    slug=f"{path.slug}-lesson-{lesson_data['order']}",
                    theory_content=lesson_data["theory"],
                    example_code=lesson_data["example"],
                    xp_reward=lesson_data["xp"],
                    order=lesson_data["order"],
                    is_locked=lesson_data["order"] > 1
                )
                lessons_added += 1
                total_lessons_added += 1
                
                quiz = Quiz.objects.create(
                    lesson=lesson,
                    title=f"Quiz: {lesson.title[:40]}",
                    time_limit_minutes=10,
                    xp_reward=lesson.xp_reward // 2,
                    is_active=True
                )
                total_quizzes_added += 1
                
                for q_num in range(1, 4):
                    question = QuizQuestion.objects.create(
                        quiz=quiz,
                        question_text=f"Question {q_num}: What is a key concept from this lesson?",
                        explanation="Great job! Keep practicing!",
                        order=q_num
                    )
                    
                    for choice_idx in range(4):
                        QuizChoice.objects.create(
                            question=question,
                            choice_text=f"Option {chr(65+choice_idx)}",
                            is_correct=(choice_idx == 0)
                        )
        
        if lessons_added > 0:
            print(f"  Added {lessons_added} generic lessons")

# ============================================
# FINAL SUMMARY
# ============================================
print("\n" + "=" * 80)
print("COURSE CONTENT ADDITION COMPLETE!")
print("=" * 80)
print(f"""
SUMMARY:
   Total Lessons Added: {total_lessons_added}
   Total Quizzes Added: {total_quizzes_added}
   Total Lessons Now: {Lesson.objects.count()}
   Total Quizzes Now: {Quiz.objects.count()}
""")

print("Visit: http://127.0.0.1:8000/learn/")