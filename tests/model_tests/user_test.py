import unittest
from tests.helpers import DBUtils
from app.models import User


class EntryModelTestCase(unittest.TestCase):
    def setUp(self):
        self.db = DBUtils('users')
        self.db.drop_schema()
        self.db.create_schema()

    def test_it_creates_user(self):
        name = 'Mutai Mwiti'
        email = 'mutaimwiti@code.com'
        # new user
        user = User.create(name, email, 'secret')
        self.assertDictContainsSubset({'name': name, 'email': email}, user)
        # duplicate user
        self.assertFalse(User.create(name, email, 'secret'))

    def test_it_checks_user_credentials(self):
        email = 'mutaimwiti@code.com'
        password = 'secret'
        # create user
        User.create('Mutai Mwiti', email, password)
        # test with valid credentials
        self.assertTrue(User.check(email, password))
        # test with invalid credentials
        self.assertFalse(User.check(email, 'wrong password'))
