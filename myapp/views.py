from rest_framework.views import APIView
from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework import status
from .models import Task, SubTask
from .serializers import (
    TaskSerializer, 
    TaskCreateSerializer,
    SubTaskSerializer,
    SubTaskCreateSerializer,
)
from django.utils import timezone
from django.db.models import Count


class TaskListCreateView(APIView):
    def get(self, request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TaskCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# hw11
# Создайте эндпойнт для получения списка задач с фильтрацией по статусу и дедлайну. 
# Реализуйте пагинацию результатов.
# http://127.0.0.1:8000/api/tasks/filter/?status=NEW&deadline=2024-08-19&page=2
class TaskFilterView(APIView):
    def get(self, request):
        filters = {}
        if 'status' in request.query_params:
            filters['status'] = request.query_params.get('status')
        if 'deadline' in request.query_params:
            filters['deadline__lte'] = request.query_params.get('deadline')
        tasks = Task.objects.filter(**filters)
        pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
        paginator = pagination_class()
        paginated_tasks = paginator.paginate_queryset(tasks, request)
        serializer = TaskSerializer(paginated_tasks, many=True)
        return paginator.get_paginated_response(serializer.data)


# hw11
# Создайте эндпойнт для получения статистики задач, таких как общее количество задач, 
# количество задач по каждому статусу и количество просроченных задач.
class TaskStatisticsView(APIView):
    def get(self, request):
        data = {}
        data['tasks'] = Task.objects.count()
        data['tasks_by_status'] = Task.objects.values('status').annotate(count=Count('id'))
        data['tasks_lte_now'] = Task.objects.filter(deadline__lt=timezone.now()).count()
        return Response(data, status=status.HTTP_200_OK)


# hw12
# Задание 5: Создание классов представлений
# Создайте классы представлений для работы с подзадачами (SubTasks), 
# включая создание, получение, обновление и удаление подзадач. 
# Используйте классы представлений (APIView) для реализации этого функционала.
# Шаги для выполнения:
#  - Создайте классы представлений для создания и получения списка подзадач (SubTaskListCreateView).
#  - Создайте классы представлений для получения, обновления и удаления подзадач (SubTaskDetailUpdateDeleteView).
#  - Добавьте маршруты в файле urls.py, чтобы использовать эти классы.
class SubTaskListCreateView(APIView):
    def get(self, request):
        subtasks = SubTask.objects.all()
        serializer = SubTaskSerializer(subtasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SubTaskCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubTaskDetailUpdateDeleteView(APIView):
    def get(self, request, pk):
        try:
            subtask = SubTask.objects.get(pk=pk)
        except SubTask.DoesNotExist:
            return Response({'error': 'Подзадача не найдена'}, status=status.HTTP_404_NOT_FOUND)
        serializer = SubTaskCreateSerializer(subtask)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            subtask = SubTask.objects.get(pk=pk)
        except SubTask.DoesNotExist:
            return Response({'error': 'Подзадача не найдена'}, status=status.HTTP_404_NOT_FOUND)
        serializer = SubTaskCreateSerializer(subtask, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            subtask = SubTask.objects.get(pk=pk)
        except SubTask.DoesNotExist:
            return Response({'error': 'Подзадача не найдена'}, status=status.HTTP_404_NOT_FOUND)
        subtask.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
