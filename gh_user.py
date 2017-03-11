import gh_api


class User:
    def __init__(self):
        self.__username, self.__cb = (None,) * 2
        self.get_new_user()

    def username(self):
        return self.__username

    def get_new_user(self):
        answer = None
        # Let's find out which user we will start off with
        while not answer:
            answer = raw_input("Which user would you like to look up? ").strip()

            if answer and gh_api.is_user(answer):
                self.__username = answer
            else:
                answer = None
                print("Invalid input or non-existent user")

    def get_contributions(self, start, end):
        if not self.__cb:
            self.__cb = gh_api.get_contributions(self.__username)

        if not (start and end):
            return self.__cb
        start_index = 364 - (gh_api.current_date - gh_api.parser.parse(start)).days
        end_index = 364 - (gh_api.current_date - gh_api.parser.parse(end)).days
        return [self.__cb[i] for i in xrange(start_index, end_index + 1)]
