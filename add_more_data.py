import os
import django
import random
from faker import Faker

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from base.models import (
    LearningPath, Lesson, Challenge, Quiz, QuizQuestion, QuizChoice,
    User, UserProfile, Badge, UserBadge, LearningProgress
)
from django.contrib.auth.hashers import make_password
from django.utils import timezone

fake = Faker()

print("=" * 60)
print("ADDING MORE DATA TO CODEQUEST")
print("=" * 60)

# ============================================
# 1. ADD QUIZZES TO ALL COURSES
# ============================================
print("\n📝 Adding quizzes to courses...")

courses = LearningPath.objects.all()
quizzes_added = 0

for course in courses:
    # Get first lesson of the course
    first_lesson = course.lessons.first()
    if not first_lesson:
        print(f"  ⏭️  {course.title[:40]} - no lessons found, skipping")
        continue
    
    # Check if course already has quizzes
    if Quiz.objects.filter(lesson__learning_path=course).count() > 0:
        print(f"  ⏭️  {course.title[:40]} - already has quizzes")
        continue
    
    # Create 2 quizzes per course
    for i in range(2):
        quiz_title = f"{course.title} Quiz {i+1}"
        
        quiz = Quiz.objects.create(
            title=quiz_title[:200],
            lesson=first_lesson,
            passing_score=70,
            xp_reward=50 + (i * 25),
            is_active=True
        )
        
        # Add questions
        questions = [
            f"What is the main focus of {course.title}?",
            f"Which skill is most important in {course.title}?",
            f"What will you learn in {course.title}?"
        ]
        
        for j, q_text in enumerate(questions[:3]):
            question = QuizQuestion.objects.create(
                quiz=quiz,
                question_text=q_text,
                order=j + 1
            )
            
            # Add choices
            QuizChoice.objects.create(question=question, choice_text="Correct answer", is_correct=True)
            QuizChoice.objects.create(question=question, choice_text="Wrong answer", is_correct=False)
            QuizChoice.objects.create(question=question, choice_text="Another wrong answer", is_correct=False)
        
        quizzes_added += 1
        print(f"  ✅ Added quiz: {quiz_title[:50]}")

print(f"  Total quizzes added: {quizzes_added}")

# ============================================
# 2. ADD MORE LESSONS TO COURSES
# ============================================
print("\n📚 Adding more lessons to courses...")

lessons_added = 0

for course in courses:
    current_lesson_count = course.lessons.count()
    
    # Add lessons only if less than 8
    if current_lesson_count < 8:
        needed = 8 - current_lesson_count
        
        for i in range(needed):
            lesson_num = current_lesson_count + i + 1
            lesson_title = f"{course.title} - Topic {lesson_num}"
            lesson_slug = f"{course.slug}-topic-{lesson_num}"
            
            lesson, created = Lesson.objects.get_or_create(
                slug=lesson_slug,
                learning_path=course,
                defaults={
                    "title": lesson_title[:200],
                    "theory_content": f"""
                    <h2>{lesson_title}</h2>
                    <p>This lesson covers important concepts in {course.title}.</p>
                    <p>You will learn practical skills and best practices.</p>
                    <h3>Key Takeaways:</h3>
                    <ul>
                        <li>Master core concepts</li>
                        <li>Build real-world projects</li>
                        <li>Prepare for certification</li>
                    </ul>
                    """,
                    "example_code": f"# Example code for {course.title}\nprint('Learning {course.title}')",
                    "order": lesson_num,
                    "xp_reward": 25 + (lesson_num * 5),
                    "is_locked": False
                }
            )
            if created:
                lessons_added += 1
                print(f"  ✅ Added lesson: {lesson_title[:50]}")

print(f"  Total lessons added: {lessons_added}")

# ============================================
# 3. ADD COURSE-SPECIFIC CHALLENGES
# ============================================
print("\n💻 Adding course-specific challenges...")

challenges_added = 0

for course in courses:
    # Get all lessons in this course
    course_lessons = course.lessons.all()
    if not course_lessons:
        continue
    
    # Count existing challenges for this course (through lessons)
    existing_count = Challenge.objects.filter(lesson__in=course_lessons).count()
    
    # Add 3 challenges per course if less than 3
    if existing_count < 3:
        needed = 3 - existing_count
        
        for i in range(needed):
            # Pick a random lesson from the course
            target_lesson = random.choice(course_lessons)
            
            challenge_title = f"{course.title} Challenge {existing_count + i + 1}"
            challenge_slug = f"{course.slug}-challenge-{existing_count + i + 1}"
            
            challenge, created = Challenge.objects.get_or_create(
                slug=challenge_slug,
                defaults={
                    "title": challenge_title[:200],
                    "problem_statement": f"""
                    <h2>{challenge_title}</h2>
                    <p>Complete this challenge to test your {course.title} skills!</p>
                    <h3>Task:</h3>
                    <p>Write a program that demonstrates your understanding of {course.title}.</p>
                    <h3>Requirements:</h3>
                    <ul>
                        <li>Use proper syntax</li>
                        <li>Handle edge cases</li>
                        <li>Write clean, readable code</li>
                    </ul>
                    """,
                    "language": course.language,
                    "lesson": target_lesson,
                    "difficulty": random.choice(['EASY', 'MEDIUM', 'HARD']),
                    "xp_reward": 50 + (i * 25),
                    "is_active": True
                }
            )
            if created:
                challenges_added += 1
                print(f"  ✅ Added challenge: {challenge_title[:50]}")

print(f"  Total challenges added: {challenges_added}")

# ============================================
# 4. CREATE 20 DUMMY USERS
# ============================================
print("\n👥 Creating dummy users...")

users_created = 0
existing_users = User.objects.count()
print(f"  Existing users: {existing_users}")

# Get badges for assignment
badges = Badge.objects.all()

for i in range(20):
    username = f"coder_{fake.user_name()}{random.randint(1, 999)}"
    email = f"{username}@codequest.com"
    
    # Check if user already exists
    if User.objects.filter(username=username).exists():
        continue
    
    user = User.objects.create(
        username=username[:150],
        email=email,
        password=make_password('password123'),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        total_xp=random.randint(0, 5000),
        current_level=random.randint(1, 10),
        is_active=True
    )
    
    # Create user profile
    profile, _ = UserProfile.objects.get_or_create(
        user=user,
        defaults={
            "bio": fake.sentence(),
            "learning_goal": random.choice(['Master Python', 'Web Development', 'Data Science', 'Game Dev', 'Mobile Apps']),
        }
    )
    
    # Assign random badges
    for badge in random.sample(list(badges), min(3, badges.count())):
        UserBadge.objects.get_or_create(
            user=user,
            badge=badge,
            defaults={"awarded_at": timezone.now()}
        )
    
    # Assign random course progress
    for course in random.sample(list(courses), min(5, courses.count())):
        progress, _ = LearningProgress.objects.get_or_create(
            user=user,
            learning_path=course,
            defaults={
                "progress_percent": random.randint(0, 100),
                "completed_at": timezone.now() if random.choice([True, False]) else None
            }
        )
        
        # Add random completed lessons
        for lesson in course.lessons.all()[:random.randint(1, 5)]:
            progress.completed_lessons.add(lesson)
    
    users_created += 1
    print(f"  ✅ Created user: {username} (Level {user.current_level}, {user.total_xp} XP)")

print(f"  Total users created: {users_created}")
print(f"  Total users now: {User.objects.count()}")

# ============================================
# SUMMARY
# ============================================
print("\n" + "=" * 60)
print("📊 FINAL SUMMARY")
print("=" * 60)
print(f"  Courses: {LearningPath.objects.count()}")
print(f"  Lessons: {Lesson.objects.count()}")
print(f"  Challenges: {Challenge.objects.count()}")
print(f"  Quizzes: {Quiz.objects.count()}")
print(f"  Users: {User.objects.count()}")
print(f"  Badges: {Badge.objects.count()}")
print("=" * 60)
print("✅ All data added successfully!")