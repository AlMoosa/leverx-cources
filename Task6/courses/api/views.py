from .models import (
    Lecture,
    Course,
    Task,
    Hometask,
    Comment,
)
from .serializers import (
    CourseDetailSerializer,
    LectureDetailSerializer,
    TaskDetailSerializer,
    HometaskDetailSerializer,
    CommentDetailSerializer,
    MarkDetailSerializer,
)
from rest_framework import viewsets
from rest_framework import generics
from .permissions import (
    IsOwnerOrReadOnly,
    IsStudentUser,
    IsTeacherUser,
    IsTeacherOrAdminOrReadOnly,
    IsNotYourCourse,

)
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class CourseListCreateView(generics.ListCreateAPIView):
    serializer_class = CourseDetailSerializer
    permission_classes = (IsAuthenticated, IsTeacherOrAdminOrReadOnly)

    def get_queryset(self):
        if self.request.user.is_student:
            queryset = Course.objects.filter(students=self.request.user)
        elif self.request.user.is_teacher:
            queryset = Course.objects.filter(teachers=self.request.user)
        elif self.request.user.is_superuser:
            queryset = Course.objects.all()
        return queryset


class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CourseDetailSerializer
    queryset = Course.objects.all()
    permission_classes = (
        IsAuthenticated,
        IsTeacherOrAdminOrReadOnly,
        IsNotYourCourse
    )


class LectureListCreateView(generics.ListCreateAPIView):
    serializer_class = LectureDetailSerializer
    # queryset = Lecture.objects.all()
    permission_classes = (
        IsAuthenticated,
        IsTeacherOrAdminOrReadOnly,
    )

    def get_queryset(self):
        if self.request.user.is_student:
            queryset = Lecture.objects.filter(
                course__students=self.request.user)
        elif self.request.user.is_teacher:
            queryset = Lecture.objects.filter(
                course__teachers=self.request.user)
        elif self.request.user.is_superuser:
            queryset = Lecture.objects.all()
        return queryset


class LectureDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LectureDetailSerializer
    queryset = Lecture.objects.all()
    permission_classes = (IsAuthenticated, IsTeacherOrAdminOrReadOnly)


class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskDetailSerializer
    # queryset = Task.objects.all()
    permission_classes = (IsAuthenticated, IsTeacherOrAdminOrReadOnly)

    def get_queryset(self):
        if self.request.user.is_student:
            queryset = Task.objects.filter(
                lecture__course__students=self.request.user)
        elif self.request.user.is_teacher:
            queryset = Task.objects.filter(
                lecture__course__teachers=self.request.user)
        elif self.request.user.is_superuser:
            queryset = Task.objects.all()
        return queryset


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskDetailSerializer
    queryset = Task.objects.all()


class HometaskListCreateView(generics.ListCreateAPIView):
    serializer_class = HometaskDetailSerializer
    # queryset = Hometask.objects.all()

    def get_queryset(self):
        queryset = Hometask.objects.filter(student=self.request.user)
        return queryset


class HometaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HometaskDetailSerializer
    queryset = Hometask.objects.all()


class MarkListCreateView(generics.ListAPIView):
    serializer_class = MarkDetailSerializer
    # queryset = Hometask.objects.all()

    def get_queryset(self):
        queryset = Hometask.objects.filter(student=self.request.user)
        return queryset


class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentDetailSerializer
    queryset = Comment.objects.all()


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentDetailSerializer
    queryset = Comment.objects.all()

# -----------------


class CourseLecturesListView(generics.ListCreateAPIView):
    def get_queryset(self):
        queryset = Lecture.objects.filter(course=self.kwargs["pk"])
        return queryset
    serializer_class = LectureDetailSerializer
    permission_classes = (IsAuthenticated, IsTeacherOrAdminOrReadOnly)


class LectureTasksListView(generics.ListCreateAPIView):
    def get_queryset(self):
        queryset = Task.objects.filter(lecture=self.kwargs["pk"])
        return queryset
    serializer_class = TaskDetailSerializer
    permission_classes = (IsAuthenticated, IsTeacherOrAdminOrReadOnly)
