from django.test import TestCase
from django.urls import reverse
from clubs.models import User
from clubs.tests.helpers import LogInTester

class UserListTest(TestCase, LogInTester):
    fixtures = ["clubs/tests/fixtures/users.json"]

    def setUp(self):
        self.user = User.objects.get(username = 'janedoe@example.org')
        self.url = reverse('user_list')

    def test_user_list_url(self):
        self.assertEqual(self.url,'/users/')

    # def test_get_user_list(self):
    #     self.client.login(username = self.user.username, password = "Password123")
    #     self.assertTrue(self._is_logged_in())
    #     self._create_test_users(15)
    #     response = self.client.get(self.url)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'user_list.html')
    #     self.assertEqual(len(response.context['users']), 17)
    #     for user_id in range(15):
    #         self.assertContains(response, f'user{user_id}@example.org')
    #         self.assertContains(response, f'First{user_id}')
    #         self.assertContains(response, f'Last{user_id}')

    def _create_test_users(self, user_count):
        for user_id in range(user_count):
            User.objects.create_user(
                f'user{user_id}@example.org',
                password='Password123',
                first_name=f'First{user_id}',
                last_name=f'Last{user_id}',
                bio=f'Bio {user_id}',
                statement = f'Statement {user_id}',
                chess_xp = 10,
            )
