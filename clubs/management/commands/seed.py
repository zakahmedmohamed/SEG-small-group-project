from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from clubs.models import User

class Command(BaseCommand):
    """The database seeder."""
    def __init__(self):
        super.__init__
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        print('seeding data...')
        self.generate_users()
        print('done.')

    def generate_users(self):
        userList = []
        jebediah = User.objects.create_user(
            first_name = 'Jebediah',
            last_name = 'Kerman',
            username = 'jeb@example.org',
            password = 'Password123',
            bio = "My name is jeb",
            statement = 'I guide others to treasure I cannot possess',
            chess_xp = 1,
            is_member = True,
            is_owner = False,
            is_officer = False
        )

        valentina = User.objects.create_user(
            first_name = 'Valentina',
            last_name = 'Kerman',
            username = 'val@example.org',
            password = 'Password123',
            bio = "My name is val",
            statement = 'I hate Tuesdays...',
            chess_xp = 2,
            is_member = True,
            is_owner = False,
            is_officer = True
        )

        billie = User.objects.create_user(
            first_name = 'Billie',
            last_name = 'Kerman',
            username = 'billie@example.org',
            password = 'Password123',
            bio = "Name's Bill",
            statement = 'Zzz',
            chess_xp = 3,
            is_member = True,
            is_owner = True,
            is_officer = True
        )
        userList.append(jebediah)
        userList.append(valentina)
        userList.append(billie)

        for i in range(20):
            user = User.objects.create_user(
                first_name = self.faker.first_name(),
                last_name = self.faker.last_name(),
                username = self.faker.email(),
                password = 'Password123',
                bio = self.faker.text(max_nb_chars=520),
                statement = self.faker.text(max_nb_chars=20),
                chess_xp = self.faker.random_digit(),
                is_member = self.faker.boolean(chance_of_getting_true=50),
                is_owner = False,
                is_officer = self.faker.boolean(chance_of_getting_true=30)
            )
            userList.append(user)

        for user in userList:
            user.full_clean()
            user.save()
