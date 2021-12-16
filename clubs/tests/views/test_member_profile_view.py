from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from clubs.models import User, Club, Membership
from clubs.tests.helpers import LogInTester

class ShowUserTest(TestCase, LogInTester):
    fixtures = ['clubs/tests/fixtures/clubs.json', 'clubs/tests/fixtures/users.json']

    def setUp(self):
        self.club1 = Club.objects.get(name = 'TheGrand')
        self.user = User.objects.get(username = 'janedoe@example.org')

        self.club_user = Membership.objects.create(
            user = self.user,
            club = self.club1,
            is_applicant = True,
            is_member = True,
            is_officer = True,
            is_owner = True
        )

        self.club_user.save()
        self.club2 = Club.objects.get(name = 'TheGrand')

        self.club_user2 = Membership.objects.create(
            user = self.user,
            club = self.club2,
            is_applicant = True,
            is_member = True,
            is_officer = False,
            is_owner = False
        )

        self.club2 = Club.objects.get(name = 'ClubB')
        self.club_user2.save()

        Membership(user = self.user, club = self.club2, is_applicant = True, is_member = True, is_officer = True, is_owner = True).save()
        self.url = reverse('member_profile', kwargs = {'user_id': self.user.id})

    def test_show_user_url(self):
        self.assertEqual(self.url,f'/member_profile/{self.user.id}/')

    def test_get_show_user_with_valid_id(self):
        self.client.login(username = self.user.username, password = "Password123")
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'member_profile.html')
        self.assertContains(response, "Jane Doe")
        self.assertContains(response, "janedoe@example.org")
        self.assertContains(response, 100)
        self.assertContains(response, "My bio")
        self.assertContains(response, "My statement")
        self.assertContains(response, "TheGrand")
        self.assertContains(response, "London")
        self.assertContains(response, "The best")
        self.assertContains(response, "ClubB")
        self.assertContains(response, "London")
        self.assertContains(response, "Second best")

    def test_get_show_user_with_invalid_id(self):
        self.client.login(username = self.user.username, password = "Password123")
        self.assertTrue(self._is_logged_in())
        url = reverse('member_profile', kwargs={'user_id': self.user.id+1})
        response = self.client.get(url, follow=True)
        response_url = reverse('my_clubs')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'my_clubs.html')
