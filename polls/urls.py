from django.urls import path
from .views import Home, TaskViewSet
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
urlpatterns = [
    # path("", views.index, name="index"),
    path('', Home.as_view()),
]

router.register(r'tasks', TaskViewSet, basename='tasks')
urlpatterns += router.urls