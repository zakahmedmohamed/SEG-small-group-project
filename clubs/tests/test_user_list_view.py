from django.test import TestCase
from django.urls import reverse
from clubs.models import User
from .helpers import LogInTester

class UserListTest(TestCase, LogInTester):
    def setUp(self):
        self.url = reverse('user_list')
        self.user = User.objects.create_user(
            username ='Johndoe@example.org',
            first_name ='John',
            last_name ='Doe',
            bio ='Hello, I am John Doe.',
            statement ='hi',
            password ='Password123',
            chess_xp = 10,
            is_member = True,
        )

    def test_user_list_url(self):
        self.assertEqual(self.url,'/users/')

    def test_get_user_list(self):
        self.client.login(username = self.user.username, password = "Password123")
        self.assertTrue(self._is_logged_in())
        self._create_test_users(15)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_list.html')
        self.assertEqual(len(response.context['users']), 16)
        for user_id in range(15):
<<<<<<< HEAD
            self.assertContains(response, f'user{user_id}@example.org')
            self.assertContains(response, f'First{user_id}')
            self.assertContains(response, f'Last{user_id}')

    def _create_test_users(self, user_count):
=======
            self.assertContains(response, f'@user{user_id}')
            self.assertContains(response, user_id)

    def _create_test_users(self, user_count=15):
>>>>>>> 5482408b51701ae53586139b439490d00c520133
        for user_id in range(user_count):
            User.objects.create_user(
                f'user{user_id}@example.org',
                password='Password123',
                first_name=f'First{user_id}',
                last_name=f'Last{user_id}',
<<<<<<< HEAD
                bio=f'Bio {user_id}',
                statement = f'Statement {user_id}',
                chess_xp = 10,
                is_member = True,
                is_owner = False,
                is_officer = False,
=======
                bio=f'Bio{user_id}',
                statement = f'Statement{user_id}',
                chess_xp = user_id,
                is_member = True,
                is_officer = True,
                is_owner = False,
>>>>>>> 5482408b51701ae53586139b439490d00c520133
            )
