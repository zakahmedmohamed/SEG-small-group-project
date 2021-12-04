"""Unit tests for the Club model."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from clubs.models import Club

#Create your tests here
class clubModelTestCase(TestCase):
    """Unit tests for the club model."""

    fixtures = ["clubs/tests/fixtures/clubs.json"]

    def setUp(self):
        self.club = Club.objects.get(name = 'TheGrand')

    def test_valid_club(self):
        self._assert_club_is_valid()

    def test_club_name_must_not_be_blank(self):
        self.club.name = ''
        self._assert_club_is_invalid()

    def test_description_need_not_be_unique(self):
        second_club = self._create_second_club()
        self.club.description = second_club.description
        self._assert_club_is_valid()

    def test_description_may_contain_520_characters(self):
        self.club.description = 'x' * 520
        self._assert_club_is_valid()

    def test_description_must_not_contain_more_than_520_characters(self):
        self.club.description = 'x' * 521
        self._assert_club_is_invalid()

    def test_location_can_be_blank(self):
        self.club.description = ''
        self._assert_club_is_valid()

    def test_location_need_not_be_unique(self):
        second_club = self._create_second_club()
        self.club.location = second_club.location
        self._assert_club_is_valid()

    def test_location_may_contain_20_characters(self):
        self.club.location = 'x' * 20
        self._assert_club_is_valid()

    def test_location_must_not_contain_more_than_20_characters(self):
        self.club.location = 'x' * 21
        self._assert_club_is_invalid()

    def test_location_must_not_be_blank(self):
        self.club.location = ''
        self._assert_club_is_invalid()

    def test_club_name_must_not_be_blank(self):
        self.club.name = ''
        self._assert_club_is_invalid()

    def test_club_name_must_be_unique(self):
        second_club = self._create_second_club()
        self.club.name = second_club.name
        self._assert_club_is_invalid()

    def _assert_club_is_valid(self):
        try:
            self.club.full_clean()
        except (ValidationError):
            self.fail('Test club should be valid')

    def _assert_club_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.club.full_clean()

    def _create_second_club(self):
        second_club = Club.objects.get(name = 'Club2')
        return second_club
