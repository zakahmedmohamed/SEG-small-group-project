from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from clubs.models import User, Club, UserClubs

class Command(BaseCommand):
    """The database seeder."""
    def __init__(self):
        super.__init__
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        print('seeding data...')
        self.generate_users()
        self.generate_clubs()
        self.generate_UserClubs()
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
        )

        valentina = User.objects.create_user(
            first_name = 'Valentina',
            last_name = 'Kerman',
            username = 'val@example.org',
            password = 'Password123',
            bio = "My name is val",
            statement = 'I hate Tuesdays...',
            chess_xp = 2
        )

        billie = User.objects.create_user(
            first_name = 'Billie',
            last_name = 'Kerman',
            username = 'billie@example.org',
            password = 'Password123',
            bio = "Name's Bill",
            statement = 'Zzz',
            chess_xp = 3
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
                chess_xp = self.faker.random_digit()
            )
            userList.append(user)

        for user in userList:
            user.full_clean()
            user.save()
        
    def generate_clubs(self):
        club_list = []
        Somalia = Club.objects.create(
            name = 'Somalia',
            description = 'This is Somalia',
            location = 'Somalia'
        )
        Bangladesh = Club.objects.create(
            name = 'Bangladesh',
            description = 'This is Bangladesh',
            location = 'Bangladesh'
        )
        club_list.append(Somalia)
        club_list.append(Bangladesh)
        
        for club in club_list:
            print(club.name)
            club.full_clean()
            club.save()
    
    def generate_UserClubs(self):
        user_clubs_list = []
        OwnerOne = UserClubs.objects.create(
            user = User.objects.get(username = 'jeb@example.org'),
            club = Club.objects.get(name = 'Bangladesh'),
            is_applicant = False,
            is_member= False,
            is_owner = True,
            is_officer = False
        )
        OwnerOne = UserClubs.objects.create(
            user = User.objects.get(username = 'billie@example.org'),
            club = Club.objects.get(name = 'Somalia'),
            is_applicant = False,
            is_member= False,
            is_owner = True,
            is_officer = False
        )

