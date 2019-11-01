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


class CourseSerializer(serializers.ModelSerializer):
    # students = CustomUserSerializer(many=True)
    # teachers = CustomUserSerializer(many=True)

    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ('teachers',)


class CourseDetailSerializer(serializers.ModelSerializer):
    # students = CustomUserSerializer(many=True)
    # teachers = CustomUserSerializer(many=True)

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


class HometaskStudentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hometask
        fields = '__all__'
        read_only_fields = ('mark', 'student',)


class HometaskTeacherDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hometask
        fields = '__all__'
        read_only_fields = ('id', 'solution_file', 'student', 'task')


class MarkDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hometask
        fields = ('id', 'task', 'mark',)


class CommentDetailSerializer(serializers.ModelSerializer):
    # user = CustomUserSerializer()

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('user',)
