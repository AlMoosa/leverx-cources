from rest_framework import generics

from .models import CustomUser
from .serializers import UserSerializer
# my
from users.serializers import CustomRegisterSerializer
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_auth.registration.views import RegisterView


class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


# Create your views here.
class CustomRegisterView(RegisterView):
    queryset = CustomUser.objects.all()
