import jwt
import bcrypt
import datetime
from utils import env
from app.database import DBQuery


class ModelNotFoundException(Exception):
    def __init__(self, model):
        if model == 'entry':
            super(ModelNotFoundException, self).__init__('The entry was not found.')
            

class Entry:
    __db = DBQuery('entries')

    def __init__(self):
        pass

    @staticmethod
    def __check(filters):
        if Entry.exists(filters) is False:
            raise ModelNotFoundException('entry')
        
    @staticmethod    
    def exists(filters):
        return Entry.__db.exists(filters)

    @staticmethod
    def count(filters=None):
        return Entry.__db.count(filters)

    @staticmethod
    def all(filters=None):
        """
        Returns all the entries.
        :rtype: list
        """
        return Entry.__db.select('*', filters)

    @staticmethod
    def get(filters):
        """
        Returns the specified entry.
        :param filters:
        :rtype: dict or None
        """
        Entry.__check(filters)
        return Entry.__db.get(filters)

    @staticmethod
    def create(title, body, created_by):
        """
        Creates an entry and returns a copy.
        :rtype: dict
        """
        if Entry.__db.exists({'title': title, 'body': body, 'created_by': created_by}):
            return None
        return Entry.__db.insert({
            'title': title,
            'body': body,
            'created_by': created_by
        })

    @staticmethod
    def update(filters, title, body):
        """
        Updates the specified entry.
        :param filters:
        :param title:
        :param body:
        :rtype: dict
        """
        Entry.__check(filters)
        return Entry.__db.update({'title': title, 'body': body}, filters)

    @staticmethod
    def delete(filters):
        """
        Deletes the specified entry.
        :param filters:
        :rtype: bool
        """
        Entry.__check(filters)
        Entry.__db.delete(filters)
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
            'id': user.get('id'),
            'email': user.get('email'),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=int(env('SESSION_LIFETIME')))
        }
        return jwt.encode(payload, env('APP_KEY'))
