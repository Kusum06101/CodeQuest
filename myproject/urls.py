"""
URL configuration for myproject project.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponse
from django.core.management import call_command

# Data loading view (temporary - remove after use)
def load_all_data(request):
    """Visit this URL to load all 47 courses into Render database"""
    # Secret key for security
    SECRET_KEY = "kushi_rishu_060910"
    
    # Only allow if secret key matches
    if request.GET.get('key') != SECRET_KEY:
        return HttpResponse("Access denied. Invalid or missing secret key.", status=403)
    
    try:
        from base.models import (
            LearningPath, Lesson, Challenge, ProgrammingLanguage, 
            Quiz, QuizQuestion, QuizChoice, CodeSubmission, 
            UserBadge, LearningProgress, QuizAttempt, QuizAnswer,
            Badge  # Add this
        )
        
        # Show current counts before deletion
        initial_courses = LearningPath.objects.count()
        initial_lessons = Lesson.objects.count()
        initial_challenges = Challenge.objects.count()
        initial_languages = ProgrammingLanguage.objects.count()
        initial_badges = Badge.objects.count()
        
        # Delete in correct order (child tables first, then parent tables)
        # This avoids foreign key constraint errors
        CodeSubmission.objects.all().delete()
        UserBadge.objects.all().delete()
        LearningProgress.objects.all().delete()
        QuizAnswer.objects.all().delete()
        QuizAttempt.objects.all().delete()
        QuizChoice.objects.all().delete()
        QuizQuestion.objects.all().delete()
        Quiz.objects.all().delete()
        Challenge.objects.all().delete()
        Lesson.objects.all().delete()
        LearningPath.objects.all().delete()
        Badge.objects.all().delete()  # Add this
        ProgrammingLanguage.objects.all().delete()
        
        # Load the data fresh
        call_command('loaddata', 'complete_data.json', verbosity=2)
        
        final_courses = LearningPath.objects.count()
        final_lessons = Lesson.objects.count()
        final_challenges = Challenge.objects.count()
        final_languages = ProgrammingLanguage.objects.count()
        final_badges = Badge.objects.count()
        
        response = f"""
        <html>
        <head><title>Data Load Complete</title></head>
        <body style="font-family: Arial; padding: 20px;">
            <h1>✅ Data Load Complete</h1>
            <h2>Courses:</h2>
            <p><strong>Before:</strong> {initial_courses}</p>
            <p><strong>After:</strong> {final_courses}</p>
            <h2>Lessons:</h2>
            <p><strong>Before:</strong> {initial_lessons}</p>
            <p><strong>After:</strong> {final_lessons}</p>
            <h2>Challenges:</h2>
            <p><strong>Before:</strong> {initial_challenges}</p>
            <p><strong>After:</strong> {final_challenges}</p>
            <h2>Languages:</h2>
            <p><strong>Before:</strong> {initial_languages}</p>
            <p><strong>After:</strong> {final_languages}</p>
            <h2>Badges:</h2>
            <p><strong>Before:</strong> {initial_badges}</p>
            <p><strong>After:</strong> {final_badges}</p>
            <hr>
            <p><a href="/learn/">View all courses →</a></p>
            <p><a href="/debug/count/">Check counts →</a></p>
        </body>
        </html>
        """
        return HttpResponse(response)
    except Exception as e:
        import traceback
        return HttpResponse(f"""
        <html>
        <head><title>Data Load Error</title></head>
        <body style="font-family: Arial; padding: 20px;">
            <h1>❌ Error Loading Data</h1>
            <pre>{str(e)}</pre>
            <pre>{traceback.format_exc()}</pre>
            <p><a href="/debug/count/">Check current counts →</a></p>
        </body>
        </html>
        """, status=500)

def debug_count(request):
    from base.models import LearningPath, Lesson, Challenge
    return HttpResponse(f"""
    <html>
    <body style="font-family: Arial; padding: 20px;">
        <h1>📊 Database Counts</h1>
        <p><strong>Courses:</strong> {LearningPath.objects.count()}</p>
        <p><strong>Lessons:</strong> {Lesson.objects.count()}</p>
        <p><strong>Challenges:</strong> {Challenge.objects.count()}</p>
        <a href="/learn/">View courses →</a>
    </body>
    </html>
    """)

urlpatterns = [
    # Temporary data loading URLs (remove after use)
    path("load-data/", load_all_data),
    path("debug/count/", debug_count),
    
    # Regular URLs
    path("admin/", admin.site.urls),
    path("", include("base.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)