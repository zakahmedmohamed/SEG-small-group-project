"""Tests of the access denied view."""
from django.test import TestCase
from django.urls import reverse
from clubs.models import User

class AcessDeniedTestCase(TestCase):
    """Tests of the access denied view."""

    fixtures = ["clubs/tests/fixtures/users.json"]

    def setUp(self):
        self.url = reverse('access_denied')
        self.user = User.objects.get(username='janedoe@example.org')

    def test_access_denied_url(self):
        self.assertEqual(self.url,'/access_denied/')

    def test_get_access_denied(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Error: You do not have access rights!")
        self.assertTemplateUsed(response, 'access_denied.html')