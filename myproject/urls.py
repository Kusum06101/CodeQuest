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
    SECRET_KEY = "kushi_rishu_060910"  # Change this to something random
    if request.GET.get('key') != SECRET_KEY:
        return HttpResponse("Access denied. Invalid key.", status=403)
    
    from base.models import LearningPath
    before = LearningPath.objects.count()
    
    try:
        call_command('loaddata', 'complete_data.json', verbosity=2)
        after = LearningPath.objects.count()
        return HttpResponse(f"""
        <html>
        <body style="font-family: Arial; padding: 20px;">
            <h1>✅ Data Load Complete</h1>
            <p>Courses before: {before}</p>
            <p>Courses after: {after}</p>
            <p>Added: {after - before} courses</p>
            <a href="/learn/">View courses →</a>
        </body>
        </html>
        """)
    except Exception as e:
        return HttpResponse(f"Error: {e}", status=500)

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