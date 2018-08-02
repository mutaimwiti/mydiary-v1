import json
from utils import NOT_FOUND_MSG
from tests.entry_api_tests.base_test import BaseTestCase


class UpdateTestCase(BaseTestCase):

    def test_it_updates_entries(self):
        self.db.create_entry(count=3, overrides={'created_by': self.user_id})
        updates = {'title': 'A new title', 'body': 'A new body'}
        response = self.put('/api/v1/entries/2', data=updates)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'application/json')
        self.assertDictContainsSubset(updates, json.loads(response.data).get('entry'))

    def test_it_allows_trailing_trash(self):
        self.db.create_entry(count=3, overrides={'created_by': self.user_id})
        response = self.put('/api/v1/entries/2/', data={'title': 'A new title', 'body': 'A new body'})
        self.assertEqual(response.status_code, 200)

    def test_it_only_updates_entries_for_owner(self):
        self.db.create_entry(count=3)
        updates = {'title': 'A new title', 'body': 'A new body'}
        response = self.put('/api/v1/entries/2', data=updates)
        self.assertEqual(response.status_code, 404)

    def test_fails_on_model_not_found(self):
        response = self.delete('/api/v1/entries/81115')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.mimetype, 'application/json')
        self.assertEqual({"message": "The entry was not found."}, json.loads(response.data))

    def test_fails_when_data_does_not_meet_min_length(self):
        short_data = {'title': 'Cook', 'body': 'Short'}
        response = self.put('/api/v1/entries/4', data=short_data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.mimetype, 'application/json')
        errors = {
            'title': ['The title field must have a minimum length of 5.'],
            'body': ['The body field must have a minimum length of 10.'],
        }
        self.assertEqual(errors, json.loads(response.data).get('errors'))

    def test_fails_when_data_exceeds_max_length(self):
        long_text = self.fake.text(1000)
        long_data = {'title': long_text, 'body': long_text + long_text}
        response = self.put('/api/v1/entries/4', data=long_data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.mimetype, 'application/json')
        errors = {
            'title': ['The title field must have a maximum length of 255.'],
            'body': ['The body field must have a maximum length of 1000.'],
        }
        self.assertEqual(errors, json.loads(response.data).get('errors'))

    def test_fails_when_data_is_missing(self):
        response = self.put('/api/v1/entries/4', data={})
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.mimetype, 'application/json')
        errors = {
            'title': ['The title field is required.'],
            'body': ['The body field is required.'],
        }
        self.assertEqual(errors, json.loads(response.data).get('errors'))

    def test_fails_when_a_similar_entry_exists_for_owner(self):
        data = {'title': 'A title', 'body': 'An entry body', 'created_by': self.user_id}
        entry = self.db.create_entry(overrides=data)
        response = self.put('/api/v1/entries/%s' % entry.get('id'), data=data)
        self.assertEqual(409, response.status_code)
        self.assertEqual('A similar already entry exists.', json.loads(response.data).get('message'))
