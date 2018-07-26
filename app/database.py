from psycopg2 import connect, sql, extras
from utils import env


class DBConnection:
    def __init__(self):
        pass

    __connection = None

    @staticmethod
    def __get_connection():
        if DBConnection.__connection is None:
            host = env('DB_HOST')
            user = env('DB_USER')
            name = env('DB_NAME')
            password = env('DB_PASSWORD')
            DBConnection.__connection = connect(
                host=host,
                user=user,
                password=password,
                dbname=name
            )
        return DBConnection.__connection

    @staticmethod
    def get():
        return DBConnection.__get_connection()


class DBQuery:
    def __init__(self, table):
        self.table = table
        self.connection = DBConnection.get()
        self.connection.autocommit = True
        self.cursor = self.connection.cursor(cursor_factory=extras.RealDictCursor)

    @staticmethod
    def attribute_equals_value(attributes):
        """
        An sql generator for a = b, j = k, m = n ...
        :param attributes:
        """
        aggregate = []
        for item in attributes:
            aggregate.append(
                sql.SQL("{} = {}").format(
                    sql.Identifier(item), sql.Placeholder()
                )
            )
        return sql.SQL(', ').join(aggregate)

    def exists(self, _id):
        return False if self.get(_id) is None else True

    def get(self, _id):
        entry = self.select('*', {'id': _id})
        return entry[0] if len(entry) > 0 else None

    def insert(self, data):
        """
        data is a dictionary containing field:value.
        Example {'title': 'My title', 'body': 'My body'}
        :type data: dict
        :param data:
        """
        fields = data.keys()
        values = list(data.values())
        query = sql.SQL("insert into {} ({}) values ({}) returning id").format(
            sql.Identifier(self.table),
            sql.SQL(', ').join(map(sql.Identifier, fields)),
            sql.SQL(', ').join(sql.Placeholder() * len(fields))
        )
        self.cursor.execute(query, values)
        _id = self.cursor.fetchone()['id']
        return self.get(_id)

    def update(self, data, filters):
        """
        data is a dictionary containing field:value. So is
        filters. data is what will be updated and filters
        is specifies the filtering criteria.
        Examples:
        data = {'title': 'My title', 'body': 'My body'}
        filters = {'id': 7}
        :param filters: dict
        :param data: dict
        """
        query = sql.SQL("update {} set {} where {} returning id").format(
            sql.Identifier(self.table),
            DBQuery.attribute_equals_value(data),
            DBQuery.attribute_equals_value(filters)
        )
        values = list(data.values()) + list(filters.values())
        self.cursor.execute(query, values)
        _id = self.cursor.fetchone()['id']
        return self.get(_id)

    def delete(self, filters):
        """
        filters is a dictionary containing field:value. It specifies
        the filtering criteria. Example: {'id': 4}
        :param filters: dict
        """
        # delete from table where condition
        query = sql.SQL("delete from {} where {}").format(
            sql.Identifier(self.table),
            DBQuery.attribute_equals_value(filters)
        )
        self.cursor.execute(query, list(filters.values()))

    def select(self, fields, filters=None):
        """
        fields is a list specifying the fields to query e.g. ['id', 'name'].
        It can also be a sting in the special case of querying all i.e. '*'.
        filters is a dictionary specifying the filtering that will be
        applied in the query e.g {'name' = 'Sir'}.
        :param fields: list or str
        :param filters: dict
        :return: list
        """
        if fields is '*':
            if filters is None:
                query = sql.SQL("select * from {}").format(
                    sql.Identifier(self.table)
                )
                self.cursor.execute(query)
            else:
                query = sql.SQL("select * from {} where {}").format(
                    sql.Identifier(self.table),
                    DBQuery.attribute_equals_value(filters)
                )
                self.cursor.execute(query, list(filters.values()))
        else:
            if filters is None:
                query = sql.SQL("select {} from {}").format(
                    sql.SQL(', ').join(map(sql.Identifier, fields)),
                    sql.Identifier(self.table),
                )
                self.cursor.execute(query)
            else:
                query = sql.SQL("select {} from {} where {}").format(
                    sql.SQL(', ').join(map(sql.Identifier, fields)),
                    sql.Identifier(self.table),
                    DBQuery.attribute_equals_value(filters)
                )
                self.cursor.execute(query, list(filters.values()))
        return self.cursor.fetchall()

    def count(self):
        """
        Gets the row count for the table.
        :return: int
        """
        query = sql.SQL("select count(*) from {}").format(sql.Identifier(self.table))
        self.cursor.execute(query)
        return self.cursor.fetchone()['count']

    def raw(self, query, fetch=False):
        self.cursor.execute(query)
        self.connection.commit()
        if fetch is True:
            return self.cursor.fetchall()
