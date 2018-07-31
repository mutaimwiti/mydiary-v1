import json
from tests.entry_api_tests.base_test import BaseTestCase


class StatsTestCase(BaseTestCase):

    def test_it_gets_entry_count_stat(self):
        self.db.create_entry(count=3, overrides={'created_by': self.user_id})
        response = self.get('/api/v1/entries/stats/count')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'application/json')
        self.assertEqual(3, json.loads(response.data).get('count'))

    def test_it_allows_trailing_trash(self):
        self.db.create_entry(count=3, overrides={'created_by': self.user_id})
        response = self.get('/api/v1/entries/stats/count/')
        self.assertEqual(response.status_code, 200)

    def test_it_gets_entry_count_only_for_owner(self):
        self.db.create_entry(3)
        response = self.get('/api/v1/entries/stats/count')
        self.assertEqual(0, json.loads(response.data).get('count'))

    def test_entry_count_remains_accurate_after_creation(self):
        data = {'title': 'A title', 'body': 'This is a body'}
        old_count = json.loads(self.get('/api/v1/entries/stats/count').data).get('count')
        self.post('/api/v1/entries', data=data)
        new_count = json.loads(self.get('/api/v1/entries/stats/count').data).get('count')
        self.assertEqual(new_count, old_count + 1)

    def test_entry_count_remains_accurate_after_deletion(self):
        self.db.create_entry(count=4, overrides={'created_by': self.user_id})
        old_count = json.loads(self.get('/api/v1/entries/stats/count').data).get('count')
        self.delete('/api/v1/entries/2')
        new_count = json.loads(self.get('/api/v1/entries/stats/count').data).get('count')
        self.assertEqual(new_count, old_count - 1)
