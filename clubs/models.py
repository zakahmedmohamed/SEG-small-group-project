from django.db import models

# Create your models here.
# class User(AbstractUser):
#     """User model used for authentication and microblog authoring."""

#     username = models.CharField(
#         max_length=30,
#         unique=True,
#         validators=[RegexValidator(
#             regex=r'^@\w{3,}$',
#             message='Username must consist of @ followed by at least three alphanumericals'
#         )]
#     )
#     first_name = models.CharField(max_length=50, blank=False)
#     last_name = models.CharField(max_length=50, blank=False)
#     email = models.EmailField(unique=True, blank=False)
