from rest_framework import serializers
from .models import CustomUser

# from allauth.socialaccount.models import SocialAccount
# from allauth.socialaccount.providers.base import AuthProcess
# from requests.exceptions import HTTPError
from rest_framework import serializers
from rest_auth.serializers import UserDetailsSerializer
from rest_auth.registration.serializers import RegisterSerializer
from allauth.account.adapter import get_adapter

# from allauth.account import app_settings as allauth_settings
# from allauth.utils import email_address_exists
# from allauth.account.adapter import get_adapter
# from allauth.account.utils import setup_user_email


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'is_student', 'is_teacher')


class CustomRegisterSerializer(RegisterSerializer):

    is_student = serializers.BooleanField(default=False)
    is_teacher = serializers.BooleanField(default=False)

    # def get_cleaned_data(self):
    #     data_dict = super().get_cleaned_data()
    #     data_dict['is_student'] = self.validated_data.get('is_student', '')
    #     data_dict['is_teacher'] = self.validated_data.get('is_teacher', '')
    #     return data_dict

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password', 'is_student', 'is_teacher')

    def get_cleaned_data(self):
        return {
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'email': self.validated_data.get('email', ''),
            'is_student': self.validated_data.get('is_student', ''),
            'is_teacher': self.validated_data.get('is_teacher', '')
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user.is_student = self.cleaned_data.get('is_student')
        user.is_teacher = self.cleaned_data.get('is_teacher')
        user.save()
        adapter.save_user(request, user, self)
        return user


class CustomUserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'is_student', 'is_teacher')
