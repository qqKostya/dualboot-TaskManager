from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .models import Tag
from .models import Task

admin.site.register(User, UserAdmin, Tag, Task)
