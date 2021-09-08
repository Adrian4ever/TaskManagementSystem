from rest_framework.routers import DefaultRouter

from apps.timelogs.views import TimeLogViewSet

router = DefaultRouter()

router.register(r'timelogs', TimeLogViewSet, basename='timelogs')

urlpatterns = router.urls

urlpatterns += [

]
