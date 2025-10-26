from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/jobs/', include('apps.jobs.urls')),
    path('api/candidates/', include('apps.candidates.urls')),
    path('api/interviews/', include('apps.interviews.urls')),
    path('api/questions/', include('apps.questions.urls')),
    path('api/scoring/', include('apps.scoring.urls')),
    path('api/reports/', include('apps.reports.urls')),
    path('api/scheduling/', include('apps.scheduling.urls')),
    path('api/integrations/', include('apps.integrations.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
