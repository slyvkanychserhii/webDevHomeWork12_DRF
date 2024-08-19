from django.urls import path
from .views import (
    TaskListCreateView, 
    TaskFilterView, 
    TaskStatisticsView,
    SubTaskListCreateView,
    SubTaskDetailUpdateDeleteView,
)

urlpatterns = [
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/filter/', TaskFilterView.as_view(), name='task-filter'),
    path('tasks/statistics/', TaskStatisticsView.as_view(), name='task-statistics'),
    path('subtasks/', SubTaskListCreateView.as_view(), name='subtask-list-create'),
    path('subtasks/<int:pk>', SubTaskDetailUpdateDeleteView.as_view(), name='subtask-detail-update-delete'),
]
