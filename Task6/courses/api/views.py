from .models import (
    Lecture,
    Course,
    Task,
    Hometask,
    Comment,
)
from .serializers import (
    CourseSerializer,
    CourseDetailSerializer,
    LectureDetailSerializer,
    TaskDetailSerializer,
    HometaskDetailSerializer,
    HometaskStudentDetailSerializer,
    HometaskTeacherDetailSerializer,

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
    IsStudentOrAdminOrReadOnly,
    IsNotYourCourse,

)
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class CourseListCreateView(generics.ListCreateAPIView):
    serializer_class = CourseSerializer
    permission_classes = (IsAuthenticated, IsTeacherOrAdminOrReadOnly)

    def get_queryset(self):
        if self.request.user.is_student:
            queryset = Course.objects.filter(students=self.request.user)
        elif self.request.user.is_teacher:
            queryset = Course.objects.filter(teachers=self.request.user)
        elif self.request.user.is_superuser:
            queryset = Course.objects.all()
        return queryset

    def perform_create(self, serializers):
        serializers.save(teachers=(self.request.user,))


class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CourseDetailSerializer
    queryset = Course.objects.all()
    permission_classes = (
        IsAuthenticated,
        IsTeacherOrAdminOrReadOnly,
        IsNotYourCourse,

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
    permission_classes = (
        IsAuthenticated,
        IsTeacherOrAdminOrReadOnly,
    )
    queryset = Lecture.objects.all()


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
    permission_classes = (IsAuthenticated, IsTeacherOrAdminOrReadOnly)


class HometaskListCreateView(generics.ListCreateAPIView):
    # serializer_class = HometaskDetailSerializer
    permission_classes = (
        IsAuthenticated,
        IsStudentOrAdminOrReadOnly,
    )

    def get_serializer_class(self):
        if self.request.user.is_student:
            return HometaskStudentDetailSerializer
        elif self.request.user.is_teacher:
            return HometaskTeacherDetailSerializer
        elif self.request.user.is_superuser:
            return HometaskDetailSerializer

    def get_queryset(self):
        if self.request.user.is_student:
            queryset = Hometask.objects.filter(
                student=self.request.user)
        elif self.request.user.is_teacher:
            queryset = Hometask.objects.filter(
                task__lecture__course__teachers=self.request.user)
        elif self.request.user.is_superuser:
            queryset = Hometask.objects.all()
        return queryset

    def perform_create(self, serializers):
        serializers.save(student=self.request.user)


class HometaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    # queryset = Hometask.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.user.is_student:
            return HometaskStudentDetailSerializer
        elif self.request.user.is_teacher:
            return HometaskTeacherDetailSerializer
        elif self.request.user.is_superuser:
            return HometaskDetailSerializer

    def get_queryset(self):
        if self.request.user.is_student:
            self.permission_classes = (IsStudentOrAdminOrReadOnly,)

        elif self.request.user.is_teacher or self.request.user.is_superuser:
            self.permission_classes = (IsTeacherOrAdminOrReadOnly,)
        return Hometask.objects.all()


class MarkListCreateView(generics.ListAPIView):
    serializer_class = MarkDetailSerializer
    permission_classes = (IsAuthenticated, IsStudentUser)

    def get_queryset(self):
        queryset = Hometask.objects.filter(student=self.request.user)
        return queryset


# class CommentListCreateView(generics.ListCreateAPIView):
#     serializer_class = CommentDetailSerializer
#     queryset = Comment.objects.all()


# class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = CommentDetailSerializer
#     queryset = Comment.objects.all()


class HometaskCommentListView(generics.ListCreateAPIView):
    serializer_class = CommentDetailSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        queryset = Comment.objects.filter(hometask=self.kwargs["pk"])
        return queryset

    def perform_create(self, serializers):
        serializers.save(user=self.request.user)


class CourseLecturesListView(generics.ListCreateAPIView):
    serializer_class = CommentDetailSerializer
    permission_classes = (IsAuthenticated, IsTeacherOrAdminOrReadOnly)

    def get_queryset(self):
        queryset = Lecture.objects.filter(course=self.kwargs["pk"])
        return queryset


class LectureTasksListView(generics.ListCreateAPIView):
    serializer_class = TaskDetailSerializer
    permission_classes = (IsAuthenticated, IsTeacherOrAdminOrReadOnly)

    def get_queryset(self):
        queryset = Task.objects.filter(lecture=self.kwargs["pk"])
        return queryset
