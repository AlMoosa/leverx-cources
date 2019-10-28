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


class Logout(APIView):
    queryset = CustomUser.objects.all()

    def get(self, request, format=None):
        # simply delete the token to force a login
        print(request.user)
        return Response(status=status.HTTP_200_OK)
