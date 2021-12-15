from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from clubs.models import User, Club, UserClubs

class Command(BaseCommand):
    """The database seeder."""
    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        print('seeding data...')
        self.generate_users()
        self.generate_clubs()
        self.generate_UserClubs()
        print('done.')

    """Create 3 fixed users as specified in the project specificaion.
    These users' information should remain the same through
     the proccess of seeding and unseeding"""
    def fixedUsers(self, list):
        list = []
        jebediah = User.objects.create_user(
            first_name = 'Jebediah',
            last_name = 'Kerman',
            username = 'jeb@example.org',
            password = 'Password123',
            bio = self.faker.text(max_nb_chars=520),
            statement = self.faker.text(max_nb_chars=20),
            chess_xp = 1,
        )

        valentina = User.objects.create_user(
            first_name = 'Valentina',
            last_name = 'Kerman',
            username = 'val@example.org',
            password = 'Password123',
            bio = self.faker.text(max_nb_chars=520),
            statement = self.faker.text(max_nb_chars=20),
            chess_xp = 2
        )

        billie = User.objects.create_user(
            first_name = 'Billie',
            last_name = 'Kerman',
            username = 'billie@example.org',
            password = 'Password123',
            bio = self.faker.text(max_nb_chars=520),
            statement = self.faker.text(max_nb_chars=20),
            chess_xp = 3
        )

        list.append(jebediah)
        list.append(valentina)
        list.append(billie)

        return list

    """Create users using faker as a user's information"""
    def generate_users(self):
        userList = []
        self.fixedUsers(userList)
        for i in range(60):
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

    """Create 3 fixed club as specified in the project specificaion.
    The club's information should remain the same through
     the proccess of seeding and unseeding"""
    def fixedClubs(self, list):
        list = []
        kerbalChessClub = Club.objects.create(
            name = 'Kerbal Chess Club',
            description = 'Yooo mr.White, its Kerbal yo.',
            location = 'London'
        )

        list.append(kerbalChessClub)

        return list

    """Create users using faker as a club's information"""
    def generate_clubs(self):
        club_list = []
        self.fixedClubs(club_list)

        for i in range(20):
            clubs = Club.objects.create(
                name = self.faker.city() + ' Chess Club',
                description = self.faker.text(max_nb_chars=520),
                location = self.faker.city()
            )

        for club in club_list:
            club.full_clean()
            club.save()

    """Create 3 fixed club as specified in the project specificaion.
    The club's information should remain the same through
     the proccess of seeding and unseeding"""
    def fixedMemberships(self, list):
        list = []
        membershipOne = UserClubs.objects.create(
            user = User.objects.get(username = 'jeb@example.org'),
            club = Club.objects.get(pk = 1),
            is_applicant = False,
            is_member= False,
            is_owner = False,
            is_officer = True
        )
        membershipTwo = UserClubs.objects.create(
            user = User.objects.get(username = 'val@example.org'),
            club = Club.objects.get(pk = 2),
            is_applicant = False,
            is_member= False,
            is_owner = True,
            is_officer = False
        )
        membershipThree = UserClubs.objects.create(
            user = User.objects.get(username = 'billie@example.org'),
            club = Club.objects.get(pk = 3),
            is_applicant = False,
            is_member= True,
            is_owner = False,
            is_officer = False
        )

        list.append(membershipOne)
        list.append(membershipTwo)
        list.append(membershipThree)

        return list

    """Create users using faker as a club membership's information"""
    def generate_UserClubs(self):
        user_clubs_list = []
        self.fixedMemberships(user_clubs_list)

        for i in range(4, 41):
            membership = UserClubs.objects.create(
                user = User.objects.get(pk = i),
                club = Club.objects.get(pk = i),
                is_member = self.faker.boolean(chance_of_getting_true=25),
                is_owner = self.faker.boolean(chance_of_getting_true=25),
                is_officer = self.faker.boolean(chance_of_getting_true=25)
            )

            user_club_list.append(membership)

        for membership in user_club_list:
            membership.full_clean()
            membership.save()
