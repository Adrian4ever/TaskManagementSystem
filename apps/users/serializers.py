from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from simplejson.compat import text_type

from apps.users.get_user_model import USER_MODEL


class UserRegisterSerializer(serializers.ModelSerializer):
    tokens = serializers.SerializerMethodField()

    class Meta:
        model = USER_MODEL
        fields = ('id', 'first_name', 'last_name', 'password', 'email', 'tokens')
        extra_kwargs = {'password': {'write_only': True}}

    def get_tokens(self, user):
        tokens = RefreshToken.for_user(user)
        refresh = text_type(tokens)
        access = text_type(tokens.access_token)
        data = {
            "refresh": refresh,
            "access": access
        }

        return data

    def create(self, validated_data):
        user = USER_MODEL(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = USER_MODEL
        fields = ("id", "first_name", "last_name", "email",)


class UserLogtime(serializers.ModelSerializer):
    user_work_time = serializers.SerializerMethodField()

    class Meta:
        model = USER_MODEL
        fields = ("first_name", "last_name", "email", "user_work_time")

    def get_user_work_time(self, obj):
        if obj.user_work_time:
            return obj.user_work_time / 60
        return obj.user_work_time
