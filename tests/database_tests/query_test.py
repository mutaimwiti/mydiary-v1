import unittest
from time import sleep
from app.database import DBQuery
from tests.helpers import DBUtils


class QueryTestCase(unittest.TestCase):

    def setUp(self):
        self.table = 'entries'
        self.query = DBQuery(self.table)
        self.db = DBUtils()
        self.db.create_schema()

    def test_it_inserts_records(self):
        data = {'title': 'My title', 'body': 'My body', 'created_by': self.db.create_user().get('id')}
        record = self.query.insert(data)
        self.assertDictContainsSubset(data, record)

    def test_it_updates_records(self):
        self.db.create_entry(3)
        data = {'title': 'Updated title', 'body': 'Updated body'}
        updated = self.query.update(data, {'id': self.db.random_entry().get('id')})
        self.assertDictContainsSubset(data, updated)

    def test_it_deletes_records(self):
        self.db.create_entry()
        record = self.db.random_entry()
        self.query.delete({'id': record.get('id')})
        self.assertEqual([], self.query.select('*', {'id': record.get('id')}))

    def test_it_gets_count_of_records(self):
        self.assertEqual(0, self.query.count())
        self.db.create_entry(3)
        self.assertEqual(3, self.query.count())

    def test_updated_at_column_is_updated(self):
        self.db.create_entry(3)
        record = self.query.select('*', {'id': self.db.random_entry().get('id')})[0]
        sleep(0.5)  # delay for 500ms before update
        self.query.update({'title': 'Tile', 'body': 'Body'}, {'id': record.get('id')})
        updated = self.query.select('*', {'id': record.get('id')})[0]
        self.assertGreater(updated.get('updated_at'), record.get('updated_at'))

    def tearDown(self):
        self.db.drop_schema()
