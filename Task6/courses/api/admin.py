from django.contrib import admin
from .models import (
    Lecture,
    Course,
    Task,
    Hometask,
    Comment,
)

admin.site.register(Lecture)
admin.site.register(Course)
admin.site.register(Task)
admin.site.register(Hometask)
admin.site.register(Comment)
