from flask import Flask
from app.handlers import ExceptionHandler, HttpHandler
from app.models import ModelNotFoundException
from app.controllers import EntryController, UserController
from app.request import ValidationException

# Create flask app
app = Flask(__name__)


# Define API endpoints
# Entry resource routes
@app.route('/api/v1/entries/', strict_slashes=False)
@UserController.check_auth
def all_entries():
    return EntryController.all()


@app.route('/api/v1/entries/<int:entry_id>/', strict_slashes=False)
@UserController.check_auth
def get(entry_id):
    return EntryController.get(entry_id)


@app.route('/api/v1/entries/', methods=['POST'], strict_slashes=False)
@UserController.check_auth
def create():
    return EntryController.create()


@app.route('/api/v1/entries/<int:entry_id>/', methods=['PUT'], strict_slashes=False)
@UserController.check_auth
def update(entry_id):
    return EntryController.update(entry_id)


@app.route('/api/v1/entries/<int:entry_id>/', methods=['DELETE'], strict_slashes=False)
@UserController.check_auth
def delete(entry_id):
    return EntryController.delete(entry_id)


# Entry stats routes
@app.route('/api/v1/entries/stats/count/', methods=['GET'], strict_slashes=False)
@UserController.check_auth
def entry_stat_count():
    return EntryController.count()


# User routes
@app.route('/api/v1/signup/', methods=['POST'], strict_slashes=False)
def signup():
    return UserController.signup()


@app.route('/api/v1/login/', strict_slashes=False)
def login():
    return UserController.login()


# Define API error handlers
@app.errorhandler(ModelNotFoundException)
def model_not_found(exception):
    return ExceptionHandler.handle(exception)


@app.errorhandler(ValidationException)
def validation_errors(exception):
    return ExceptionHandler.handle(exception)


@app.errorhandler(404)
def not_found(error):
    return HttpHandler.handle(404)
