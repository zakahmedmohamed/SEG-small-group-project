from django.core.management.base import BaseCommand, CommandError
from clubs.models import User

class Command(BaseCommand):
        """The database unseeder."""
        def __init__(self):
            super().__init__()

        def handle(self, *args, **options):
            #print("TODO: The database unseeder will be added here...")
            user_set = User.objects.all()

            print('unseeding data...')
            for user in user_set.iterator():
                if user.is_superuser == False:
                    user.delete()
            print('done.')
