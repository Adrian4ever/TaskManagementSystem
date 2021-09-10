from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.get_user_model import USER_MODEL


class TokenObtainLifetimeSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['lifetime'] = int(refresh.access_token.lifetime.total_seconds())
        return data


class TokenRefreshLifetimeSerializer(TokenRefreshSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = RefreshToken(attrs['refresh'])
        data['lifetime'] = int(refresh.access_token.lifetime.total_seconds())
        return data


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = USER_MODEL
        fields = ("id", "first_name", "last_name", "email", "password")


class UserLogtime(serializers.ModelSerializer):
    user_work_time = serializers.SerializerMethodField()

    class Meta:
        model = USER_MODEL
        fields = ("first_name", "last_name", "email", "user_work_time")

    def get_user_work_time(self, obj):
        if obj.user_work_time:
            return obj.user_work_time / 60
        return obj.user_work_time
