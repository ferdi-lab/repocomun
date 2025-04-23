from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('check/', views.check_urls, name='check_urls'),
    path('done/<int:pk>/', views.mark_done, name='mark_done'),
]
