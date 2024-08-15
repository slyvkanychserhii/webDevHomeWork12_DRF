from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from . import models
from . import serializers
from django.utils import timezone
from django.db.models import Count

# Создайте эндпойнт для создания новой задачи. Задача должна быть создана 
# с полями title, description, status, и deadline.
@api_view(['GET', 'POST'])
def tasks_list_create(request):
    if request.method == 'GET':
        tasks = models.Task.objects.all()
        serializer = serializers.TaskModelSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = serializers.TaskModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
def tasks_detail_update_delete(request, id=None):
    try:
        task = models.Task.objects.get(id=id)
    except models.Task.DoesNotExist:
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = serializers.TaskModelSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = serializers.TaskModelSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        task.delete()
        return Response({'message': 'Book deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

# Создайте эндпойнт для получения списка задач с фильтрацией по статусу и дедлайну. 
# Реализуйте пагинацию результатов.
# http://127.0.0.1:8000/api/tasks/status/NEW/deadline/gt/2024-08-15/page/1/
@api_view(['GET'])
def tasks_filtered(request, task_status, lookup, deadline, page):
    page_size = 2
    filters = {'status':task_status.upper(), f'deadline__{lookup}': deadline}
    tasks = models.Task.objects.filter(**filters)
    page_count = (tasks.count() + page_size - 1) // page_size
    start = (page - 1) * page_size
    end = min(start + page_size, tasks.count())
    paginated = tasks[start:end]
    serializer = serializers.TaskModelSerializer(paginated, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Создайте эндпойнт для получения статистики задач, таких как общее количество задач, 
# количество задач по каждому статусу и количество просроченных задач.
@api_view(['GET'])
def tasks_stats(request):
    total_tasks = models.Task.objects.count()
    tasks_by_status = models.Task.objects.values('status').annotate(count=Count('id'))
    overdue_tasks = models.Task.objects.filter(deadline__lt=timezone.now()).count()
    data = {
        'total_tasks': total_tasks,
        'tasks_by_status': list(tasks_by_status),
        'overdue_tasks': overdue_tasks
    }
    return Response(data, status=status.HTTP_200_OK)
