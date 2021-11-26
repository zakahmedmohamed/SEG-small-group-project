from django.db import models
from libgravatar import Gravatar
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, RegexValidator

#Create your models here.
class User(AbstractUser):
    """User model used for authentication and microblog authoring."""
    
    username = models.CharField(
        max_length=30,
        unique=True,
        validators=[RegexValidator(
            regex=r'^@\w{3,}$',
            message='Username must consist of @ followed by at least three alphanumericals'
        )]
    )
    email = models.EmailField(unique=True, blank=False)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    bio = models.CharField(max_length=520, blank=True)
    statement = models.CharField(max_length=1000, blank=False)
    chess_xp = models.IntegerField(validators = [MinValueValidator(0)], default=0)

    def gravatar(self, size=120):
        """Return a URL to the user's gravatar."""
        gravatarObj = Gravatar(self.email)
        gravatarURL = gravatarObj.get_image(size=size, default='mp')
        return gravatarURL

    def __str__(self):
        return self.username


class Club(models.Model):
    name = models.CharField(max_length=20, unique=True, blank=False)
    description = models.CharField(max_length=520, blank=True)
    location = models.CharField(max_length=20, blank=False)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.name

    class meta:
        ordering = ['created_at']

class UserClubs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    is_member = models.BooleanField(default=False)
    is_owner = models.BooleanField(default=False)
    is_officer = models.BooleanField(default=False)




    