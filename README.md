# py_github_contrib

GitHub User Contribution Retriever fetches the contributions of a user of GitHub in the last year (365 days) or within a specified date range.

Additionally, there is Docker support, unit tests using unittest, REST server using Flask and E2E mock using PyTest.

## Criteria

To be considered a contribution, it must fall in the below requirements:

1. Commits made by the user on a master repository
2. Pull requests opened by the user on a master repository
3. Issues opened by a user

> Note: It is limited to publicly available information within GitHub.

## Prerequisites

> Suggest using built-in means like `brew`, `apt-get` or `pip` to avoid human error.

* Python 2.7.x - https://www.python.org/downloads/release/python-2713/
* Base required libraries
    * python-dateutil
    * requests
    * grequests
* (optional) REST server libraries
    * flask
    * flask-restful
    * flask-httpauth
* (optional) E2E library
    * pytest
* (optional) Docker - https://docs.docker.com/engine/getstarted/

## Running py_github_contrib

> To avoid being eventually blocked by GitHub due to exceeding requests, use a GitHub account
and OAuth token set to the following environment variables respectively: GH_USER , GH_USER_OATOKEN

From the repo directory, to run the CLI app:

    python ./github_contrib.py

To run the REST server:

    python ./gh_web.py

### REST APIs

Base route is `/ghuc/api/v1.0/users` (BASE) with the following support:

* GET
* POST

BASE + `/<username>` has the following support:

* GET
* PUT
* DELETE

BASE + `/<username>/<start>:<end>` has the following support:

* GET
