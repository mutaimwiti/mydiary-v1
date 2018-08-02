import json
from tests.auth_api_tests.base_test import BaseTestCase


class SignupTestCase(BaseTestCase):

    def setUp(self):
        BaseTestCase.setUp(self)
        self.credentials = {
            'name': 'Mutai Mwiti',
            'email': 'mutaimwiti@code.com',
            'password': '$2a$12$XGJGf0MDMNn.nH9g6hsAguE0kmFS2PMWh33F7bEcNSxxEgMEs.X2y'
        }
        self.db.create_user(overrides=self.credentials)
        self.credentials.update({'password': 'password'})

    def test_it_generates_token_for_user(self):
        # login user
        response = self.post('/api/v1/login', data=self.credentials)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'application/json')
        # confirm token is not none
        self.assertIsNotNone(json.loads(response.data).get('token'))

    def test_it_allows_trailing_trash(self):
        # login user
        response = self.post('/api/v1/login/', data=self.credentials)
        self.assertEqual(response.status_code, 200)

    def test_it_fails_when_user_does_not_exist(self):
        self.credentials.update({'email': 'fake@mail.com'})
        response = self.post('/api/v1/login', data=self.credentials)
        self.assertEqual(response.status_code, 401)
        self.assertEqual('Invalid login.', json.loads(response.data).get('message'))

    def test_it_fails_when_data_is_missing(self):
        response = self.post('/api/v1/login', data={})
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.mimetype, 'application/json')
        errors = {
            'email': ['The email field is required.'],
            'password': ['The password field is required.']
        }
        self.assertEqual(errors, json.loads(response.data).get('errors'))
