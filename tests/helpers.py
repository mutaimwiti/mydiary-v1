from psycopg2 import extras, sql
from faker import Faker
from app.database import DBConnection
from app.models import User
from utils import full_path


class DBUtils:
    """
    This class allows for easy testing of the database. We must trust it.
    """
    def __init__(self):
        self.fake = Faker()
        self.connection = DBConnection.get()
        self.connection.autocommit = True
        self.cursor = self.connection.cursor(cursor_factory=extras.RealDictCursor)

    def drop_schema(self):
        self.cursor.execute(open(full_path('schema/drop.sql'), 'r').read())

    def create_schema(self):
        self.cursor.execute(open(full_path('schema/create.sql'), 'r').read())

    def random_user(self, count=1):
        return self.random('users', count)

    def random_entry(self, count=1):
        return self.random('entries', count)

    def random(self, table, count=1):
        query = sql.SQL("select * from {} order by random() limit {}").format(
            sql.Identifier(table), sql.Placeholder()
        )
        self.cursor.execute(query, (count,))
        items = self.cursor.fetchall()
        return items[0] if count == 1 else items

    def make_user(self, count=1, overrides=None):
        """
        Creates a dictionary containing values that can be used to create a user.
        :param count:
        :param overrides:
        :return:
        """
        overrides = overrides if overrides else {}
        override_fields = overrides.keys()
        users = []
        for i in range(0, count):
            users.append(
                {
                    'name': overrides.get('name') if 'name' in override_fields else self.fake.name(),
                    'email': overrides.get('email') if 'email' in override_fields else self.fake.email(),
                    'password': overrides.get('password') if 'password' in override_fields else self.fake.password()
                }
            )
        return users[0] if count == 1 else users

    def make_entry(self, count=1, overrides=None):
        """
        Creates a dictionary containing values that can be used to create an entry.
        The created_by field holds an the id of a user on the database.
        :param count:
        :param overrides:
        :return:
        """
        overrides = overrides if overrides else {}
        override_fields = overrides.keys()
        entries = []
        for i in range(0, count):
            entries.append({
                'title': overrides.get('title') if 'title' in override_fields else self.fake.name(),
                'body': overrides.get('body') if 'body' in override_fields else self.fake.email(),
                'created_by':
                    overrides.get('created_by') if 'created_by' in override_fields else self.create_user().get('id')
            })
        return entries[0] if count == 1 else entries

    def create_user(self, count=1, overrides=None):
        """
        Whips up an email and persists it to the database.
        :param count: int
        :param overrides: None or dict
        :return: list or dict
        """
        return self.create('users', 'user', ['name', 'email', 'password'], count, overrides)

    def create_entry(self, count=1, overrides=None):
        """
        Whips up an entry and persists it to the database.
        :param count: int
        :param overrides: None or dict
        :return: list or dict
        """
        return self.create('entries', 'entry', ['title', 'body', 'created_by'], count, overrides)

    def create(self, table, model, fields, count=1, overrides=None):
        """
        Whips up an item and persists it to the database.
        Insert sample query: "insert into x (a, b, c) values (x, y, z) returning id"
        Retrieve entry sample query: "select * from entries where id in (2, 3, 4)"
        :param table: str
        :param model: str
        :param fields: list
        :param count: int
        :param overrides: None or dict
        :return: list or dict
        """
        overrides = overrides if overrides else {}
        item_ids = []
        for i in range(0, count):
            # build insert query string
            query = sql.SQL("insert into {} ({}) values ({}) returning id").format(
                sql.Identifier(table),
                sql.SQL(', ').join(map(sql.Identifier, fields)),
                sql.SQL(', ').join(sql.Placeholder() * len(fields))
            )
            # make random values
            make_method = getattr(self, 'make_' + model)
            random_values = list(make_method(overrides=overrides).values())
            # insert item
            self.cursor.execute(query, random_values)
            # get id of inserted item
            item_ids.append(self.cursor.fetchone().get('id'))
        # build query to retrieve just inserted item
        query = sql.SQL("select * from {} where id in ({})").format(
            sql.Identifier(table),
            sql.SQL(', ').join(sql.Placeholder() * len(item_ids))
        )
        # retrieve just inserted items
        self.cursor.execute(query, item_ids)
        return self.cursor.fetchone() if count == 1 else self.cursor.fetchall()
