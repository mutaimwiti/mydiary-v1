import jwt
import bcrypt
import datetime
from utils import env
from app.database import DBQuery


class ModelNotFoundException(Exception):
    pass


class Entry:
    __db = DBQuery('entries')

    def __init__(self):
        pass

    @staticmethod
    def __check(entry_id):
        if Entry.__db.exists(entry_id) is False:
            raise ModelNotFoundException

    @staticmethod
    def count():
        return Entry.__db.count()

    @staticmethod
    def all():
        """
        Returns all the entries.
        :rtype: list
        """
        return Entry.__db.select('*')

    @staticmethod
    def get(entry_id):
        """
        Returns the specified entry.
        :param entry_id:
        :rtype: dict or None
        """
        Entry.__check(entry_id)
        return Entry.__db.get(entry_id)

    @staticmethod
    def create(title, body):
        """
        Creates an entry and returns a copy.
        :rtype: dict
        """
        return Entry.__db.insert({
            'title': title,
            'body': body,
        })

    @staticmethod
    def update(entry_id, title, body):
        """
        Updates the specified entry.
        :param entry_id:
        :param title:
        :param body:
        :rtype: dict
        """
        Entry.__check(entry_id)
        return Entry.__db.update({'title': title, 'body': body}, {'id': entry_id})

    @staticmethod
    def delete(entry_id):
        """
        Deletes the specified entry.
        :param entry_id:
        :rtype: bool
        """
        Entry.__check(entry_id)
        Entry.__db.delete({'id': entry_id})
        return True


class User:
    __db = DBQuery('users')

    def __init__(self):
        pass

    @staticmethod
    def __hash_password(password):
        return bcrypt.hashpw(password, bcrypt.gensalt())

    @staticmethod
    def __check_password(password, hashed):
        return bcrypt.checkpw(password, hashed)

    @staticmethod
    def get_by_email(email):
        selection = User.__db.select('*', {'email': email})
        return selection[0] if len(selection) > 0 else None

    @staticmethod
    def create(name, email, password):
        """
        Creates an entry and returns a copy.
        :rtype: dict
        """
        if User.get_by_email(email) is not None:
            return False
        return User.__db.insert({
            'name': name,
            'email': email,
            'password': User.__hash_password(password)
        })

    @staticmethod
    def check(email, password):
        user = User.get_by_email(email)
        if user is not None:
            return User.__check_password(password, user['password'])
        return False

    @staticmethod
    def generate_token(user):
        # token payload
        payload = {
            'user': user['email'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=int(env('SESSION_LIFETIME')))
        }
        return jwt.encode(payload, env('APP_KEY'))
