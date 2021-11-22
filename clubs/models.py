from django.db import models
from django.db.models.base import Model
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
    is_member = models.BooleanField(default=False)
    is_owner = models.BooleanField(default=False)
    is_officer = models.BooleanField(default=False)

    def gravatar(self, size=120):
        """Return a URL to the user's gravatar."""
        gravatarObj = Gravatar(self.email)
        gravatarURL = gravatarObj.get_image(size=size, default='mp')
        return gravatarURL

class Club(models.Model):
    #The club consists of the club name, location, description
    name = models.CharField(max_length=20,blank=False,unique=True)
    description = models.CharField(max_length=120,blank=False,unique=False)
    location = models.CharField(max_length=20,blank=False,unique=False)



