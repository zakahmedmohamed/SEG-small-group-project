"""Referenced from clucker application"""
"""Tests of the sign up view."""
from django.contrib.auth.hashers import check_password
from django.test import TestCase
from django.urls import reverse
from clubs.forms import SignUpForm, Create_A_Club_Form
from clubs.models import User, Club, UserClubs
from clubs.tests.helpers import LogInTester

class Create_club_test(TestCase, LogInTester):

    fixtures = ["clubs/tests/fixtures/users.json"]

    """Tests of the sign up view."""
    def setUp(self):
        self.url = reverse('create_club')
        self.user = User.objects.get(username='janedoe@example.org')
        self.client.login(username=self.user.username, password='Password123')
        self.form_input = {
            'name': 'Club B',
            'description': 'This is Club B',
            'location': 'London',
        }

    def test_create_club_url(self):
        self.assertEqual(self.url,'/create_club/')

    def test_get_create_club(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_club.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, Create_A_Club_Form))
        self.assertFalse(form.is_bound)

    def test_unsuccesful_create_club(self):
        self.form_input['name'] = ''
        before_count = Club.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = Club.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_club.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, Create_A_Club_Form))
        self.assertTrue(form.is_bound)

    def test_succesful_create_club(self):
        before_count = Club.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = Club.objects.count()
        self.assertEqual(after_count, before_count+1)
        new_club = Club.objects.latest('created_at')
        club_user = UserClubs.objects.get(club = new_club, user = self.user)
        self.assertEqual(self.user, club_user.user)
        response_url = reverse('my_clubs')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'my_clubs.html')
        club = Club.objects.get(name='Club B')
        self.assertEqual(club.name, 'Club B')
        self.assertEqual(club.description, 'This is Club B')
        self.assertEqual(club.location, 'London')
