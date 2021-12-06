"""Unit tests of the log in form."""
from django import forms
from django.test import TestCase
from clubs.forms import Log_in_form
from clubs.models import User

class LogInFormTestCase(TestCase):
    """Unit tests of the log in form."""

    fixtures = ["clubs/tests/fixtures/users.json"]

    def setUp(self):
        self.form_input = {'username': 'janedoe@example.org', 'password': 'Password123'}

    def test_form_contains_required_fields(self):
        form = Log_in_form()
        self.assertIn('username', form.fields)
        self.assertIn('password', form.fields)
        password_field = form.fields['password']
        self.assertTrue(isinstance(password_field.widget,forms.PasswordInput))

    def test_form_accepts_valid_input(self):
        form = Log_in_form(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_rejects_blank_username(self):
        self.form_input['username'] = ''
        form = Log_in_form(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_blank_password(self):
        self.form_input['password'] = ''
        form = Log_in_form(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_accepts_incorrect_username(self):
        self.form_input['username'] = 'email.com'
        form = Log_in_form(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_accepts_incorrect_password(self):
        self.form_input['password'] = 'pwd'
        form = Log_in_form(data=self.form_input)
        self.assertTrue(form.is_valid())
