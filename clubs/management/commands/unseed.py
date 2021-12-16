from django.core.management.base import BaseCommand, CommandError
from clubs.models import User,Club, Membership

class Command(BaseCommand):
        """The database unseeder."""
        def __init__(self):
            super().__init__()

        def handle(self, *args, **options):
            #print("TODO: The database unseeder will be added here...")
            user_set = User.objects.all()
            userClubs_set = Membership.objects.all()
            club_set = Club.objects.all()

            print('unseeding data...')
            for user in user_set.iterator():
                if user.is_superuser == False:
                    user.delete()
            for club in club_set.iterator():
                club.delete() 
            for userClub in userClubs_set.iterator():
                userClub.delete() 
            print('done.')
