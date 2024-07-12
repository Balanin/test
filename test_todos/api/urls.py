# api/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('todos/', views.TodoCreate.as_view(), name='todo-list-create'),
    path('todos/<int:pk>/', views.TodoRetrieveUpdateDestroy.as_view(), name='todo-detail'),
    path('todos/<int:pk>/complete/', views.TodoToggleComplete.as_view(), name='todo-complete'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('login_by_google/', views.home, name='login_by_google'),
    path('logout/', views.logout_view, name='logout'),
]
