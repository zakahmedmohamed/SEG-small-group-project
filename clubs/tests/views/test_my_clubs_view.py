from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from clubs.models import User, Club, Membership
from clubs.tests.helpers import reverse_with_next

class MyClubsTest(TestCase):

    fixtures = ['clubs/tests/fixtures/clubs.json', 'clubs/tests/fixtures/users.json']

    def setUp(self):
        self.club = Club.objects.get(name = 'TheGrand')
        self.user = User.objects.get(username = 'janedoe@example.org')
        self.no_club_user = User.objects.get(username = 'janedoe1@example.org')
        self.club_user = Membership.objects.create(
        user = self.user,
        club = self.club,
        is_applicant = True,
        is_member = True,
        is_officer = True,
        is_owner = True
        )
        self.club_user.save()
        self.url = reverse('my_clubs')

    def test_my_clubs_url(self):
        self.assertEqual(self.url,'/my_clubs/')

    def test_get_my_clubs_list(self):
        self.client.login(username=self.user.username, password='Password123')
        self._create_test_clubs(5)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'my_clubs.html')
        for club_id in range(5):
            self.assertNotContains(response, f'Club{club_id}')
            self.assertContains(response, self.club)
            my_club = Club.objects.all().get(name='TheGrand')
            club_url = reverse('club_home', kwargs={'club_name': my_club.name})
            self.assertContains(response, club_url)

    def test_get_user_empty_my_clubs(self):
        self.client.login(username=self.no_club_user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'my_clubs.html')
        self.assertContains(response, 'No clubs joined')
        self.assertContains(response, 'Please join or create a club')

    def test_get_my_clubs_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def _create_test_clubs(self, club_count=10):
        for club_id in range(club_count):
            name=f'Club{club_id}'
            description=f'The best{club_id}'
            location='London'
            club = Club(name=name,description=description,location=location)
            club.save()
