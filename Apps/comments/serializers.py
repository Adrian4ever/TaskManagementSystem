from rest_framework import serializers

from apps.comments.models import Comment


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
