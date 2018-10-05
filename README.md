# Open Humans Template

This is a template repository for a project that interacts with Open Humans and deploys in Heroku.

## Setup

For local development:

1. create an OAuth2 project in Open Humans this app connects to: https://www.openhumans.org/direct-sharing/oauth2-setup/
  * `REDIRECT_URL`: `http://127.0.0.1:5000/`
2. copy `env.example` to `.env`
  * edit `CLIENT_ID` and `CLIENT_SECRET` using the values provided in the information page for this project you just created on Open Humans website
3. install Heroku's command line client:
https://devcenter.heroku.com/categories/command-line
4. run `heroku local`
