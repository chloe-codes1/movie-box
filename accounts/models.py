from django.db import models
from django.contrib.auth.models import AbstractUser
from movies.models import Genre, Movie
import random
import hashlib
# Create your models here.

class User(AbstractUser):
    
    @property
    def gravatar_url(self):
        return f"https://s.gravatar.com/avatar/{hashlib.md5(self.email.encode('utf-8').strip().lower()).hexdigest()}?s=50&d=mp"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorites = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)