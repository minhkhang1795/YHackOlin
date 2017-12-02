from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Creator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, null=True)

    def __str__(self):
        return "Creator %s" % self.user.username


class Post(models.Model):
    creator = models.ForeignKey(Creator, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default="")
    short_description = models.TextField(blank=True, default="")
    story = models.TextField(blank=True, default="")
    pub_date = models.DateTimeField('date published', default=timezone.now)
    # vote_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title
