from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

# Create your models here.

class StreamingPlatform(models.Model):
    name = models.CharField(max_length=30)
    about = models.CharField(max_length=100)
    website = models.URLField(max_length=100)
    
    def __str__(self) -> str:
        return self.name
    

class WatchList(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    platform = models.ForeignKey(
        StreamingPlatform,
        on_delete=models.CASCADE,
        related_name="watchlist"
        )
    avg_rating = models.FloatField(default=0)
    total_reviews = models.IntegerField(default=0)
    def __str__(self) -> str:
        return self.title


class Review(models.Model):
    rating = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
            ]
        )
    review = models.CharField(max_length=200, null=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    watchlist = models.ForeignKey(
        WatchList,
        on_delete=models.CASCADE,
        related_name="reviews"
        )
    review_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="review_user")
    
    def __str__(self) -> str:
        return str(self.rating) + " | " + self.watchlist.title + " | " + str(self.review_user)