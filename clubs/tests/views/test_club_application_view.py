from django.test import TestCase
from django.urls import reverse
from clubs.models import User, UserClubs, Club
from clubs.tests.helpers import reverse_with_next

class ShowUserTest(TestCase):

    fixtures = [
        'clubs/tests/fixtures/users.json',
        'clubs/tests/fixtures/clubs.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='janedoe@example.org')
        self.club = Club.objects.get(name = "TheGrand")
        self.url = reverse('club_application', kwargs={'club_name': self.club.name})

    def test_follow_toggle_url(self):
        self.assertEqual(self.url,f'/club_application/{self.club.name}/')

    def test_get_club_application_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def tests_apply_for_club(self):
        self.client.login(username=self.user.username, password='Password123')
        is_member_before = UserClubs.objects.filter(user = self.user, club = self.club).exists()
        self.user.apply_club(self.club)
        response = self.client.get(self.url)
        is_member_after = UserClubs.objects.filter(user = self.user, club = self.club).exists()
        self.assertFalse(is_member_before)
        self.assertTrue(is_member_after)
        response_url = reverse('club_list')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)

    def tests_apply_for_club_that_does_not_exist(self):
        self.client.login(username=self.user.username, password='Password123')
        wrong_url = reverse('club_application', kwargs={'club_name': "bad_club"})
        response = self.client.get(wrong_url)
        response_url = response_url = reverse('club_list')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        


    """def test_promote_user_who_is_already_officer(self):
        self.client.login(username=self.user.username, password='Password123')
        self.other_member.is_officer = True
        is_officer_before = self.other_member.is_officer
        self.member.promote_member(self.other_member)
        response = self.client.get(self.url, follow=True)
        is_officer_after = self.other_member.is_officer
        self.assertTrue(is_officer_before)
        self.assertTrue(is_officer_after)
        response_url = reverse('owner_commands', kwargs={'club_name': self.other_member.club.name})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'owner_commands.html')

    def test_get_follow_toggle_with_invalid_id(self):
        self.client.login(username=self.user.username, password='Password123')
        url = reverse('promote_member', kwargs={'club_name': self.other_member.club.name, 'user_id': self.other_user.id+9999})
        response = self.client.get(url, follow=True)
        response_url = reverse('owner_commands', kwargs={'club_name': self.other_member.club.name})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'owner_commands.html')"""