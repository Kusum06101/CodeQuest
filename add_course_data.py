# add_course_data.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from base.models import ProgrammingLanguage, LearningPath, Lesson, Quiz, QuizQuestion, QuizChoice, Badge

print("=" * 60)
print("ADDING COURSE DATA VIA SCRIPT")
print("=" * 60)

# 1. ADD PROGRAMMING LANGUAGES
print("\n1. Adding Programming Languages...")

languages = [
    {"name": "Python", "slug": "python", "version": "3.12", "compiler_key": "python3", 
     "description": "Python is a high-level, interpreted programming language known for its simplicity and readability."},
    {"name": "JavaScript", "slug": "javascript", "version": "ES2024", "compiler_key": "node", 
     "description": "JavaScript is the programming language of the web."},
    {"name": "Java", "slug": "java", "version": "21 LTS", "compiler_key": "javac", 
     "description": "Java is a class-based, object-oriented programming language."},
]

for lang in languages:
    obj, created = ProgrammingLanguage.objects.get_or_create(name=lang["name"], defaults=lang)
    print(f"  {'Created' if created else 'Exists'}: {lang['name']}")

# 2. CREATE LEARNING PATHS
print("\n2. Creating Learning Paths...")

python = ProgrammingLanguage.objects.get(name="Python")
javascript = ProgrammingLanguage.objects.get(name="JavaScript")
java = ProgrammingLanguage.objects.get(name="Java")

paths = [
    {"language": python, "title": "Python Programming Fundamentals", "slug": "python-fundamentals", 
     "description": "Master Python programming from scratch.", "difficulty": "BEGINNER", "estimated_hours": 40},
    {"language": javascript, "title": "JavaScript Essentials", "slug": "javascript-essentials", 
     "description": "Learn JavaScript from basics to advanced.", "difficulty": "BEGINNER", "estimated_hours": 35},
    {"language": java, "title": "Java Programming Basics", "slug": "java-basics", 
     "description": "Start your Java journey with fundamentals.", "difficulty": "BEGINNER", "estimated_hours": 45},
]

created_paths = []
for path_data in paths:
    path, created = LearningPath.objects.get_or_create(
        language=path_data["language"],
        title=path_data["title"],
        defaults=path_data
    )
    created_paths.append(path)
    print(f"  {'Created' if created else 'Exists'}: {path.title}")

# 3. ADD LESSONS FOR PYTHON
print("\n3. Adding Python Lessons...")

python_path = LearningPath.objects.filter(language__name="Python").first()
if python_path:
    lessons = [
        {"title": "Introduction to Python", "order": 1, "xp": 50, "is_locked": False,
         "theory": "<h1>Welcome to Python!</h1><p>Python is a powerful programming language.</p><h2>Your First Program</h2><pre><code>print('Hello, World!')</code></pre>",
         "example": "print('Hello, World!')\nprint('Welcome to Python!')"},
        {"title": "Variables and Data Types", "order": 2, "xp": 60, "is_locked": True,
         "theory": "<h1>Variables</h1><p>Variables store data.</p><pre><code>name = 'Alice'\nage = 25</code></pre>",
         "example": "name = input('Enter name: ')\nprint(f'Hello, {name}!')"},
        {"title": "Control Flow: If-Else", "order": 3, "xp": 70, "is_locked": True,
         "theory": "<h1>If-Else Statements</h1><p>Make decisions in your code.</p><pre><code>if age >= 18:\n    print('Adult')</code></pre>",
         "example": "age = int(input('Enter age: '))\nif age >= 18:\n    print('Adult')\nelse:\n    print('Minor')"},
    ]
    
    for lesson_data in lessons:
        lesson, created = Lesson.objects.get_or_create(
            learning_path=python_path,
            order=lesson_data["order"],
            defaults={
                "title": lesson_data["title"],
                "slug": f"{python_path.slug}-lesson-{lesson_data['order']}",
                "theory_content": lesson_data["theory"],
                "example_code": lesson_data["example"],
                "xp_reward": lesson_data["xp"],
                "is_locked": lesson_data["is_locked"]
            }
        )
        print(f"  {'Created' if created else 'Exists'}: {lesson.title}")

# 4. ADD QUIZZES
print("\n4. Adding Quizzes...")

for path in created_paths:
    for lesson in path.lessons.all()[:2]:
        quiz, created = Quiz.objects.get_or_create(
            lesson=lesson,
            title=f"Quiz: {lesson.title[:40]}",
            defaults={"time_limit_minutes": 10, "xp_reward": lesson.xp_reward // 2, "is_active": True}
        )
        if created:
            print(f"  Created quiz for: {lesson.title}")

# SUMMARY
print("\n" + "=" * 60)
print("COURSE DATA ADDED SUCCESSFULLY!")
print("=" * 60)
print(f"""
   Programming Languages: {ProgrammingLanguage.objects.count()}
   Learning Paths: {LearningPath.objects.count()}
   Lessons: {Lesson.objects.count()}
   Quizzes: {Quiz.objects.count()}

   Visit: http://127.0.0.1:8000/learn/
""")