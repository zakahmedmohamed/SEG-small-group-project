from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from clubs.models import User, Club, Membership

class Command(BaseCommand):
    """The database seeder."""
    def __init__(self):
        super.__init__
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        print('seeding data...')
        self.generate_users()
        self.generate_clubs()
        self.generate_Membership()
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
        owner1 = User.objects.create_user(
            first_name = 'Bob',
            last_name = 'Doe',
            username = 'bob@example.org',
            password = 'Password123',
            bio = "Name's Bob",
            statement = 'Whooo',
            chess_xp = 10
        )
        owner2 = User.objects.create_user(
            first_name = 'Jane',
            last_name = 'Doe',
            username = 'jane@example.org',
            password = 'Password123',
            bio = "Name's Jane",
            statement = 'Thank you',
            chess_xp = 40
        )
        userList.append(jebediah)
        userList.append(valentina)
        userList.append(billie)
        userList.append(owner1)
        userList.append(owner2)

        
    def generate_clubs(self):
        club_list = []
        club1 = Club.objects.create(
            name = 'Kerbal Chess Club',
            description = 'This is kerbal chess club',
            location = 'New york'
        )
        club2 = Club.objects.create(
            name = 'The Grand',
            description = 'This is the grand',
            location = 'London'
        )
        club3 = Club.objects.create(
            name = 'Club B',
            description = 'This is club b',
            location = 'Bristol'
        )
        club4 = Club.objects.create(
            name = 'Dragonfly',
            description = 'This is Dragonfly',
            location = 'London'
        )
        club_list.append(club1)
        club_list.append(club2)
        club_list.append(club3)
        club_list.append(club4)
        
        for club in club_list:
            print(club.name)
            club.full_clean()
            club.save()
    
    def generate_Membership(self):
        Membership.objects.create(
            user = User.objects.get(username = 'jeb@example.org'),
            club = Club.objects.get(name = 'Kerbal Chess Club'),
            is_member= True,
            is_applicant= True,
            is_owner = False,
            is_officer = False
        )
        Membership.objects.create(
            user = User.objects.get(username = 'billie@example.org'),
            club = Club.objects.get(name = 'Kerbal Chess Club'),
            is_member= True,
            is_applicant= True,
            is_owner = True,
            is_officer = True
        )
        Membership.objects.create(
            user = User.objects.get(username = 'val@example.org'),
            club = Club.objects.get(name = 'Kerbal Chess Club'),
            is_member= True,
            is_applicant= True,
            is_owner = False,
            is_officer = True
        )
        Membership.objects.create(
            user = User.objects.get(username = 'jeb@example.org'),
            club = Club.objects.get(name = 'The Grand'),
            is_member= True,
            is_applicant= True,
            is_owner = False,
            is_officer = True
        )
        Membership.objects.create(
            user = User.objects.get(username = 'billie@example.org'),
            club = Club.objects.get(name = 'Club B'),
            is_member= True,
            is_applicant= True,
            is_owner = False,
            is_officer = False
        )
        Membership.objects.create(
            user = User.objects.get(username = 'val@example.org'),
            club = Club.objects.get(name = 'Dragonfly'),
            is_member= True,
            is_applicant= True,
            is_owner = True,
            is_officer = True
        )
        Membership.objects.create(
            user = User.objects.get(username = 'bob@example.org'),
            club = Club.objects.get(name = 'The Grand'),
            is_member= True,
            is_applicant= True,
            is_owner = True,
            is_officer = False
        )
        Membership.objects.create(
            user = User.objects.get(username = 'jane@example.org'),
            club = Club.objects.get(name = 'Club B'),
            is_member= True,
            is_applicant= True,
            is_owner = True,
            is_officer = True
        )
