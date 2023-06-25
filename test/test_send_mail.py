from unittest.mock import patch, MagicMock

from django.core import mail
from django.template.loader import render_to_string

from main.models import Task
from task_manager.services.mail import send_assign_notification
from test.base import TestViewSetBase


class TestSendEmail(TestViewSetBase):
    basename = 'tasks'
    @patch.object(mail, "send_mail")
    def test_send_assign_notification(self, fake_sender: MagicMock) -> None:
        assignee = self.create_api_user
        task = self.create(assignee)

        send_assign_notification(task["id"])

        fake_sender.assert_called_once_with(
            subject="You've assigned a task.",
            message="",
            from_email=None,
            recipient_list=[assignee.email],
            html_message=render_to_string(
                "emails/notification.html",
                context={"task": Task.objects.get(pk=task["id"])},
            ),
        )
