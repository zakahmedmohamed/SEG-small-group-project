from django.test import TestCase
from django.urls import reverse
from clubs.models import User, UserClubs, Club
from clubs.tests.helpers import reverse_with_next

class Club_application_test(TestCase):

    fixtures = [
        'clubs/tests/fixtures/users.json',
        'clubs/tests/fixtures/clubs.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='janedoe@example.org')
        self.user2 = User.objects.get(username='janedoe1@example.org')
        self.club = Club.objects.get(name = "TheGrand")
        self.club2 = Club.objects.get(name = 'ClubB')
        self.club_user = UserClubs.objects.create(
        user = self.user,
        club = self.club,
        is_applicant = True,
        is_member = True,
        is_officer = True,
        is_owner = True
        )
        UserClubs(user = self.user, club = self.club2, is_applicant = True, is_member = True, is_officer = True, is_owner = True).save()
        self.url = reverse('club_application', kwargs={'club_name': self.club.name})

    def test_club_application_url(self):
        self.assertEqual(self.url,f'/club_application/{self.club.name}/')

    def test_get_club_application_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def tests_apply_for_club(self):
        self.client.login(username=self.user2.username, password='Password123')
        is_applicant_before = UserClubs.objects.filter(user = self.user2, club = self.club).exists()
        self.user2.apply_club(self.club)
        response = self.client.get(self.url)
        is_applicant_after = UserClubs.objects.filter(user = self.user2, club = self.club).exists()
        self.assertFalse(is_applicant_before)
        self.assertTrue(is_applicant_after)
        response_url = reverse('club_list')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)

    def tests_apply_for_club_that_does_not_exist(self):
        self.client.login(username=self.user2.username, password='Password123')
        wrong_url = reverse('club_application', kwargs={'club_name': "bad_club"})
        response = self.client.get(wrong_url)
        response_url = response_url = reverse('club_list')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)

    def test_apply_for_applied_club(self):
        self.client.login(username=self.user.username, password='Password123')
        is_applicant_before = self.club_user.is_applicant
        self.user.apply_club(self.club)
        response = self.client.get(self.url, follow=True)
        is_applicant_after = self.club_user.is_applicant
        self.assertTrue(is_applicant_before)
        self.assertTrue(is_applicant_after)
        response_url = reverse('club_list')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'club_list.html')
