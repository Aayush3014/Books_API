from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    authors = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255, blank=True, null=True)
    published_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    cover_image = models.URLField(blank=True, null=True)
    average_rating = models.FloatField(blank=True, null=True)
    ratings_count = models.IntegerField(blank=True, null=True)
    genre = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.title

class Recommendation(models.Model):
    book = models.ForeignKey(Book, on_delete=models.SET_NULL,null=True, blank=True, related_name='recommendations')
    user = models.CharField(max_length=200, null=True, blank=True)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} recommends {self.book.title}"

class Like(models.Model):
    recommendation = models.ForeignKey(Recommendation, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.recommendation.user}"
