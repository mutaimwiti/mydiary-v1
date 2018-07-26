# MyDiary API v1

[![Build Status](https://travis-ci.org/mutaimwiti/mydiary-v1.svg?branch=api)](
https://travis-ci.org/mutaimwiti/mydiary-v1)
[![Coverage Status](https://coveralls.io/repos/github/mutaimwiti/mydiary-v1/badge.svg?branch=api)](
https://coveralls.io/github/mutaimwiti/mydiary-v1?branch=api)

This is v1 of a RESTful API to power MyDiary front-end pages.

The API is implemented using Flask Python Framework.

#### Requirements
1. `python3` - [Python](https://www.python.org/)
2. `pip` - [Install pip](https://pip.pypa.io/en/stable/installing/)

#### Setup
Create a virtual environment

`$ python3 -m venv venv`

Activate the virtual environment

`$ . venv/bin/activate`

Install project dependencies

`$ pip install -r requirements.txt`

#### Running tests
To run the tests ensure:
1. You are on the project directory.
2. The virtual environment is activated.
3. Dependencies are installed.

Run the tests

`$ pytest`

#### Running app
Ensure the requirements for running tests are met.

Run app

`$ flask run`

