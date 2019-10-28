from django.urls import path, include
from .views import (
    LectureListCreateView,
    LectureDetailView,
    CourseListCreateView,
    CourseDetailView,
    HometaskListCreateView,
    HometaskDetailView,
    TaskSolutionListCreateView,
    TaskSolutionDetailView,

    # nested
    CourseLecturesListView,
    LectureHometasksList,

)

app_name = "courses"

urlpatterns = [
    # users endpoits
    path('users/', include('users.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    # other endpoints
    path('tasksolutions/', TaskSolutionListCreateView.as_view()),
    path('tasksolutions/<int:pk>/', TaskSolutionDetailView.as_view()),
    path('hometasks/', HometaskListCreateView.as_view()),
    path('hometasks/<int:pk>/', HometaskDetailView.as_view()),
    path('lectures/', LectureListCreateView.as_view()),
    path('lectures/<int:pk>/', LectureDetailView.as_view()),
    path('courses/', CourseListCreateView.as_view()),
    path('courses/<int:pk>/', CourseDetailView.as_view()),
    path('courses/<int:pk>/lectures/', CourseLecturesListView.as_view()),
    path('lectures/<int:pk>/hometasks/', LectureHometasksList.as_view()),

]
