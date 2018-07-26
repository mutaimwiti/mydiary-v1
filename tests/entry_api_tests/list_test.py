import json
from tests.entry_api_tests.base_test import BaseTestCase


class ListTestCase(BaseTestCase):

    def test_it_lists_all_entries(self):
        records = self.db.create(10, select=['title', 'body'])
        response = self.get('/api/v1/entries')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'application/json')
        filtered = [{'title': item['title'], 'body': item['body']} for item in json.loads(response.data)['entries']]
        self.assertEqual(records, filtered)
