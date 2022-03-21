from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from analysis.views import top, sample

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', top, name='top'),
    path('<int:num>/', top, name='top'),
    path('sample', sample, name='sample'),
    path('analysis/', include('analysis.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
