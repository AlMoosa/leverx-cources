from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class IsTeacherUser(permissions.BasePermission):
    message = 'User is not teacher'

    def has_permission(self, request, view):
        return request.user and request.user.is_teacher

    def has_object_permission(self, request, view):
        return request.user and request.user.is_teacher


class IsStudentUser(permissions.BasePermission):
    message = 'User is not student'

    def has_permission(self, request, view):
        return request.user and request.user.is_student

    def has_object_permission(self, request, view):
        return request.user and request.user.is_student
