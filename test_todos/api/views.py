from django.shortcuts import render, redirect
from rest_framework import generics, permissions
from django.contrib.auth import authenticate, logout
from django.db import IntegrityError
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
import time

from todo.models import Todo
from .serializer import TodoSerializer, TodoToggleComplateSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination

class todosPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 10

class TodoCreate(generics.ListCreateAPIView):
    pagination_class = todosPagination
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]
    # filter_backends = [DjangoFilterBackend, OrderingFilter]
    # filterset_fields = ['completed', 'due_date']
    # ordering_fields = ['due_date']
    
    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user).order_by('-created_at')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TodoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
 
        return Todo.objects.filter(user=user)

    
class TodoToggleComplete(generics.UpdateAPIView):
    serializer_class = TodoToggleComplateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user)
    
    def perform_update(self, serializer):
        serializer.instance.complated = not(serializer.instance.complated)
        serializer.save()


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            user = User.objects.create_user(
                username=data['username'],
                password = data['password'])
            user.save()
            token = Token.objects.create(user=user)
            return JsonResponse({'token':str(token)},status = 201)
        except IntegrityError:
            return JsonResponse(
                {'error':'username taken.choose another username'},status=400
            )

@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            print(request)
            data = JSONParser().parse(request)
            username = data.get('username')
            password = data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is None:
                return JsonResponse({'error': 'Unable to login. Check username and password.'}, status=400)
            else:
                token, created = Token.objects.get_or_create(user=user)
                return JsonResponse({'token': str(token)}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    

def home(request):
    return render(request,'home.html')  

def logout_view(request):
    logout(request)
    return redirect('/')


