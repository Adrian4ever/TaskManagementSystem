from datetime import timedelta

from django.db.models import Sum, F, Q
from django.utils import timezone
from drf_util.decorators import serialize_decorator
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.users.get_user_model import USER_MODEL
from apps.users.serializers import UserLogtime, UserRegisterSerializer


class RegisterUserView(GenericAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class UserLogtimeView(GenericAPIView):
    queryset = USER_MODEL.objects.all
    serializer_class = UserLogtime

    def get(self, request):
        users = USER_MODEL.objects.filter(email=self.request.user).annotate(
            user_work_time=Sum(
                F('timelog__end_time') -
                F('timelog__start_time'),
                filter=Q(timelog__end_time__gte=timezone.now() - timedelta(days=30))
            )
        )
        return Response(UserLogtime(users, many=True).data)
