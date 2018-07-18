import unittest
from data import entries, Entry, ModelNotFoundException


class EntryMockModelTestCase(unittest.TestCase):
    def setUp(self):
        self.entries = entries()
        Entry.set_values(self.entries)

    def test_it_lists_all_entries(self):
        self.assertEqual(self.entries, Entry.all())

    def test_it_gets_a_specific_entry(self):
        # The second index of dummy entries has id == 3
        self.assertEqual(self.entries[2], Entry.get(3))
        self.assertNotEqual(self.entries[3], Entry.get(3))

    def test_it_returns_none_on_attempt_to_get_a_non_existent_model(self):
        self.assertIsNone(Entry.get(51115))

    def test_it_creates_new_entries(self):
        title = 'A title'
        body = 'A body'
        new_entry = Entry.create(title, body)
        self.assertEqual(new_entry, Entry.get(Entry.get_latest_id()))
        self.assertDictContainsSubset({'title': title, 'body': body}, new_entry)

    def test_it_increments_id(self):
        count_before = Entry.get_latest_id()
        Entry.create('Another title', 'Another body')
        self.assertEqual(count_before + 1, Entry.get_latest_id())

    def test_it_updates_entries(self):
        title = 'A new title'
        body = 'A new body'
        updated_entry = Entry.update(2, title, body)
        self.assertEqual(updated_entry, Entry.get(2))
        self.assertDictContainsSubset({'title': title, 'body': body}, updated_entry)

    def test_it_fails_on_attempt_to_update_non_existent_models(self):
        with self.assertRaises(ModelNotFoundException):
            Entry.update(71115, 'Foo', 'Bar')

    def test_it_deletes_entries(self):
        self.assertTrue(Entry.delete(3))

    def test_it_fails_on_attempt_to_delete_non_existent_models(self):
        with self.assertRaises(ModelNotFoundException):
            Entry.delete(91155)