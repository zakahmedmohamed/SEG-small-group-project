from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from clubs.models import User, Club, UserClubs
from clubs.tests.helpers import reverse_with_next

"""class OwnerCommandsTest(TestCase):

    fixtures = ['clubs/tests/fixtures/clubs.json', 'clubs/tests/fixtures/users.json']

    def setUp(self):
        self.club = Club.objects.get(name = 'TheGrand')
        self.user = User.objects.get(username = 'janedoe@example.org')
        self.club_user = UserClubs.objects.create(
        user = self.user,
        club = self.club,
        is_applicant = True,
        is_member = True,
        is_officer = True,
        is_owner = True
        )
        self.club_user.save()
        self.user2 = User.objects.get(username = 'janedoe1@example.org')
        self.club_user2 = UserClubs.objects.create(
        user = self.user2,
        club = self.club,
        is_applicant = False,
        is_member = False,
        is_officer = False,
        is_owner = False
        )
        self.club_user2.save()
        self.club2 = Club.objects.get(name = 'ClubB')
        UserClubs(user = self.user, club = self.club2, is_member = True, is_officer = True, is_owner = True).save()
        self.url = reverse('owner_commands', kwargs = {'club_name': self.club.name})

    def test_owner_commands_url(self):
        self.assertEqual(self.url,f'/owner_commands/{self.club.name}/')

    def test_get_owner_commands(self):
        self.client.login(username=self.user.username, password='Password123')
        self._create_test_applicants(5)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'owner_commands.html')
        for user_id in range(5):
            self.assertContains(response, f'user{user_id}@example.org')
            self.assertContains(response, f'First{user_id}')
            self.assertContains(response, f'Last{user_id}')
            self.assertContains(response, f'Is officer: True')
            self.assertContains(response, f'Is owner: False')

    def test_empty_owner_commands(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'owner_commands.html')
        self.assertContains(response, 'No members to execute commands')

    def test_get_owner_commands_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_owner_commands_as_not_owner_fails(self):
        self.club_user2.is_applicant=True
        self.club_user2.is_member=True
        self.club_user2.is_officer=True
        self.club_user2.save()
        self.client.login(username=self.user2.username, password='Password123')
        response = self.client.get(self.url)
        redirect_url = reverse('club_list')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def _create_test_applicants(self, user_count=5):
        for user_id in range(user_count):
            self.user = User.objects.create_user(
                f'user{user_id}@example.org',
                password='Password123',
                first_name=f'First{user_id}',
                last_name=f'Last{user_id}',
                bio=f'Bio{user_id}',
                statement = f'Statement{user_id}',
                chess_xp = user_id
            )
            self.club_user = UserClubs.objects.create(
            user = self.user,
            club = self.club,
            is_member = True,
            is_officer = True
            )
            self.club_user.save()
"""