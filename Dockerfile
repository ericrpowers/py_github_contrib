FROM python:2-onbuild

# NOTE: You must set the following environment variables (using docker -e flag): GH_USER, GH_USER_OATOKEN
# eg. docker run -e GH_USER=$GH_USER -e GH_USER_OATOKEN=$GH_USER_OATOKEN -it --rm --name py_github_contrib_app py_github_contrib_img
CMD [ "python", "./github_contrib.py" ]