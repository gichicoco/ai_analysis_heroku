from django.urls import path

from analysis import views

urlpatterns = [
    path("new/", views.analysis_new, name="analysis_new"),
    path("<int:analysis_id>/", views.analysis_detail, name="analysis_detail"),
    path('delete/<int:analysis_id>', views.analysis_delete, name='analysis_delete'),
]
