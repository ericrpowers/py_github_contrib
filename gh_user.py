import gh_api


class Users:
    def __init__(self):
        self.__user_list = []

    def get_user_list(self):
        return self.__user_list

    def add_new_user(self, username):
        if username and len([user for user in self.__user_list if user['username'] == username]) == 0:
            if gh_api.is_user(username):
                self.__user_list.append({
                    'username': username,
                    'contributions': gh_api.get_contributions(username)
                })
                return True
        return False

    def get_contributions(self, username, start, end, refetch=False):
        if not username:
            return []
        user = [user for user in self.__user_list if user['username'] == username]
        if len(user) == 0:
            return []
        user = user[0]
        if refetch is True:
            user['contributions'] = gh_api.get_contributions(username)

        if not (start and end):
            return user['contributions']
        start_index = 364 - (gh_api.CURRENT_DATE - gh_api.parser.parse(start)).days
        end_index = 364 - (gh_api.CURRENT_DATE - gh_api.parser.parse(end)).days
        return [user['contributions'][i] for i in xrange(start_index, end_index + 1)]

    def remove_user(self, username):
        user = [user for user in self.__user_list if user['username'] == username]
        if len(user) == 0:
            return False
        self.__user_list.remove(user[0])
        return True
