from rest_framework import serializers
from .models import (
    Lecture,
    Course,
    Task,
    Hometask,
    Comment,
)
from users.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email')


class CourseDetailSerializer(serializers.ModelSerializer):
    students = CustomUserSerializer(many=True)
    teachers = CustomUserSerializer(many=True)

    class Meta:
        model = Course
        fields = '__all__'


class LectureDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lecture
        fields = '__all__'


class TaskDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class HometaskDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hometask
        fields = '__all__'


class MarkDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hometask
        fields = ('id', 'task', 'mark',)


class CommentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
