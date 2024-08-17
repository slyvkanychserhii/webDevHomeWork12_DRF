from rest_framework import serializers
from . import models


# class TaskModelSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Task
#         fields = ['title', 'description', 'status', 'deadline',]


# hw12
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Task
        fields = ['title', 'description', 'status', 'deadline',]


# hw12
class TaskCreateSerializer(serializers.ModelSerializer):
    pass


# hw12
class TaskDetailSerializer(serializers.ModelSerializer):
    pass


# hw12
class SubTaskSerializer(serializers.ModelSerializer):
    pass


# hw12
class SubTaskCreateSerializer(serializers.ModelSerializer):
    pass


# hw12
class CategoryCreateSerializer(serializers.ModelSerializer):
    pass
