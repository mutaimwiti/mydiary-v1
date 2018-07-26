import json
from utils import NOT_FOUND_MSG
from tests.entry_api_tests.base_test import BaseTestCase


class UpdateTestCase(BaseTestCase):
    def test_it_updates_entries(self):
        self.db.create(10)
        updates = {'title': 'A new title', 'body': 'A new body'}
        response = self.put('/api/v1/entries/3', data=updates)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'application/json')
        self.assertDictContainsSubset(updates, json.loads(response.data)['entry'])

    def test_fails_on_model_not_found(self):
        response = self.delete('/api/v1/entries/81115')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.mimetype, 'application/json')
        self.assertEqual({"error": NOT_FOUND_MSG}, json.loads(response.data))

    def test_fails_when_data_does_not_meet_min_length(self):
        short_data = {'title': 'Cook', 'body': 'Short'}
        response = self.put('/api/v1/entries/4', data=short_data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.mimetype, 'application/json')
        errors = {
            'title': ['The title field must have a minimum length of 5.'],
            'body': ['The body field must have a minimum length of 10.'],
        }
        self.assertEqual(errors, json.loads(response.data)['errors'])

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
        self.assertEqual(errors, json.loads(response.data)['errors'])

    def test_fails_when_data_is_missing(self):
        response = self.put('/api/v1/entries/4', data={})
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.mimetype, 'application/json')
        errors = {
            'title': ['The title field is required.'],
            'body': ['The body field is required.'],
        }
        self.assertEqual(errors, json.loads(response.data)['errors'])
