from rest_framework import serializers
from .models import Task, SubTask, Category
from django.utils import timezone


class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = '__all__'


# hw12
# Задание 1: Переопределение полей сериализатора
# Создайте SubTaskCreateSerializer, в котором поле created_at 
# будет доступно только для чтения (read_only).
# Шаги для выполнения:
#  - Определите SubTaskCreateSerializer в файле serializers.py.
#  - Переопределите поле created_at как read_only.
class SubTaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = '__all__'
        read_only_fields = ['created_at']


# hw12
# Задание 2: Переопределение методов create и update
# Создайте сериализатор для категории CategoryCreateSerializer, 
# переопределив методы create и update для проверки уникальности 
# названия категории. Если категория с таким названием уже существует, 
# возвращайте ошибку валидации.
# Шаги для выполнения:
#  - Определите CategoryCreateSerializer в файле serializers.py.
#  - Переопределите метод create для проверки уникальности названия категории.
#  - Переопределите метод update для аналогичной проверки при обновлении.
class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
    
    def create(self, validated_data):
        сategory_name = validated_data.get('name')
        if Category.objects.filter(name__iexact=сategory_name).exists():
            raise serializers.ValidationError('Категория с таким названием уже существует.')
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        pk = instance.pk
        сategory_name = validated_data.get('name')
        if Category.objects.filter(name__iexact=сategory_name).exclude(pk=pk).exists():
            raise serializers.ValidationError('Категория с таким названием уже существует.')
        return super().update(instance, validated_data)


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'deadline',]


# hw12
# Задание 3: Использование вложенных сериализаторов
# Создайте сериализатор для TaskDetailSerializer, который включает 
# вложенный сериализатор для полного отображения связанных подзадач (SubTask). 
# Сериализатор должен показывать все подзадачи, связанные с данной задачей.
# Шаги для выполнения:
#  - Определите TaskDetailSerializer в файле serializers.py.
#  - Вложите SubTaskSerializer внутрь TaskDetailSerializer.
class TaskDetailSerializer(serializers.ModelSerializer):
    subtask = SubTaskSerializer()
    
    class Meta:
        model = Task
        fields = '__all__'


# hw12
# Задание 4: Валидация данных в сериализаторах
# Создайте TaskCreateSerializer и добавьте валидацию для поля deadline, 
# чтобы дата не могла быть в прошлом. Если дата в прошлом, 
# возвращайте ошибку валидации.
# Шаги для выполнения:
#  - Определите TaskCreateSerializer в файле serializers.py.
#  - Переопределите метод validate_deadline для проверки даты.
class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
    
    def validate_deadline(self, value):
        # Django сам добавляет наивной дате информацию о своей временной зоне
        # "2024-08-15" -> '2024-08-15T00:00:00+00:00'
        # Django сам приводит дату к своей временной зоне 
        # "2024-08-15T00:53:40+01:00" -> '2024-08-14T23:53:40+00:00'
        if value < timezone.now():
            raise serializers.ValidationError("Дедлайн не может быть в прошлом")
        return value
