from datetime import timedelta

from django.db.models import Sum, F, Q
from django.utils import timezone
from drf_util.decorators import serialize_decorator
from rest_framework import viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.users.get_user_model import USER_MODEL
from apps.users.serializers import UserSerializer, UserLogtime
from apps.timelogs.models import TimeLog


# class UserViewSet(viewsets.ModelViewSet):
#     queryset = USER_MODEL.objects.all()
#     serializer_class = UserSerializer


class RegisterUserView(GenericAPIView):
    serializer_class = UserSerializer

    permission_classes = (AllowAny,)
    authentication_classes = ()

    @serialize_decorator(UserSerializer)
    def post(self, request):
        validated_data = request.serializer.validated_data

        user = USER_MODEL.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()

        return Response(UserSerializer(user).data)


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
