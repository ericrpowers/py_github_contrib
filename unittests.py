from unittest import TestCase
import datetime
import gh_user
import gh_api

Default_user = 'ericrpowers'


class UserSetUp(TestCase):
    def setUp(self):
        self.users = gh_user.Users()
        self.users.add_new_user(Default_user)


class TestGHUser(UserSetUp):
    # get_user_list
    def test_get_user_list(self):
        self.assertEqual(Default_user, self.users.get_user_list()[0]['username'])

    # add_new_user
    def test_add_new_user_invalid(self):
        self.users.add_new_user('@!@_test_@!@')
        self.assertEqual(1, len(self.users._Users__user_list))

    def test_add_new_user_empty(self):
        self.users.add_new_user('')
        self.assertEqual(1, len(self.users._Users__user_list))

    def test_add_new_user_Dogild(self):
        self.users.add_new_user('Dogild')
        self.assertEqual(2, len(self.users._Users__user_list))

    # get_contributions
    def test_get_contributions_year(self):
        self.assertEqual(365, len(self.users.get_contributions(Default_user, None, None)))

    def test_get_contributions_2_days(self):
        current_date = datetime.date.today()
        ten_days_prior = str((current_date - datetime.timedelta(days=1)))
        self.assertEqual(2, len(self.users.get_contributions(Default_user, ten_days_prior, str(current_date))))

    def test_get_contributions_1_days(self):
        current_date = str(datetime.date.today())
        self.assertEqual(1, len(self.users.get_contributions(Default_user, current_date, current_date)))

    def test_get_contributions_365_days(self):
        current_date = datetime.date.today()
        ten_days_prior = str((current_date - datetime.timedelta(days=364)))
        self.assertEqual(365, len(self.users.get_contributions(Default_user, ten_days_prior, str(current_date))))

    def test_get_contributions_364_days(self):
        current_date = datetime.date.today()
        ten_days_prior = str((current_date - datetime.timedelta(days=363)))
        self.assertEqual(364, len(self.users.get_contributions(Default_user, ten_days_prior, str(current_date))))

    # remove_user
    def test_remove_user_valid(self):
        if self.users.remove_user(Default_user) is False:
            self.assertFalse(True)
        self.assertEqual([], self.users.get_user_list())

    def test_remove_user_invalid(self):
        if self.users.remove_user('Dogild') is True:
            self.assertFalse(True)
        self.assertEqual(Default_user, self.users.get_user_list()[0]['username'])

    def test_remove_user_empty(self):
        if self.users.remove_user('') is True:
            self.assertFalse(True)
        self.assertEqual(Default_user, self.users.get_user_list()[0]['username'])

    def test_remove_user_double_remove(self):
        if self.users.remove_user(Default_user) is False:
            self.assertFalse(True)
        self.assertFalse(self.users.remove_user(Default_user))


class TestGHAPI(TestCase):
    # is_user
    def test_is_user_valid(self):
        self.assertTrue(gh_api.is_user(Default_user))

    def test_is_user_invalid(self):
        self.assertFalse(gh_api.is_user('@!@_test_@!@'))

    def test_is_user_empty(self):
        self.assertFalse(gh_api.is_user(''))

    # get_repos
    def test_get_repos_valid(self):
        self.assertTrue(len(gh_api.get_repos(Default_user)) >= 2)

    def test_get_repos_invalid(self):
        self.assertEqual(None, gh_api.get_repos('@!@_test_@!@'))

    def test_get_repos_empty(self):
        self.assertEqual(None, gh_api.get_repos(''))

    # get_contributions
    def test_get_contributions_invalid(self):
        self.assertEqual([], gh_api.get_contributions('@!@_test_@!@'))

    def test_get_contributions_empty(self):
        self.assertEqual([], gh_api.get_contributions(''))
