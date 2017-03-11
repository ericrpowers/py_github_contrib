import gh_api


class User:
    def __init__(self):
        self.__username = None
        self.__user_list = {}
        self.get_new_user()

    def username(self):
        return self.__username

    def get_new_user(self):
        answer = None
        # Let's find out which user we will start off with
        while not answer:
            answer = raw_input("Which user would you like to look up? ").strip()
            if answer and answer not in self.__user_list:
                self.__user_list[answer] = [] if gh_api.is_user(answer) else None

            if answer and self.__user_list[answer] is not None:
                self.__username = answer
            else:
                answer = None
                print("Invalid input or non-existent user.")

    def get_contributions(self, start, end):
        if len(self.__user_list[self.__username]) == 0:
            self.__user_list[self.__username] = gh_api.get_contributions(self.__username)

        if not (start and end):
            return self.__user_list[self.__username]
        start_index = 364 - (gh_api.CURRENT_DATE - gh_api.parser.parse(start)).days
        end_index = 364 - (gh_api.CURRENT_DATE - gh_api.parser.parse(end)).days
        return [self.__user_list[self.__username][i] for i in xrange(start_index, end_index + 1)]
