from django.conf import settings
from django.urls import reverse
from django.db import models
from django.utils import timezone
import datetime
from dateutil.parser import parse
import misaka
from groups.models import  Group
from django.contrib.auth import get_user_model
User = get_user_model()


class Post(models.Model):
    user = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    dead_line = models.DateTimeField(null=False)
    created_at = models.DateTimeField(auto_now=True)
    message = models.TextField(max_length=100)
    message_html = models.TextField(editable=False,max_length=100)
    group = models.ForeignKey(Group, related_name="posts",null=True, blank=True, on_delete=models.CASCADE)
    # a=dateutil.parser.parse('dead_line')
    # b=dateutil.parser.parse('created_at')

    # def status(self):
    #     if self.dead_line and datetime.date.today()  > self.dead_line:
    #         return True
    now1=datetime.datetime.now()




    # if now __gte dead_line:
    #     print ('complete')
    # else:
    #     print ('incomplete')

    def __str__(self):
        return self.message

    def save(self, *args, **kwargs):
        self.message_html = misaka.html(self.message)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "posts:single",
            kwargs={
                "username": self.user.username,
                "pk": self.pk
            }
        )

    class Meta:
        ordering = ["-created_at"]
        unique_together = ["user", "message"]
