import json
from tests.entry_api_tests.base_test import BaseTestCase


class ListTestCase(BaseTestCase):

    def test_it_lists_all_entries(self):
        records = self.db.create_entry(count=3, overrides={'created_by': self.user_id})
        response = self.get('/api/v1/entries')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'application/json')
        expected = [
            {'title': item.get('title'), 'body': item.get('body')} for item in records
        ]
        received = [
            {'title': item.get('title'), 'body': item.get('body')} for item in json.loads(response.data).get('entries')
        ]
        self.assertEqual(expected, received)

    def test_it_allows_trailing_trash(self):
        self.db.create_entry(count=3, overrides={'created_by': self.user_id})
        response = self.get('/api/v1/entries/')
        self.assertEqual(response.status_code, 200)

    def test_it_only_returns_entries_for_the_owner(self):
        self.db.create_entry(3)
        response = self.get('/api/v1/entries')
        self.assertEqual(0, json.loads(response.data).get('count'))
