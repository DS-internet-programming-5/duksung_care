from django.contrib import admin
from django.urls import path
from django.conf.urls import include

from django.conf import settings
from django.conf.urls.static import static

# duksung_care/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('hospital/', include('hospitals.urls')),
    path('admin/', admin.site.urls),
    path('health_tips/', include('health_tips.urls')),
    path('', include('main.urls')),  # main 앱의 URL 매핑을 포함합니다.
    path('accounts/', include('accounts.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
