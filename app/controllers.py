import jwt
from functools import wraps
from flask import jsonify, request
from app.models import Entry, User
from app.request import validate, auth
from utils import env


class EntryController:
    def __init__(self):
        pass

    @staticmethod
    def count():
        entry = Entry.count({'created_by': auth.id()})
        return jsonify({'count': entry}), 200

    @staticmethod
    def all():
        entries = Entry.all({'created_by': auth.id()})
        return jsonify({'entries': entries, 'count': len(entries)}), 200

    @staticmethod
    def get(entry_id):
        entry = Entry.get({'id': entry_id, 'created_by': auth.id()})
        return jsonify({'entry': entry}), 200

    @staticmethod
    def create():
        validate(request.form, {'title': 'required|min:5|max:255', 'body': 'required|min:10|max:1000'})
        entry = Entry.create(request.form.get('title'), request.form.get('body'), auth.id())
        return jsonify({'entry': entry}), 201

    @staticmethod
    def update(entry_id):
        validate(request.form, {'title': 'required|min:5|max:255', 'body': 'required|min:10|max:1000'})
        entry = Entry.update(
            {'id': entry_id, 'created_by': auth.id()},
            request.form.get('title'),
            request.form.get('body')
        )
        return jsonify({'entry': entry}), 200

    @staticmethod
    def delete(entry_id):
        Entry.delete({'id': entry_id, 'created_by': auth.id()})
        return jsonify({'message': 'Entry deleted.'}), 200


class UserController:
    def __init__(self):
        pass

    @staticmethod
    def signup():
        # create a new user
        validate(request.form, {'name': 'required', 'email': 'required|email', 'password': 'required|min:6'})
        created = User.create(request.form.get('name'), request.form.get('email'), request.form.get('password'))
        if created is False:
            return jsonify({'message': 'A user with the same email address exists.'}), 409
        return jsonify({'message': 'User created.'}), 201

    @staticmethod
    def login():
        _auth = request.authorization
        # check that username(email in this case) and password are provided.
        if not _auth or not _auth.username or not _auth.password:
            message = {'error': 'Login required.'}
        else:
            # check that the user actually exists
            user = User.get_by_email(_auth.username)

            if user:
                # check the user credentials
                if User.check(_auth.username, _auth.password):
                    # generate jwt token
                    token = User.generate_token(user)
                    # return token
                    return jsonify({'token': token.decode('UTF-8')}), 200
            # the user gave invalid credentials
            message = {'error': 'Invalid login.'}
        return jsonify(message), 401

    @staticmethod
    def check_auth(f):
        """
        This is a decorator method to wrap routes
        that require authentication.
        :param f:
        :return:
        """
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None

            if 'x-access-token' in request.headers:
                token = request.headers.get('x-access-token')

            if not token:
                return jsonify({'error': 'Authentication is required.'}), 401

            try:
                data = jwt.decode(token, env('APP_KEY'))
                auth.set(data.get('user'))
            except:
                return jsonify({'error': 'Invalid access token.'}), 401

            return f(*args, **kwargs)

        return decorated
