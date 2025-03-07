from django.contrib import admin
from django.urls import path, include
from django.conf import settings  # Import the settings module
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),


    path('', include('apps.authen.urls')),
    path('chat/', include('apps.chat.urls')), 
    
    
    path('patient/', include('apps.patient.urls')),
    
    path('doctor/', include('apps.doctor.urls') ),




]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)