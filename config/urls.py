from django.contrib import admin
from django.urls import path, include

from analysis.views import top

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', top, name='top'),
    path('<int:num>/', top, name='top'),
    path('analysis/', include('analysis.urls')),
]
