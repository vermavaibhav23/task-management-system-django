from rest_framework import serializers

from polls.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'user', 'title', 'description', 'status', 'priority', 'timestamp']
        extra_kwargs = {'user': {'required': False}}  # Ensure user is not required from request
