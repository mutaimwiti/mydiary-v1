from psycopg2 import connect, sql, extras
from sys import modules
from utils import env


class DBConnection:
    def __init__(self):
        pass

    __connection = None

    @staticmethod
    def __get_connection():
        if DBConnection.__connection is None:
            # determine whether we are testing or in
            # production or staging.
            if 'pytest' not in modules.keys():
                host = env('DB_HOST')
                user = env('DB_USER')
                name = env('DB_NAME')
                password = env('DB_PASSWORD')
            else:
                host = env('TEST_DB_HOST')
                user = env('TEST_DB_USER')
                name = env('TEST_DB_NAME')
                password = env('TEST_DB_PASSWORD')
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
    def __x_equals_y_comma_clause(attributes):
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

    @staticmethod
    def __x_equals_y_and_clause(attributes):
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
        return sql.SQL(' and ').join(aggregate)

    def exists(self, filters):
        """
        filters is a dictionary specifying the filtering criteria
        to be applied e.g {'id': 25, created_by' = 10}.
        :param filters:
        :return:
        """
        return False if self.get(filters) is None else True

    def get(self, filters):
        """
        filters is a dictionary specifying the filtering criteria
        to be applied e.g {'id': 25, created_by' = 10}.
        :param filters:
        :return:
        """
        entry = self.select('*', filters)
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
        item_id = self.cursor.fetchone().get('id')
        return self.get({'id': item_id})

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
            DBQuery.__x_equals_y_comma_clause(data),
            DBQuery.__x_equals_y_and_clause(filters)
        )
        values = list(data.values()) + list(filters.values())
        self.cursor.execute(query, values)
        item_id = self.cursor.fetchone().get('id')
        return self.get({'id': item_id})

    def delete(self, filters):
        """
        filters is a dictionary containing field:value. It specifies
        the filtering criteria. Example: {'id': 4}
        :param filters: dict
        """
        # delete from table where condition
        query = sql.SQL("delete from {} where {}").format(
            sql.Identifier(self.table),
            DBQuery.__x_equals_y_and_clause(filters)
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
                    DBQuery.__x_equals_y_and_clause(filters)
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
                    DBQuery.__x_equals_y_and_clause(filters)
                )
                self.cursor.execute(query, list(filters.values()))
        return self.cursor.fetchall()

    def count(self, filters=None):
        """
        Gets the row count for the table.
        :return: int
        """
        if filters is None:
            query = sql.SQL("select count(*) from {}").format(sql.Identifier(self.table))
            self.cursor.execute(query)
        else:
            query = sql.SQL("select count(*) from {} where {}").format(
                sql.Identifier(self.table),
                DBQuery.__x_equals_y_and_clause(filters)
            )
            self.cursor.execute(query, list(filters.values()))
        return self.cursor.fetchone().get('count')

    def raw(self, query, fetch=False):
        self.cursor.execute(query)
        self.connection.commit()
        if fetch is True:
            return self.cursor.fetchall()
