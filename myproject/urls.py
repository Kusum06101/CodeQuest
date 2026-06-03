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
        from base.models import LearningPath, ProgrammingLanguage
        
        # Show current counts
        initial_courses = LearningPath.objects.count()
        initial_langs = ProgrammingLanguage.objects.count()
        
        # Load the data - IGNORE existing records
        call_command('loaddata', 'complete_data.json', verbosity=2, ignorenonexistent=True)
        
        final_courses = LearningPath.objects.count()
        final_langs = ProgrammingLanguage.objects.count()
        
        response = f"""
        <html>
        <head><title>Data Load Complete</title></head>
        <body style="font-family: Arial; padding: 20px;">
            <h1>✅ Data Load Complete</h1>
            <h2>Courses:</h2>
            <p><strong>Before:</strong> {initial_courses}</p>
            <p><strong>After:</strong> {final_courses}</p>
            <p><strong>Added:</strong> {final_courses - initial_courses}</p>
            <h2>Languages:</h2>
            <p><strong>Before:</strong> {initial_langs}</p>
            <p><strong>After:</strong> {final_langs}</p>
            <p><strong>Added:</strong> {final_langs - initial_langs}</p>
            <hr>
            <p><a href="/learn/">View all courses →</a></p>
            <p><a href="/debug/count/">Check counts →</a></p>
        </body>
        </html>
        """
        return HttpResponse(response)
    except Exception as e:
        return HttpResponse(f"""
        <html>
        <head><title>Data Load Error</title></head>
        <body style="font-family: Arial; padding: 20px;">
            <h1>❌ Error Loading Data</h1>
            <pre>{str(e)}</pre>
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