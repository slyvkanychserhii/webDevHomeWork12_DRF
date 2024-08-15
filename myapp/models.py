from django.db import models
from django.db.models.functions import Lower
from django.utils import timezone


StatusType = models.TextChoices('StatusType', "NEW IN_PROGRESS PENDING BLOCKED DONE")


class Category(models.Model):
    name = models.CharField(
        verbose_name='название категории',
        max_length=100,
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        db_table = '"task_manager_category"'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        constraints = [
            models.UniqueConstraint(Lower('name'), name='%(app_label)s_%(class)s_name_unique'),
        ]


def default_deadline():
    return timezone.now() + timezone.timedelta(days=7)


# Abstract base classes
# https://docs.djangoproject.com/en/5.0/topics/db/models/#abstract-base-classes

# Model Meta options
# https://docs.djangoproject.com/en/5.0/ref/models/options/


class BaseTask(models.Model):
    title = models.CharField(
        verbose_name='название задачи',
        max_length=100,
    )
    description = models.TextField(
        verbose_name='описание задачи',
        blank=True,
        null=True,
    )
    status = models.CharField(
        verbose_name='статус задачи',
        max_length=25,
        choices=StatusType.choices,
        default=StatusType.NEW,
    )
    deadline = models.DateTimeField(
        verbose_name='дата и время дедлайн',
        default=default_deadline,
    )
    created_at = models.DateTimeField(
        verbose_name='дата и время создания',
        auto_now_add=True,
    )

    def __str__(self):
        return self.title

    class Meta:
        abstract = True
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(Lower('title'), name='%(app_label)s_%(class)s_title_unique'),
        ]


class Task(BaseTask):
    categories = models.ManyToManyField(
        to=Category,
        related_name='tasks',  # по умолчанию: имя модели плюс суффикс '_set', например: сategory.task_set.all()
        related_query_name='task',  # по умолчанию: имя модели, например: Category.objects.filter(task__title='blablabla')
        verbose_name='категории задачи',
        blank=True,
    )

    class Meta(BaseTask.Meta):
        db_table = '"task_manager_task"'
        verbose_name = 'Task'


class SubTask(BaseTask):
    task = models.ForeignKey(
        to=Task,
        on_delete=models.CASCADE,
        related_name='sub_tasks',  # по умолчанию: имя модели плюс суффикс '_set', например: task.subtask_set.all()
        related_query_name='sub_task',  # по умолчанию: имя модели, например: Task.objects.filter(subtask__title='blablabla')
        verbose_name='основная задача',
    )

    class Meta(BaseTask.Meta):
        db_table = '"task_manager_subtask"'
        verbose_name = 'SubTask'
