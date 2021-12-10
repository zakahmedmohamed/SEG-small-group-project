from django.test import TestCase
from django.urls import reverse
from clubs.models import User, UserClubs, Club
from clubs.tests.helpers import reverse_with_next

class TransferOwnershipTest(TestCase):

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
        self.url = reverse('transfer_ownership', kwargs={'club_name': self.other_member.club.name, 'user_id': self.other_user.id})

    def test_transfer_ownership_url(self):
        self.assertEqual(self.url,f'/transfer_ownership/{self.other_member.club.name}/{self.other_user.id}')

    def test_get_transfer_ownership_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_transfer_ownership_as_owner(self):
        self.client.login(username=self.user.username, password='Password123')
        is_member_officer_before = self.member.is_officer
        is_member_owner_before = self.member.is_owner
        is_other_member_officer_before = self.other_member.is_officer
        is_other_member_owner_before = self.other_member.is_owner
        response = self.client.get(self.url, follow=True)
        self.member.transfer_ownership(self.other_member)
        is_member_officer_after = self.member.is_officer
        is_member_owner_after = self.member.is_owner
        is_other_member_officer_after = self.other_member.is_officer
        is_other_member_owner_after = self.other_member.is_owner
        self.assertTrue(is_member_officer_before)
        self.assertTrue(is_member_owner_before)
        self.assertFalse(is_other_member_officer_before)
        self.assertFalse(is_other_member_owner_before)
        self.assertTrue(is_member_officer_after)
        self.assertFalse(is_member_owner_after)
        self.assertTrue(is_other_member_officer_after)
        self.assertTrue(is_other_member_owner_after)
        response_url = reverse('club_home', kwargs={'club_name': self.other_member.club.name})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'club_home.html')

    def test_transfer_ownership_not_as_owner(self):
        self.client.login(username=self.other_user.username, password='Password123')
        is_member_officer_before = self.member.is_officer
        is_member_owner_before = self.member.is_owner
        is_other_member_officer_before = self.other_member.is_officer
        is_other_member_owner_before = self.other_member.is_owner
        response = self.client.get(self.url, follow=True)
        self.other_member.transfer_ownership(self.member)
        is_member_officer_after = self.member.is_officer
        is_member_owner_after = self.member.is_owner
        is_other_member_officer_after = self.other_member.is_officer
        is_other_member_owner_after = self.other_member.is_owner
        self.assertTrue(is_member_officer_before)
        self.assertTrue(is_member_owner_before)
        self.assertFalse(is_other_member_officer_before)
        self.assertFalse(is_other_member_owner_before)
        self.assertTrue(is_member_officer_after)
        self.assertTrue(is_member_owner_after)
        self.assertFalse(is_other_member_officer_after)
        self.assertFalse(is_other_member_owner_after)
        response_url = reverse('club_list')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'club_list.html')

    def test_get_ftransfer_ownership_with_invalid_id(self):
        self.client.login(username=self.user.username, password='Password123')
        url = reverse('transfer_ownership', kwargs={'club_name': self.other_member.club.name, 'user_id': self.other_user.id+9999})
        response = self.client.get(url, follow=True)
        response_url = reverse('club_home', kwargs={'club_name': self.other_member.club.name})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'club_home.html')