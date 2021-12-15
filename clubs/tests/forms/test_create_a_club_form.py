"""Referenced from clucker application"""
"""Unit tests of the club form."""
from django import forms
from django.test import TestCase
from clubs.forms import Create_A_Club_Form
from clubs.models import Club

class CreateAClubFormTestCase(TestCase):
    """Unit tests of the create a club form."""

    def setUp(self):
        self.form_input = {
            'name': 'ClubA',
            'description': 'The best',
            'location': 'London'
        }

    def test_valid_club_form(self):
        form = Create_A_Club_Form(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_has_necessary_fields(self):
        form = Create_A_Club_Form()
        self.assertIn('name', form.fields)
        self.assertIn('description', form.fields)
        self.assertIn('location', form.fields)

    def test_form_rejects_blank_club_name(self):
        self.form_input['name'] = ''
        form = Create_A_Club_Form(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_invalid_club_name(self):
        self.form_input['name'] = 'x' * 30
        form = Create_A_Club_Form(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_accepts_blank_description(self):
        self.form_input['description'] = ''
        form = Create_A_Club_Form(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_rejects_blank_location(self):
        self.form_input['location'] = ''
        form = Create_A_Club_Form(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_invalid_club_location(self):
        self.form_input['location'] = 'x' * 30
        form = Create_A_Club_Form(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_must_save_correctly(self):
        form = Create_A_Club_Form(data=self.form_input)
        before_count = Club.objects.count()
        form.save()
        after_count = Club.objects.count()
        self.assertEqual(after_count, before_count+1)
        club = Club.objects.get(name='ClubA')
        self.assertEqual(club.description, 'The best')
        self.assertEqual(club.location, 'London')
