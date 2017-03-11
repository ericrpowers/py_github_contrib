import datetime
import json
import os
import grequests
import requests
import dateutil.parser as parser

# To avoid saving sensitive info into the code
__auth = (os.environ.get('GH_USER', ''), os.environ.get('GH_USER_OATOKEN', ''))
current_date = datetime.datetime.now()


def is_user(username):
    r = requests.get('https://api.github.com/users/' + username, auth=__auth)
    return r.ok


def get_repos(username):
    r = requests.get('https://api.github.com/users/' + username + '/repos?type=all', auth=__auth)
    if not r.ok:
        return None
    repo_list = json.loads(r.text or r.content)
    return [repo['full_name'] for repo in repo_list]


def get_contributions(username):
    """ Contributions are based on the following:
        1) Commits made by the user on a master repository
        2) Pull requests opened by the user on a master repository
        3) Issues opened by an user """
    init_url = 'https://api.github.com/repos/'
    repos = get_repos(username)
    if len(repos) == 0:
        return []
    # Commits and Issues
    # Per documentation: every pull request is an issue, but not every issue is a pull request.
    response_list_dict = []
    for cmd in ['/commits?author=', '/issues?creator=']:
        url_list = [init_url + repo + cmd + username for repo in repos]
        request_list = [grequests.get(url, auth=__auth) for url in url_list]
        response_list_dict.append(grequests.imap(request_list))

    # Add up everything with respect to the date
    contrib_list = [0] * 365
    for resp_dict in response_list_dict:
        for r in resp_dict:
            jr_list = json.loads(r.text or r.content)
            for jr in jr_list:
                if not ('commit' in jr or 'created_at' in jr):
                    continue
                try:
                    date = parser.parse(jr['commit']['author']['date']).replace(tzinfo=None)
                except TypeError:
                    date = parser.parse(jr['created_at']).replace(tzinfo=None)
                index = 364 - (current_date - date).days
                if index >= 0:
                    if contrib_list[index] == 0:
                        contrib_list[index] = 1
                    else:
                        contrib_list[index] += 1
    return contrib_list
