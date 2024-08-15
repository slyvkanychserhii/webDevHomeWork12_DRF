from django.urls import path
from . import views

urlpatterns = [
    path('tasks/', views.tasks_list_create),
    path('tasks/<int:id>/', views.tasks_detail_update_delete),
    path('tasks/status/<str:task_status>/deadline/<str:lookup>/<str:deadline>/page/<int:page>/', views.tasks_filtered),
    path('tasks/stats/', views.tasks_stats),
]
