from rest_framework import serializers

from apps.users.get_user_model import USER_MODEL


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = USER_MODEL
        # fields = '__all__'
        fields = ("id", "first_name", "last_name", "email", "password",)
