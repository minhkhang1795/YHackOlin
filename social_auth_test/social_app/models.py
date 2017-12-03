from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class Creator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, null=True)
    profile_pic_url = models.TextField(default="")
    cover_pic_url = models.TextField(default="")
    bio = models.TextField(default="")

    # favorite_posts =
    # voted_posts =

    def __str__(self):
        return "Creator %s" % self.user.username


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return "Category %s" % self.name


class Experience(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return "Experience %s" % self.name


class Post(models.Model):
    creator = models.ForeignKey(Creator, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default="")
    short_description = models.TextField(blank=True, default="")
    story = models.TextField(blank=True, default="")
    pub_date = models.DateTimeField('date published', default=timezone.now)
    categories = models.ManyToManyField(Category, blank=True)
    experiences = models.ManyToManyField(Experience, blank=True)

    pictures = models.TextField(blank=True, default="", null=True)

    def get_like_count(self):

        return self.liketable_set.all().count()

    # personal_links = models.TextField(blank=True, default="", null=True)
    # helpful_links = models.TextField(blank=True, default="")
    # material_ls = models.TextField(blank=True, default="")
    # favorite_count = models.IntegerField(default=0)
    # view_count = models.IntegerField(default=0)
    # vote_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class LikeTable(models.Model):
    creator = models.ForeignKey(Creator)
    post = models.ForeignKey(Post)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('creator', 'post',)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Creator.objects.get_or_create(user=instance)
