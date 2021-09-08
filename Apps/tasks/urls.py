from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.tasks.views import TaskViewSet, UserListView, TaskItemView, TaskSearchView, TaskItemLogsView

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='tasks')

urlpatterns = router.urls

urlpatterns += [
    path('users/', UserListView.as_view(), name='users-list'),
    path('tasks/<int:pk>/comments/', TaskItemView.as_view(), name='task-comments'),
    path('tasks/<int:pk>/logs/', TaskItemLogsView.as_view(), name='task-logs'),
    path('tasks/search/', TaskSearchView.as_view(), name='task-search'),

]
