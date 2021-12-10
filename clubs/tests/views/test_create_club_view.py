from django.contrib.auth.hashers import check_password
from django.http import response
from django.test import TestCase
from django.urls import reverse
from clubs.forms import Create_A_Club_Form
from clubs.models import User, Club
from clubs.tests.helpers import LogInTester


class createCLubTestCase(TestCase):

    def setUp(self):
        self.url = reverse('create_club')
        self.forminput = {'name': 'test club','description': 'test description', 'location': 'london'}
        self.form_input = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'username': 'janedoe@example.org',
            'bio': 'My bio',
            'statement': 'My statement',
            'chess_xp': 100,
            'new_password': 'Password123',
            'password_confirmation': 'Password123'
        }

    def test_create_club_url(self):
        self.assertEquals(self.url, '/create_club/')

    def test_create_a_club_success(self):
        self.client.login(username= 'johndoe@example.org', password = 'Password123')
        response = self.client.post(self.url, self.form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_club.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, Create_A_Club_Form))

    def test_create_a_club_fail(self):
        self.client.login(username= 'johndoe@example.org', password = 'WrongPassword123')
        self.form_input['name'] = ""
        response = self.client.post(self.url, self.form_input, follow=True)
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
