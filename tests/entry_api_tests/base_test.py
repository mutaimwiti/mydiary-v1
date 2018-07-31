import unittest
from faker import Faker
from app import app
from tests.helpers import DBUtils
from app.models import User


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        self.fake = Faker()
        self.db = DBUtils()
        self.db.create_schema()
        user = self.db.create_user()
        self.user_id = user.get('id')
        self.client = app.test_client(self)
        self.token = User.generate_token(user)

    def get(self, url):
        return self.client.get(url, headers={'x-access-token': self.token})

    def post(self, url, data):
        return self.client.post(url, data=data, headers={'x-access-token': self.token})

    def put(self, url, data):
        return self.client.put(url, data=data, headers={'x-access-token': self.token})

    def delete(self, url):
        return self.client.delete(url, headers={'x-access-token': self.token})

    def tearDown(self):
        self.db.drop_schema()
