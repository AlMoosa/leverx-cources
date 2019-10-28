from django.urls import include, path

from .views import UserListView, CustomRegisterView


urlpatterns = [
    path('', UserListView.as_view()),
    path('registration/', CustomRegisterView.as_view()),

]
