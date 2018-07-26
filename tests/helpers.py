from psycopg2 import extras, sql
from faker import Faker
from app.database import DBConnection
from app.models import User
from utils import full_path


class DBUtils:
    """
    This class allows for easy testing of the database. We must trust it.
    """
    def __init__(self, table):
        self.table = table
        self.fake = Faker()
        self.connection = DBConnection.get()
        self.connection.autocommit = True
        self.cursor = self.connection.cursor(cursor_factory=extras.RealDictCursor)

    def drop_schema(self):
        self.cursor.execute(open(full_path('schema/drop.sql'), 'r').read())

    def create_schema(self):
        self.cursor.execute(open(full_path('schema/create.sql'), 'r').read())

    def random(self):
        self.cursor.execute("select id from entries order by random()")
        return self.cursor.fetchone()

    def create(self, count=1, select='*'):
        records = []
        for i in range(0, count):
            self.cursor.execute(
                sql.SQL("insert into {} (title, body) values(%s, %s) returning id").format(
                    sql.Identifier(self.table)
                ), (self.fake.sentence(), self.fake.text())
            )
            _id = [self.cursor.fetchone()['id']]
            if select == '*':
                self.cursor.execute(sql.SQL("select * from {} where id = {}").format(
                    sql.Identifier(self.table), sql.Placeholder()
                ), _id)
            else:
                self.cursor.execute(sql.SQL("select {} from {} where id = {}").format(
                    sql.SQL(', ').join(map(sql.Identifier, select)),
                    sql.Identifier(self.table),
                    sql.Placeholder()
                ), _id)
            records.append(self.cursor.fetchone())
        return records


def auth_token():
    user = User.create('Mutai Mwiti', 'mutaimwiti@code.com', 'secret')
    return User.generate_token(user)
