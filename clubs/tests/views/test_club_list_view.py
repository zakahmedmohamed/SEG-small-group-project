from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from clubs.models import User, Club, UserClubs
from clubs.tests.helpers import reverse_with_next

class ClubListTest(TestCase):

    fixtures = ['clubs/tests/fixtures/clubs.json', 'clubs/tests/fixtures/users.json']

    def setUp(self):
        self.url = reverse('club_list')
        self.club = Club.objects.get(name = 'TheGrand')
        self.user = User.objects.get(username = 'janedoe@example.org')
        self.club2 = Club.objects.get(name = 'ClubB')
        UserClubs(user = self.user, club = self.club, is_applicant = True, is_member = True, is_officer = True, is_owner = True).save()
        UserClubs(user = self.user, club = self.club2, is_applicant = True, is_member = True, is_officer = True, is_owner = True).save()

    def test_club_list_url(self):
        self.assertEqual(self.url,'/club_list/')

    def test_get_club_list(self):
        self.client.login(username=self.user.username, password='Password123')
        self._create_test_clubs(5)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'club_list.html')
        for club_id in range(5):
            self.assertContains(response, f'Club{club_id}')
            self.assertContains(response, f'The best{club_id}')
            club = Club.objects.all().get(name=f'Club{club_id}')
            club_url = reverse('club_profile', kwargs={'club_name': club.name})
            self.assertContains(response, club_url)

    def test_get_club_list_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def _create_test_clubs(self, club_count=5):
        for club_id in range(club_count):
            name=f'Club{club_id}'
            description=f'The best{club_id}'
            location='London'
            club = Club(name=name,description=description,location=location)
            club.save()
            UserClubs(user = self.user, club = club, is_member = True, is_officer = True, is_owner = True).save()
