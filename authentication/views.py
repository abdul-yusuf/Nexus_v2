from django.shortcuts import render
from .serializers import UserRegSerializer
from rest_framework import generics
from .models import User
# Create your views here.

class UserRegistration(generics.CreateAPIView):
    queryset = User
    serializer_class = UserRegSerializer

