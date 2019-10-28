from rest_framework import serializers
from .models import Lecture, Course, Hometask, TaskSolution


class CourseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class LectureDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = '__all__'


class HometaskDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hometask
        fields = '__all__'


class TaskSolutionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskSolution
        fields = '__all__'
