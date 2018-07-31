import json
from tests.entry_api_tests.base_test import BaseTestCase


class GetTestCase(BaseTestCase):

    def test_it_gets_a_specific_entry(self):
        record = self.db.create_entry(overrides={'created_by': self.user_id})
        response = self.get('/api/v1/entries/%s' % str(record.get('id')))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'application/json')
        expected_data = {'title': record.get('title'), 'body': record.get('body')}
        self.assertDictContainsSubset(expected_data, json.loads(response.data).get('entry'))

    def test_it_allows_trailing_trash(self):
        record = self.db.create_entry(overrides={'created_by': self.user_id})
        response = self.get('/api/v1/entries/%s/' % str(record.get('id')))
        self.assertEqual(response.status_code, 200)

    def test_if_fails_when_the_current_user_is_not_the_owner(self):
        entry_id = self.db.create_entry().get('id')
        response = self.delete('/api/v1/entries/%s' % str(entry_id))
        self.assertEqual(response.status_code, 404)
