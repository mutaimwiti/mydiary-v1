import json
from tests.auth_api_tests.base_test import BaseTestCase


class LoginTestCase(BaseTestCase):

    def setUp(self):
        BaseTestCase.setUp(self)
        self.credentials = {
            'name': 'Mutai Mwiti',
            'email': 'mutaimwiti@code.com',
            'password': 'password'
        }

    def test_it_creates_new_users(self):
        response = self.post('/api/v1/signup', data=self.credentials)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.mimetype, 'application/json')

    def test_it_allows_trailing_trash(self):
        response = self.post('/api/v1/signup/', data=self.credentials)
        self.assertEqual(response.status_code, 201)

    def test_it_fails_when_user_exists(self):
        self.db.create_user(overrides=self.credentials)
        response = self.post('/api/v1/signup', data=self.credentials)
        self.assertEqual(response.status_code, 409)

    def test_it_fails_when_password_is_less_than_6_characters(self):
        self.credentials.update({'password': 'pass'})
        response = self.post('/api/v1/signup', data=self.credentials)
        self.assertEqual(response.status_code, 422)
        self.assertEquals(
            {'password': ['The password field must have a minimum length of 6.']},
            json.loads(response.data).get('errors')
        )

    def test_it_fails_when_data_is_missing(self):
        response = self.post('/api/v1/signup', data={})
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.mimetype, 'application/json')
        errors = {
            'name': ['The name field is required.'],
            'email': ['The email field is required.'],
            'password': ['The password field is required.']
        }
        self.assertEqual(errors, json.loads(response.data).get('errors'))
