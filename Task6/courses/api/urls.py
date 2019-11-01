from rest_auth.registration.views import VerifyEmailView, RegisterView
from django.urls import path, include, re_path
from .views import (
    LectureListCreateView,
    LectureDetailView,
    CourseListCreateView,
    CourseDetailView,
    TaskListCreateView,
    TaskDetailView,
    HometaskListCreateView,
    HometaskDetailView,
    MarkListCreateView,
    HometaskCommentListView,
    CourseLecturesListView,
    LectureTasksListView,
)

app_name = "courses"

urlpatterns = [
    path('users/', include('users.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),

    # path('comments/', CommentListCreateView.as_view()),
    # path('comments/<int:pk>/', CommentDetailView.as_view()),

    path('hometasks/', HometaskListCreateView.as_view()),
    path('hometasks/<int:pk>/', HometaskDetailView.as_view()),
    path('hometasks/<int:pk>/comments/', HometaskCommentListView.as_view()),

    path('marks/', MarkListCreateView.as_view()),

    path('tasks/', TaskListCreateView.as_view()),
    path('tasks/<int:pk>/', TaskDetailView.as_view()),

    path('lectures/', LectureListCreateView.as_view()),
    path('lectures/<int:pk>/', LectureDetailView.as_view()),

    path('courses/', CourseListCreateView.as_view()),
    path('courses/<int:pk>/', CourseDetailView.as_view()),
    path('courses/<int:pk>/lectures/', CourseLecturesListView.as_view()),

    path('lectures/<int:pk>/tasks/', LectureTasksListView.as_view()),

]
