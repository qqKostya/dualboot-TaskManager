from django.db import models
from .user import User
from .tag import Tag


class Task(models.Model):
    class State(models.TextChoices):
        NEW = "new_task"
        IN_DEVELOPMENT = "in_development"
        IN_QA = "in_qa"
        IN_CODE_REVIEW = "in_code_review"
        READT_FOR_RELEASE = "ready_for_release"
        RELEASED = "released"
        ARCHIVED = "archived"

    class Priority(models.TextChoices):
        LOW = "Low"
        MEDIUM = "Medium"
        HIGH = "High"

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_change = models.DateTimeField(auto_now=True)
    deadline = models.DateField()
    state = models.CharField(max_length=255, choices=State.choices, default=State.NEW)
    priority = models.CharField(
        max_length=255, choices=Priority.choices, default=Priority.LOW
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="author_task"
    )
    executor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="executor_tasl"
    )
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title
