from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='homepage'),
    path('moderator/', views.moderator, name='moderator'),
    path('display/', views.display, name='display'),
]