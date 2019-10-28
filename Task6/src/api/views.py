from .models import Lecture, Course, Hometask, TaskSolution
from .serializers import CourseDetailSerializer, LectureDetailSerializer, HometaskDetailSerializer, TaskSolutionDetailSerializer
from rest_framework import viewsets
from rest_framework import generics
from .permissions import IsOwnerOrReadOnly, IsStudentUser, IsTeacherUser
from rest_framework.permissions import IsAuthenticated


class CourseListCreateView(generics.ListCreateAPIView):
    serializer_class = CourseDetailSerializer
    queryset = Course.objects.all()
    #permission_classes = (IsAuthenticated, IsOwnerOrReadOnly, )


class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CourseDetailSerializer
    queryset = Course.objects.all()
    #permission_classes = (IsAuthenticated,)
    # permission_classes = (IsOwnerOrReadOnly)


class LectureListCreateView(generics.ListCreateAPIView):
    serializer_class = LectureDetailSerializer
    queryset = Lecture.objects.all()


class LectureDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LectureDetailSerializer
    queryset = Lecture.objects.all()


class HometaskListCreateView(generics.ListCreateAPIView):
    serializer_class = HometaskDetailSerializer
    queryset = Hometask.objects.all()


class HometaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HometaskDetailSerializer
    queryset = Hometask.objects.all()


class TaskSolutionListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSolutionDetailSerializer
    queryset = TaskSolution.objects.all()


class TaskSolutionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSolutionDetailSerializer
    queryset = TaskSolution.objects.all()


class CourseLecturesListView(generics.ListCreateAPIView):
    def get_queryset(self):
        queryset = Lecture.objects.filter(course=self.kwargs["pk"])
        return queryset
    serializer_class = LectureDetailSerializer


class LectureHometasksList(generics.ListCreateAPIView):
    def get_queryset(self):
        queryset = Hometask.objects.filter(lecture=self.kwargs["pk"])
        return queryset
    serializer_class = HometaskDetailSerializer
