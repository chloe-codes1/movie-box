from django.db import models
from django.contrib.auth.models import AbstractUser
from movies.models import Genre, Movie
import random
# Create your models here.

class User(AbstractUser):
    pass

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorites = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)