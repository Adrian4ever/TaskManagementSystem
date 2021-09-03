from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.tasks.views import TaskViewSet, UserListView

router = DefaultRouter()
router.register(r'task', TaskViewSet, basename='task')

urlpatterns = router.urls

urlpatterns += [
    path('users/', UserListView.as_view(), name='users_list'),
    #     path('user/', UserViewSet.as_view(), name='user_list'),
    #     # path('blog/<int:pk>/', BlogItemView.as_view(), name='blog_item'),
    #     # path('comment/', CommentsViewSet.as_view(), name='comment_list'),
    #
]
