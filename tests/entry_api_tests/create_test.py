import json
from tests.entry_api_tests.base_test import BaseTestCase


class CreateTestCase(BaseTestCase):

    def test_it_creates_new_entries(self):
        new_entry = {'title': 'A title', 'body': 'A body to add'}
        response = self.post('/api/v1/entries', data=new_entry)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.mimetype, 'application/json')
        self.assertDictContainsSubset(new_entry, json.loads(response.data).get('entry'))

    def test_it_allows_trailing_trash(self):
        response = self.post('/api/v1/entries/', data={'title': 'A title', 'body': 'A body to add'})
        self.assertEqual(response.status_code, 201)

    def test_fails_when_data_exceeds_max_length(self):
        long_text = self.fake.text(1000)
        long_data = {'title': long_text, 'body': long_text + long_text}
        response = self.post('/api/v1/entries', data=long_data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.mimetype, 'application/json')
        errors = {
            'title': ['The title field must have a maximum length of 255.'],
            'body': ['The body field must have a maximum length of 1000.'],
        }
        self.assertEqual(errors, json.loads(response.data).get('errors'))

    def test_fails_when_data_is_missing(self):
        response = self.post('/api/v1/entries', data={})
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.mimetype, 'application/json')
        errors = {
            'title': ['The title field is required.'],
            'body': ['The body field is required.'],
        }
        self.assertEqual(errors, json.loads(response.data).get('errors'))

    def test_it_fails_when_a_similar_entry_exists_for_owner(self):
        data = {'title': 'A title', 'body': 'An entry body', 'created_by': self.user_id}
        self.db.create_entry(overrides=data)
        response = self.post('/api/v1/entries', data=data)
        self.assertEqual(409, response.status_code)
        self.assertEqual('A similar already entry exists.', json.loads(response.data).get('message'))
