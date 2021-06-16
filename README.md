# Open Humans Template

This is a template repository for a project that interacts with Open Humans and deploys in Heroku.

## Setup

For local development:

1. create an OAuth2 project in Open Humans this app connects to: https://www.openhumans.org/direct-sharing/oauth2-setup/
  * `REDIRECT_URL`: `http://127.0.0.1:5000/`
1. copy `env.example` to `.env`
  * edit using the values provided in the information page for this project you just created on Open Humans website and the Heroku app settings page
1. install Heroku's command line client:
https://devcenter.heroku.com/categories/command-line
1. `python --version` and update Pipfile to reflect your 3.x Python version
1. `pipenv --rm || true` to restart if something went wrong in the install process
1. `pipenv install`
1. `pipenv run python manage.py collectstatic`
1. `pipenv run python manage.py migrate`
1. run `heroku local` or `pipenv run python manage.py runserver`
