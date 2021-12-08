from django.test import TestCase
from django.urls import reverse
from clubs.models import User
from clubs.tests.helpers import reverse_with_next

class ShowUserTest(TestCase):

    fixtures = ['clubs/tests/fixtures/users.json']

    def setUp(self):
        self.user = User.objects.get(username='janedoe@example.org')
        self.user = User.objects.get(username='janedoe1@example.org')
        self.url = reverse('promote_member', kwargs={'club_name': self.other_user.club.name, 'user_id': self.other_user.id})
