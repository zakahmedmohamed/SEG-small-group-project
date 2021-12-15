from django.test import TestCase
from django.urls import reverse
from clubs.models import User, Club, UserClubs
from clubs.tests.helpers import LogInTester

class ViewMembersTest(TestCase, LogInTester):
    fixtures = ["clubs/tests/fixtures/users.json", "clubs/tests/fixtures/clubs.json"]
    

    def setUp(self):
        self.user = User.objects.get(username = 'janedoe@example.org')
        self.club = Club.objects.get(name = 'TheGrand')
        self.member = UserClubs(user = self.user ,club = self.club, is_member = True, is_officer = True)
        self.member.save()
        self.url = reverse('view_members', kwargs={'club_name': self.member.club.name})


    def test_view_members_url(self):
        self.assertEqual(self.url,f'/view_members/{self.member.club.name}/')

    def test_get_view_members_as_officer(self):
        self.client.login(username = self.user.username, password = "Password123")
        self.assertTrue(self._is_logged_in())
        self._create_test_users(15)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'view_members.html')
        #self.assertEqual(len(response.context['view_members']), 16)
        for user_id in range(15):
            self.assertContains(response, f'First{user_id}')
            self.assertContains(response, f'Last{user_id}')
            self.assertContains(response, f'Bio{user_id}')
            self.assertContains(response, f'user{user_id}@example.org')
            self.assertContains(response, f'Statement{user_id}')
            self.assertContains(response, f'Chess xp: {user_id}')


    def test_get_view_members_as_member(self):
        self.member.is_officer = False
        self.member.save()
        self.client.login(username = self.user.username, password = "Password123")
        self.assertTrue(self._is_logged_in())
        self._create_test_users(15)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'view_members.html')
        #self.assertEqual(len(response.context['view_members']), 16)
        for user_id in range(15):
            self.assertContains(response, f'First{user_id}')
            self.assertContains(response, f'Last{user_id}')
            self.assertContains(response, f'Bio{user_id}')
            self.assertNotContains(response, f'user{user_id}@example.org')
            self.assertNotContains(response, f'Statement{user_id}')
            self.assertNotContains(response, f'Chess xp: {user_id}')


    def _create_test_users(self, user_count):
        for user_id in range(user_count):
            user = User.objects.create_user(
                f'user{user_id}@example.org',
                password='Password123',
                first_name=f'First{user_id}',
                last_name=f'Last{user_id}',
                bio=f'Bio{user_id}',
                statement = f'Statement{user_id}',
                chess_xp = f'{user_id}',
            )
            user_club = UserClubs.objects.create(
            user = user,
            club = self.club,
            is_member = True,
            )
            user_club.save()
