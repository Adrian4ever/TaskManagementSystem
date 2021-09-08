from django.conf.global_settings import DEFAULT_FROM_EMAIL
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.comments.models import Comment
from apps.comments.serializers import CommentsSerializer


class CommentsViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentsSerializer

    def create(self, request, *args, **kwargs):
        serializer = CommentsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        task_id = validated_data.get('task')
        com_text = validated_data.get('text')
        self.perform_create(serializer)
        subject = 'One of your tasks was commented!'
        message = 'Hello, ' + task_id.owner.last_name + ', a new comment was posted to your ' + \
                  task_id.title + '\n Comment: "' + com_text + ' "'
        to_email = task_id.owner.email
        send_mail(subject, message, DEFAULT_FROM_EMAIL, [to_email])

        return Response({"success": True, "message": "comment added successfully"})
