from django.test import TestCase
from django.urls import reverse
from clubs.models import User, UserClubs, Club
from clubs.tests.helpers import reverse_with_next

class promote_member_test(TestCase):

    fixtures = [
        'clubs/tests/fixtures/users.json',
        'clubs/tests/fixtures/clubs.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='janedoe@example.org')
        self.other_user = User.objects.get(username='janedoe1@example.org')
        self.club = Club.objects.get(name = "TheGrand")
        self.member = UserClubs(user = self.user ,club = self.club, is_member = True, is_officer = True, is_owner = True)
        self.member.save()
        self.other_member = UserClubs(user = self.other_user ,club = self.club, is_member = True)
        self.other_member.save()
        self.url = reverse('promote_member', kwargs={'club_name': self.other_member.club.name, 'user_id': self.other_user.id})

    def test_promote_member_url(self):
        self.assertEqual(self.url,f'/promote_member/{self.other_member.club.name}/{self.other_user.id}')

    def test_get_promote_member_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_promote_user_who_is_member(self):
        self.client.login(username=self.user.username, password='Password123')
        is_officer_before = self.other_member.is_officer
        self.member.promote_member(self.other_member)
        response = self.client.get(self.url, follow=True)
        is_officer_after = self.other_member.is_officer
        self.assertFalse(is_officer_before)
        self.assertTrue(is_officer_after)
        response_url = reverse('owner_commands', kwargs={'club_name': self.other_member.club.name})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'owner_commands.html')

    def test_promote_user_who_is_already_officer(self):
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

    def test_get_promote_member_with_invalid_id(self):
        self.client.login(username=self.user.username, password='Password123')
        url = reverse('promote_member', kwargs={'club_name': self.other_member.club.name, 'user_id': self.other_user.id+9999})
        response = self.client.get(url, follow=True)
        response_url = reverse('owner_commands', kwargs={'club_name': self.other_member.club.name})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'owner_commands.html')
