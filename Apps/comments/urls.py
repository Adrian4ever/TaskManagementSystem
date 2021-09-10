from rest_framework.routers import DefaultRouter

from apps.comments.views import CommentsViewSet

router = DefaultRouter()
router.register(r'comments', CommentsViewSet, basename='comments')
urlpatterns = router.urls

urlpatterns = [

] + router.urls
