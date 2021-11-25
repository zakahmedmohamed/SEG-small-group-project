from django.db import models
from libgravatar import Gravatar
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, RegexValidator

#Create your models here.
class User(AbstractUser):
    """User model used for authentication and microblog authoring."""

    # username = models.CharField(
    #     max_length=30,
    #     unique=True,
    #     validators=[RegexValidator(
    #         regex=r'^@\w{3,}$',
    #         message='Username must consist of @ followed by at least three alphanumericals'
    #     )]
    # )
    # email = models.EmailField(unique=True, blank=False)

    username = models.EmailField(unique=True, blank=False)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    bio = models.CharField(max_length=520, blank=True)
    statement = models.CharField(max_length=1000, blank=False)
    chess_xp = models.IntegerField(validators = [MinValueValidator(0)], default=None)
    is_member = models.BooleanField(default=False)
    is_owner = models.BooleanField(default=False)
    is_officer = models.BooleanField(default=False)

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def gravatar(self, size=120):
        """Return a URL to the user's gravatar."""
        gravatar_object = Gravatar(self.email)
        gravatar_url = gravatar_object.get_image(size=size, default='mp')
        return gravatar_url

    def mini_gravatar(self):
        """Return a URL to a miniature version of the user's gravatar."""
        return self.gravatar(size=60)
