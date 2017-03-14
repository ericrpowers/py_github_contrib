import gh_user


def main():
    print "*~*~*~* GitHub User Contribution Retriever *~*~*~*"
    user_list = gh_user.Users()
    username = None

    while True:
        if username is None:
            username = __get_new_user(user_list)
        # Decide if we want the whole year or a date range
        answer = ""
        start_date, end_date = (None,) * 2
        while not (answer == "y" or answer == "d"):
            answer = raw_input("Do you want the entire year or a specific date range?(y/d) ").strip().lower()

        # Grab the dates specified
        if answer == "d":
            start_date, end_date = __date_range()

        # Gather contributions and print result
        contributions = user_list.get_contributions(username, start_date, end_date, True)
        if not contributions:
            print "No contributions exist for this user or the specified date range"
        else:
            print contributions

        # Find out if we want a new user or not
        answer = ""
        while not (answer == "u" or answer == "d" or answer == "exit"):
            answer = raw_input("Lookup new user, new date, or exit?(u/d/exit) ").strip().lower()
        if answer == "exit":
            break
        elif answer == "u":
            username = None


def __get_new_user(ul):
    # Let's find out which user we will start off with
    while True:
        answer = raw_input("Which user would you like to look up? ").strip()
        if ul.add_new_user(answer):
            return answer
        else:
            print("Invalid input or non-existent user.")


def __date_range():
    arr = [None] * 2
    for i in xrange(2):
        while True:
            try:
                date = gh_user.gh_api.parser.parse(raw_input(
                    "What is the " + ("start" if i == 0 else "end") + " date?(YYYY-MM-DD) ").replace("\\s+", ""))
                if 365 - (gh_user.gh_api.CURRENT_DATE - date).days < 0:
                    print "Date is out of range (has to be within 365 days of today's date)."
                    continue
                if arr[0] is not None and (date - gh_user.gh_api.parser.parse(arr[0])).days < 0:
                    print "End date is before start date!"
                    continue
                arr[i] = date.isoformat()
                break
            except ValueError or OverflowError:
                print "Not a valid value. Please try again."
                arr[i] = None

    return arr[0], arr[1]


if __name__ == "__main__":
    main()
