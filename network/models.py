from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField('self', related_name="follower", blank=True, symmetrical=False)
    #followers = *look at self*
    #following = *look at self*
    #posts = *look at post model*
    #likedposts = *look at post model*
    #pass

class post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    text = models.CharField(max_length=250)
    time = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(blank= True, null=True, default='0')
    likers = models.ManyToManyField(User, related_name="likedposts", blank=True)
    def __str__(self):
        return self.text