"""Unit tests of the user form."""
from django import forms
from django.test import TestCase
from clubs.forms import UserForm
from clubs.models import User

class ChangeProfileFormTestCase(TestCase):
    """Unit tests of the user form."""

    fixtures = ['clubs/tests/fixtures/users.json']

    def setUp(self):
        self.form_input = {
            'first_name': 'Dias',
            'last_name': 'Nate',
            'username': 'dias@example.org',
            'bio': 'My bio',
            'statement': 'My statement',
            'chess_xp': 170
        }

    def test_form_has_necessary_fields(self):
        form = UserForm()
        self.assertIn('first_name', form.fields)
        self.assertIn('last_name', form.fields)
        self.assertIn('username', form.fields)
        self.assertIn('bio', form.fields)
        self.assertIn('statement', form.fields)
        self.assertIn('chess_xp', form.fields)
        email_field = form.fields['username']
        self.assertTrue(isinstance(email_field, forms.EmailField))

    def test_valid_user_form(self):
        form = UserForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_uses_model_validation(self):
        self.form_input['username'] = 'badusername'
        form = UserForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_must_save_correctly(self):
        user = User.objects.get(username='janedoe@example.org')
        form = UserForm(instance=user, data=self.form_input)
        before_count = User.objects.count()
        form.save()
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(user.username, 'dias@example.org')
        self.assertEqual(user.first_name, 'Dias')
        self.assertEqual(user.last_name, 'Nate')
        self.assertEqual(user.bio, 'My bio')
        self.assertEqual(user.statement, 'My statement')
        self.assertEqual(user.chess_xp, 170)
