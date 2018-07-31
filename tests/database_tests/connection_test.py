import unittest
from app.database import DBConnection


class ConnectionTestCase(unittest.TestCase):

    def test_an_open_connection_is_created(self):
        connection = DBConnection.get()
        self.assertEqual(0, connection.closed)
