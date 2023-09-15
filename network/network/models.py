from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime

class User(AbstractUser):
    pass


class Post(models.Model):
    poster = models.ForeignKey(User,on_delete=models.CASCADE, related_name="poster")
    text = models.CharField(max_length=200)
    posted_on = models.DateField(default=datetime.now)

    def __str__(self):
        return f"{self.poster}, created on {self.posted_on}"

class Like(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="post")
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user")

    def __str__(self):
        return f"Like in post {self.post.id} by {self.user}"

class Follow(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_following")
    userFollowed = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_followed")

    def __str__(self):
        return f"{self.user} is following {self.userFollowed}"