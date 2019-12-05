from django.urls import path
from . import views

urlpatterns = [
    path('snippets/detail/', views.snippet_list),
    path('test', views.snippet_abc),
    path('result/<task_id>', views.snippet_result),
    path('snippets/<int:pk>/', views.snippet_detail),
]
