from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


class User(AbstractUser):
    pass

    def __str__(self):
        return f"{self.username}"

class Category(models.Model):
    type = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.type}"

class AuctionListing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=300)
    startingBid = models.FloatField()
    actualBid = models.FloatField()
    url = models.URLField(null=True)
    owner = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name="user")
    category = models.ForeignKey(Category,on_delete=models.CASCADE,blank=True,null=True,related_name="category")
    isActive = models.BooleanField(default=True)
    lastOferrer = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name="lastOferrer")

    def __str__(self):
        return f"{self.title}"

class WatchList(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name="userWatchlist")
    list = models.ForeignKey(AuctionListing,on_delete=models.CASCADE,blank=True,null=True,related_name="listWatchlist")

    class Meta:
        unique_together = ('user', 'list')

    def __str__(self):
        return f"{self.user.username}, {self.list.title}"

class Bid(models.Model):
    oferrer = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name="oferrer")
    watchlist = models.ForeignKey(AuctionListing,on_delete=models.CASCADE,blank=True,null=True,related_name="bidWatchlist")
    date = models.DateTimeField(default=datetime.now)
    
    class Meta:
        unique_together = ('oferrer', 'watchlist','date')
    
    def __str__(self):
        return f"Oferrer: {self.oferrer}, list: {self.watchlist} at date: {self.date}"


class Comment(models.Model):
    poster = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name="poster")
    list = models.ForeignKey(AuctionListing,on_delete=models.CASCADE,blank=True,null=True,related_name="postList")
    body = models.TextField()
    created_on = models.DateTimeField(default=datetime.now)

    class Meta:
        ordering = ['created_on']
        unique_together = ('poster','list','created_on')
    
    def __str__(self):
        return f"Posted by {self.poster} on listing {self.list.title}"

class Notifications(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name="notificationTo")
    message = models.TextField()
    date = models.DateTimeField(default=datetime.now)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f"{self.user}, {self.date}"