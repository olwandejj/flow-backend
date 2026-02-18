from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from reports.views import dashboard_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/reports/', include('reports.urls')), # Link our new app
    path('dashboard/', dashboard_view, name='dashboard'),
]

# This allows us to serve the uploaded images during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)