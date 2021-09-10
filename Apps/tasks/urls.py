from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.tasks.views import TaskViewSet, UserListView, TaskItemView, TaskSearchView, TaskItemLogsView
from apps.users.views import UserLogtimeView

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='tasks')

urlpatterns = [
                  path('users/', UserListView.as_view(), name='users-list'),
                  path('tasks/search/', TaskSearchView.as_view(), name='task-search'),
                  path('user/logtime/', UserLogtimeView.as_view(), name='user_logtime'),
                  path('tasks/<int:pk>/comments/', TaskItemView.as_view(), name='task-comments'),
                  path('tasks/<int:pk>/logs/', TaskItemLogsView.as_view(), name='task-logs'),
              ] + router.urls
