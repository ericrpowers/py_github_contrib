FROM python:2-onbuild

# NOTE: You must set the following environment variables (using docker -e flag): GH_USER, GH_USER_OATOKEN 
CMD [ "python", "./github_contrib.py" ]