import unittest
from time import sleep
from app.database import DBQuery
from tests.helpers import DBUtils


class QueryTestCase(unittest.TestCase):
    # before each test
    def setUp(self):
        self.table = 'entries'
        self.query = DBQuery(self.table)
        self.db = DBUtils('entries')
        self.db.drop_schema()
        self.db.create_schema()

    def test_it_inserts_records(self):
        data = {'title': 'My title', 'body': 'My body'}
        record = self.query.insert(data)
        self.assertDictContainsSubset(data, record)

    def test_it_updates_records(self):
        self.db.create(10)
        data = {'title': 'Updated title', 'body': 'Updated body'}
        updated = self.query.update(data, {'id': self.db.random()['id']})
        self.assertDictContainsSubset(data, updated)

    def test_it_deletes_records(self):
        self.db.create(10)
        record = self.db.random()
        self.query.delete({'id': record['id']})
        self.assertEqual([], self.query.select('*', {'id': record['id']}))

    def test_it_gets_count_of_records(self):
        self.assertEqual(0, self.query.count())
        self.db.create(5)
        self.assertEqual(5, self.query.count())

    def test_updated_at_column_is_updated(self):
        self.db.create(10)
        record = self.query.select('*', {'id': self.db.random()['id']})[0]
        sleep(0.5)  # delay for 500ms before update
        self.query.update({'title': 'Tile', 'body': 'Body'}, {'id': record['id']})
        updated = self.query.select('*', {'id': record['id']})[0]
        self.assertGreater(updated['updated_at'], record['updated_at'])
