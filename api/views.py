from rest_framework import generics, permissions
from .serializers import TodoSerializer, TodoToggleCompleteSerializer
from todo.models import Todo
from django.db import IntegrityError
from django.contrib.auth.models import User
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate

# Create your views here.

# http://localhost:8000/api/todos/
class TodoListAndCreate(generics.ListCreateAPIView):
    # ListAPIView requires two mandatory attributes, serializer_class and
    # queryset.
    # We specify TodoSerializer which we have earlier implemented
    serializer_class = TodoSerializer

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user).order_by("-created")

    def perform_create(self, serializer):
        # serializer holds a django model
        serializer.save(user=self.request.user)


"""
Django REST Framework provides the built-in RetrieveUpdateDestroyAPIView to automatically implement the
get(), put() and delete() endpoint.
http://localhost:8000/api/todos/<todo_id>
"""


class TodoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)


class TodoToggleComplete(generics.UpdateAPIView):
    serializer_class = TodoToggleCompleteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)

    # perform update when toggle complete
    def perform_update(self, serializer):
        serializer.instance.completed = not (serializer.instance.completed)
        serializer.save()


@csrf_exempt
def signup(request):
    if request.method == "POST":
        try:
            data = JSONParser().parse(request)  # data is a dict
            user = User.objects.create_user(
                username=data["username"], password=data["password"]
            )
            user.save()

            token = Token.objects.create(user=user)
            return JsonResponse({"token": str(token)}, status=201)
        except IntegrityError:
            return JsonResponse(
                {"error": "username taken. choose another username"}, status=400
            )


@csrf_exempt
def login(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        user = authenticate(
            request, username=data["username"], password=data["password"]
        )
        if user is None:
            return JsonResponse(
                {"error": "unable to login, check username and password"}, status=400
            )

        else:
            try:
                token = Token.objects.get(user=user)
            except:
                token = Token.objects.create(user=user)

            return JsonResponse({"token": str(token)}, status=201)
