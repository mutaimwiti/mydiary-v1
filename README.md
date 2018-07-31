# MyDiary API v1

[![Build Status](https://travis-ci.org/mutaimwiti/mydiary-v1.svg?branch=development)](
https://travis-ci.org/mutaimwiti/mydiary-v1)
[![Coverage Status](https://coveralls.io/repos/github/mutaimwiti/mydiary-v1/badge.svg?branch=development)](
https://coveralls.io/github/mutaimwiti/mydiary-v1?branch=development)

This is v1 of a RESTful API to power MyDiary front-end pages.

The API is implemented using Flask Python Framework. 

It uses JWT authentication and Postgres database.  The API is minimal in its use of programming abstractions with Flask 
being the only notable one. It implements it's own custom validator and database abstraction layer.

#### Requirements
1. `python3` - [Python](https://www.python.org/)
2. `pip` - [Install pip](https://pip.pypa.io/en/stable/installing/)
3. `postgres` - [Postgres](https://www.postgresql.org/)

#### Setup
##### The .env file
Create the .env file.

`$ cp .env.example .env`

###### general config
`SESSION_LIFETIME` - An integer that determines how long the authentication token should remain valid (minutes).

`APP_KEY=$SECRET_KEY$` - A random key that is used by the application to generate secure authentication tokens.
###### production db config
`DB_HOST` - The production/staging database host.

`DB_USER` - The production/staging database user.

`DB_NAME` - The production/staging database name.

`DB_PASSWORD` - The production/staging database password.
###### testing db config
`TEST_DB_HOST` - The testing database host.

`TEST_DB_USER` - The testing database user.

`TEST_DB_NAME` - The testing database name.

`TEST_DB_PASSWORD` - The testing database password.

Set the variables on this files to suit your preferences and environment.

Create a virtual environment

`$ python3 -m venv venv`

Activate the virtual environment

`$ . venv/bin/activate`

Install project dependencies

`$ pip install -r requirements.txt`

#### Running tests
Create a testing database 

`$ psql -c 'create database <your_testing_database_name>;' -U <postgres_username>`

Example:

`$ psql -c 'create database mydiary_testing;' -U postgres`

Run the tests

`$ pytest`

#### Running app
Create a production/staging database 

`$ psql -c 'create database <your_database_name>;' -U <postgres_username>`

Example:

`$ psql -c 'create database mydiary;' -U postgres`

Import the database schema into your database. Navigate to the project directory and import it.

`$ psql -d <your_database_name> -a -f schema/create.sql -U <postgres_username>`

Run app

`$ flask run`

Note that to run the app or tests the virtual environment must to be active.
