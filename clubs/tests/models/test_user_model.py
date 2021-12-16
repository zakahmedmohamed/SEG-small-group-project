"""Unit tests for the User model."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from clubs.models import User, Club, Membership

class UserModelTestCase(TestCase):
    """Unit tests for the User model."""

    fixtures = ["clubs/tests/fixtures/users.json", "clubs/tests/fixtures/clubs.json"]

    def setUp(self):
        self.user = User.objects.get(username = 'janedoe@example.org')
        self.club = Club.objects.get(name = 'TheGrand')

    def test_valid_user(self):
        self._assert_user_is_valid()

    def test_xp_cannot_be_less_than_zero(self):
        self.user.chess_xp = -1
        self._assert_user_is_invalid()

    def test_first_name_must_not_be_blank(self):
        self.user.first_name = ''
        self._assert_user_is_invalid()

    def test_first_name_need_not_be_unique(self):
        second_user = self._create_second_user()
        self.user.first_name = second_user.first_name
        self._assert_user_is_valid()

    def test_first_name_may_contain_50_characters(self):
        self.user.first_name = 'x' * 50
        self._assert_user_is_valid()

    def test_first_name_must_not_contain_more_than_50_characters(self):
        self.user.first_name = 'x' * 51
        self._assert_user_is_invalid()


    def test_last_name_must_not_be_blank(self):
        self.user.last_name = ''
        self._assert_user_is_invalid()

    def test_last_name_need_not_be_unique(self):
        second_user = self._create_second_user()
        self.user.last_name = second_user.last_name
        self._assert_user_is_valid()

    def test_last_name_may_contain_50_characters(self):
        self.user.last_name = 'x' * 50
        self._assert_user_is_valid()

    def test_last_name_must_not_contain_more_than_50_characters(self):
        self.user.last_name = 'x' * 51
        self._assert_user_is_invalid()

    def test_personal_statement_must_not_contain_more_than_1000_characters(self):
        self.user.last_name = 'x' * 1001
        self._assert_user_is_invalid()


    def test_username_must_not_be_blank(self):
        self.user.username = ''
        self._assert_user_is_invalid()

    def test_username_must_be_unique(self):
        second_user = self._create_second_user()
        self.user.username = second_user.username
        self._assert_user_is_invalid()


    def test_username_must_contain_at_symbol(self):
        self.user.username = 'johndoe.example.org'
        self._assert_user_is_invalid()

    def test_username_must_contain_domain_name(self):
        self.user.username = 'johndoe@.org'
        self._assert_user_is_invalid()

    def test_username_must_contain_domain(self):
        self.user.username = 'johndoe@example'
        self._assert_user_is_invalid()

    def test_username_must_not_contain_more_than_one_at(self):
        self.user.username = 'johndoe@@example.org'
        self._assert_user_is_invalid()


    def test_bio_may_be_blank(self):
        self.user.bio = ''
        self._assert_user_is_valid()

    def test_statement_may_be_blank(self):
        self.user.statement = ''
        self._assert_user_is_invalid()

    def test_bio_need_not_be_unique(self):
        second_user = self._create_second_user()
        self.user.bio = second_user.bio
        self._assert_user_is_valid()

    def test_bio_may_contain_520_characters(self):
        self.user.bio = 'x' * 520
        self._assert_user_is_valid()

    def test_bio_must_not_contain_more_than_520_characters(self):
        self.user.bio = 'x' * 521
        self._assert_user_is_invalid()

    def test_user_can_apply_for_a_club(self):
        self.client.login(username=self.user.username, password='Password123')
        beforeExists = Membership.objects.filter(user = self.user, club = self.club).exists()
        beforeCount = Membership.objects.count()
        self.user.apply_club(self.club)
        afterExists = Membership.objects.filter(user = self.user, club = self.club).exists()
        afterCount = Membership.objects.count()
        self.assertFalse(beforeExists)
        self.assertTrue(afterExists)
        self.assertEqual(beforeCount + 1, afterCount)

    def test_user_can_make_club_owner(self):
        self.client.login(username=self.user.username, password='Password123')
        beforeExists = Membership.objects.filter(user = self.user, club = self.club).exists()
        beforeCount = Membership.objects.count()
        self.user.make_club_owner(self.club)
        afterExists = Membership.objects.filter(user = self.user, club = self.club).exists()
        afterMember = Membership.objects.get(user = self.user, club = self.club).is_member
        afterOfficer = Membership.objects.get(user = self.user, club = self.club).is_officer
        afterOwner = Membership.objects.get(user = self.user, club = self.club).is_owner
        afterCount = Membership.objects.count()
        self.assertFalse(beforeExists)
        self.assertTrue(afterExists)
        self.assertTrue(afterMember)
        self.assertTrue(afterOfficer)
        self.assertTrue(afterOwner)
        self.assertEqual(beforeCount + 1, afterCount)

    def _assert_user_is_valid(self):
        try:
            self.user.full_clean()
        except (ValidationError):
            self.fail('Test user should be valid')

    def _assert_user_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.user.full_clean()

    def _create_second_user(self):
        second_user = User.objects.get(username = 'janedoe1@example.org')
        return second_user