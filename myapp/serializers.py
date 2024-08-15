from rest_framework import serializers
from . import models


class TaskModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Task
        fields = ['title', 'description', 'status', 'deadline',]
