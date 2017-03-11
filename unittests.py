from unittest import TestCase
from mock import patch
import datetime
import gh_user
import gh_api


class UserSetUp(TestCase):
    def setUp(self):
        with patch('__builtin__.raw_input', side_effect=['ericrpowers']):
            self.user = gh_user.User()


class TestGHUser(UserSetUp):
    # username
    def test_username(self):
        self.assertEqual(self.user.username(), 'ericrpowers')

    # get_new_user
    def test_get_new_user_invalid(self):
        with patch('__builtin__.raw_input', side_effect=['@!@_test_@!@', 'ericrpowers']):
            self.user.get_new_user()
            self.assertEqual(self.user._User__user_list['@!@_test_@!@'], None)

    def test_get_new_user_empty(self):
        with patch('__builtin__.raw_input', side_effect=['', 'ericrpowers']):
            self.user.get_new_user()
            self.assertEqual(self.user._User__user_list['ericrpowers'], [])

    def test_get_new_user_Dogild(self):
        with patch('__builtin__.raw_input', side_effect=['Dogild']):
            self.user.get_new_user()
            self.assertEqual(self.user._User__user_list['Dogild'], [])

    # get_contributions
    def test_get_contributions_year(self):
        self.assertEqual(len(self.user.get_contributions(None, None)), 365)

    def test_get_contributions_2_days(self):
        current_date = datetime.date.today()
        ten_days_prior = str((current_date - datetime.timedelta(days=1)))
        self.assertEqual(len(self.user.get_contributions(ten_days_prior, str(current_date))), 2)

    def test_get_contributions_1_days(self):
        current_date = str(datetime.date.today())
        self.assertEqual(len(self.user.get_contributions(current_date, current_date)), 1)

    def test_get_contributions_365_days(self):
        current_date = datetime.date.today()
        ten_days_prior = str((current_date - datetime.timedelta(days=364)))
        self.assertEqual(len(self.user.get_contributions(ten_days_prior, str(current_date))), 365)

    def test_get_contributions_364_days(self):
        current_date = datetime.date.today()
        ten_days_prior = str((current_date - datetime.timedelta(days=363)))
        self.assertEqual(len(self.user.get_contributions(ten_days_prior, str(current_date))), 364)


class TestGHAPI(TestCase):
    # is_user
    def test_is_user_valid(self):
        self.assertTrue(gh_api.is_user('ericrpowers'))

    def test_is_user_invalid(self):
        self.assertFalse(gh_api.is_user('@!@_test_@!@'))

    def test_is_user_empty(self):
        self.assertFalse(gh_api.is_user(''))

    # get_repos
    def test_get_repos_valid(self):
        self.assertTrue(len(gh_api.get_repos('ericrpowers')) >= 2)

    def test_get_repos_invalid(self):
        self.assertEqual(gh_api.get_repos('@!@_test_@!@'), None)

    def test_get_repos_empty(self):
        self.assertEqual(gh_api.get_repos(''), None)

    # get_contributions
    def test_get_contributions_invalid(self):
        self.assertEqual(gh_api.get_contributions('@!@_test_@!@'), [])

    def test_get_contributions_empty(self):
        self.assertEqual(gh_api.get_contributions(''), [])
