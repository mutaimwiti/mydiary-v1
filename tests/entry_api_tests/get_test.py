import json
from tests.entry_api_tests.base_test import BaseTestCase


class GetTestCase(BaseTestCase):

    def test_it_gets_a_specific_entry(self):
        records = self.db.create(4, select=['title', 'body'])
        response = self.get('/api/v1/entries/4')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'application/json')
        # The third index of records has id == 4
        self.assertDictContainsSubset(records[3], json.loads(response.data)['entry'])
