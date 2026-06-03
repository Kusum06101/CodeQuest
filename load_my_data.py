import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from base.models import LearningPath, Lesson, Challenge

print("=" * 50)
print("LOADING DATA TO RENDER")
print("=" * 50)

# Check current counts
print(f"\nCurrent counts:")
print(f"  Courses: {LearningPath.objects.count()}")
print(f"  Lessons: {Lesson.objects.count()}")
print(f"  Challenges: {Challenge.objects.count()}")

# Load the data
print(f"\nLoading complete_data.json...")

try:
    from django.core.management import call_command
    call_command('loaddata', 'complete_data.json', verbosity=1)
    print("\n✅ Data loaded successfully!")
except Exception as e:
    print(f"\n❌ Error: {e}")

# Check new counts
print(f"\nNew counts:")
print(f"  Courses: {LearningPath.objects.count()}")
print(f"  Lessons: {Lesson.objects.count()}")
print(f"  Challenges: {Challenge.objects.count()}")

print("\n" + "=" * 50)