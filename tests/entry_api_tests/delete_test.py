import json
from utils import NOT_FOUND_MSG
from tests.entry_api_tests.base_test import BaseTestCase


class DeleteTestCase(BaseTestCase):

    def test_it_deletes_entries(self):
        self.db.create(3)
        response = self.delete('/api/v1/entries/2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'application/json')
        self.assertEqual({'message': 'Entry deleted.'}, json.loads(response.data))
        # Ensure that entry with id == 2 no longer exists on the models
        all_entries = json.loads(self.get('/api/v1/entries').data)['entries']
        self.assertFalse(any(entry['id'] == 2 for entry in all_entries))

    def test_fails_on_model_not_found(self):
        response = self.delete('/api/v1/entries/71115')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.mimetype, 'application/json')
        self.assertEqual({"error": NOT_FOUND_MSG}, json.loads(response.data))
