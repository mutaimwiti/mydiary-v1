import unittest
from tests.helpers import DBUtils
from app.models import Entry, ModelNotFoundException


class EntryModelTestCase(unittest.TestCase):
    def setUp(self):
        self.db = DBUtils()
        self.db.create_schema()

    def test_it_lists_all_entries(self):
        records = self.db.create_entry(10)
        self.assertEqual(records, Entry.all())

    def test_it_gets_a_specific_entry(self):
        self.db.create_entry(4)
        entry = self.db.random_entry()
        self.assertEqual(entry, Entry.get({'id': entry.get('id')}))
        # Fails for non-existent entries
        with self.assertRaises(ModelNotFoundException):
            Entry.get({'id': 51115})

    def test_it_creates_new_entries(self):
        title = 'A title'
        body = 'A body'
        new_entry = Entry.create(title, body, self.db.create_user().get('id'))
        self.assertDictContainsSubset({'title': title, 'body': body}, new_entry)

    def test_it_updates_entries(self):
        self.db.create_entry(10)
        title = 'A new title'
        body = 'A new body'
        updated_entry = Entry.update({'id': 2}, title, body)
        self.assertEqual(updated_entry, Entry.get({'id': 2}))
        self.assertDictContainsSubset({'title': title, 'body': body}, updated_entry)
        # Fails for non-existent entries
        with self.assertRaises(ModelNotFoundException):
            Entry.update({'id': 71115}, 'Foo', 'Bar')

    def test_it_deletes_entries(self):
        self.db.create_entry(4)
        self.assertTrue(Entry.delete({'id': 3}))
        # Fails for non-existent entries
        with self.assertRaises(ModelNotFoundException):
            Entry.delete({'id': 91155})

    def test_it_gets_entry_count(self):
        self.db.create_entry(6)
        self.assertEqual(6, Entry.count())

    def test_entry_count_is_always_accurate(self):
        self.db.create_entry(5)
        # when new entry is created
        count_before = Entry.count()
        Entry.create('A title', 'A body', self.db.create_user().get('id'))
        count_after = Entry.count()
        self.assertEqual(count_after, count_before + 1)
        # when an entry is deleted
        count_before = Entry.count()
        Entry.delete({'id': 2})
        count_after = Entry.count()
        self.assertEqual(count_after, count_before - 1)

    def tearDown(self):
        self.db.drop_schema()
