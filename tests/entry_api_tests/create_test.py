import json
from tests.entry_api_tests.base_test import BaseTestCase


class CreateTestCase(BaseTestCase):

    def test_it_creates_new_entries(self):
        new_entry = {'title': 'A title', 'body': 'A body to add'}
        response = self.post('/api/v1/entries', data=new_entry)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.mimetype, 'application/json')
        self.assertDictContainsSubset(new_entry, json.loads(response.data)['entry'])

    def test_fails_when_data_does_not_meet_min_length(self):
        short_data = {'title': 'Cook', 'body': 'Short'}
        response = self.post('/api/v1/entries', data=short_data)
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
        response = self.post('/api/v1/entries', data=long_data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.mimetype, 'application/json')
        errors = {
            'title': ['The title field must have a maximum length of 255.'],
            'body': ['The body field must have a maximum length of 1000.'],
        }
        self.assertEqual(errors, json.loads(response.data)['errors'])

    def test_fails_when_data_is_missing(self):
        response = self.post('/api/v1/entries', data={})
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.mimetype, 'application/json')
        errors = {
            'title': ['The title field is required.'],
            'body': ['The body field is required.'],
        }
        self.assertEqual(errors, json.loads(response.data)['errors'])
