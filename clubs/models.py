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
    chess_xp = models.IntegerField(validators = [MinValueValidator(0)], default=0)

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def gravatar(self, size=120):
        """Return a URL to the user's gravatar."""
        gravatar_object = Gravatar(self.username)
        gravatar_url = gravatar_object.get_image(size=size, default='mp')
        return gravatar_url

    def mini_gravatar(self):
        """Return a URL to a miniature version of the user's gravatar."""
        return self.gravatar(size=60)

    def __str__(self):
        return self.username

    def make_club_owner(self, new_club):
        club_user = UserClubs(user = self, club = new_club)
        club_user.is_member = True
        club_user.is_officer = True
        club_user.is_owner = True
        club_user.save()

    def apply_club(self, new_club):
        club_user = UserClubs(user = self, club = new_club)
        club_user.save()

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
    is_applicant = models.BooleanField(default=False)
    is_member = models.BooleanField(default=False)
    is_officer = models.BooleanField(default=False)
    is_owner = models.BooleanField(default=False)

    def promote_member(self, user):
        user.is_officer = True
        user.save()

    def demote_officer(self, user):
        user.is_officer = False
        user.save()

    def transfer_ownership(self, user):
        self.is_owner = False
        user.is_officer = True
        user.is_owner = True
        self.save()
        user.save()

    def approve_application(self,user):
        user.is_member = True
        user.save()

    def reject_application(self,user):
        if user.is_member == False:
            user.delete()
