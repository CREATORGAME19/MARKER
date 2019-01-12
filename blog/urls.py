from django.urls import path
from . import views
from django.urls import path, include 
urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('login', include('django.contrib.auth.urls'), name='login'),
    path('<int:id>',views.task, name='task'),
    path('task_submit/<int:id>',views.task_submit, name='task_submit'),
]
