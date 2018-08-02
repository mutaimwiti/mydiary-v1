import json
from utils import NOT_FOUND_MSG
from tests.entry_api_tests.base_test import BaseTestCase


class DeleteTestCase(BaseTestCase):

    def test_it_deletes_entries(self):
        entry_id = self.db.create_entry(overrides={'created_by': self.user_id}).get('id')
        response = self.delete('/api/v1/entries/%s' % str(entry_id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'application/json')
        self.assertEqual({'message': 'Entry deleted.'}, json.loads(response.data))
        all_entries = json.loads(self.get('/api/v1/entries').data).get('entries')
        self.assertFalse(any(entry.get('id') == entry_id for entry in all_entries))

    def test_it_allows_trailing_trash(self):
        entry = self.db.create_entry(overrides={'created_by': self.user_id})
        response = self.delete('/api/v1/entries/%s/' % str(entry.get('id')))
        self.assertEqual(response.status_code, 200)

    def test_if_fails_when_the_current_user_is_not_the_owner(self):
        entry_id = self.db.create_entry().get('id')
        response = self.delete('/api/v1/entries/%s' % str(entry_id))
        self.assertEqual(response.status_code, 404)

    def test_fails_on_model_not_found(self):
        response = self.delete('/api/v1/entries/71115')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.mimetype, 'application/json')
        self.assertEqual({"message": "The entry was not found."}, json.loads(response.data))
