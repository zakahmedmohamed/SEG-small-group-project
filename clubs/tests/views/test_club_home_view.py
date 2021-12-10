from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from clubs.models import User, Club, UserClubs
from clubs.tests.helpers import reverse_with_next

class Club_Home_Test(TestCase):

    fixtures = [
        'clubs/tests/fixtures/users.json',
        'clubs/tests/fixtures/clubs.json'
    ]

    def setUp(self):
        self.owner_user = User.objects.get(username='janedoe@example.org')
        self.officer_user = User.objects.get(username='janedoe1@example.org')
        self.member_user = User.objects.get(username='janedoe2@example.org')
        self.club = Club.objects.get(name = "TheGrand")
        self.owner_user_club = UserClubs.objects.create(user = self.owner_user, club = self.club, is_member = True, is_officer = True, is_owner = True)
        self.officer_user_club = UserClubs.objects.create(user = self.officer_user, club = self.club, is_member = True, is_officer = True, is_owner = False)
        self.member_user_club = UserClubs.objects.create(user = self.member_user, club = self.club, is_member = True, is_officer = False, is_owner = False)
        self.url = reverse('club_home', kwargs={'club_name': self.club.name})

    def test_show_user_url(self):
        self.assertEqual(self.url,f'/club_home/{self.club.name}/')

    def test_get_show_club_home_with_valid_owner_user(self):
        self.client.login(username=self.owner_user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'club_home.html')
        self.assertContains(response, "View Members!")
        self.assertContains(response, "Approve or reject applications!")
        self.assertContains(response, "Promote, demote or tranfer ownership as the club's owner")

    def test_get_show_club_home_with_valid_officer_user(self):
        self.client.login(username=self.officer_user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'club_home.html')
        self.assertContains(response, "View Members!")
        self.assertContains(response, "Approve or reject applications!")
        self.assertNotContains(response, "Promote, demote or tranfer ownership as the club's owner")

    def test_get_show_club_home_with_valid_member_user(self):
        self.client.login(username=self.member_user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'club_home.html')
        self.assertContains(response, "View Members!")
        self.assertNotContains(response, "Approve or reject applications!")
        self.assertNotContains(response, "Promote, demote or tranfer ownership as the club's owner")

    def test_get_club_profile_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
