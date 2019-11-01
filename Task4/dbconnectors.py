import pymysql


class DatabaseConnector:

    def __enter__(self):
        raise NotImplementedError

    def __exit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError

    @property
    def connection(self):
        raise NotImplementedError

    @property
    def cursor(self):
        raise NotImplementedError

    def commit(self):
        raise NotImplementedError

    def execute(self, sql, params=None):
        raise NotImplementedError

    def fetchall(self):
        raise NotImplementedError

    def fetchone(self):
        raise NotImplementedError

    def query(self, sql, params=None):
        raise NotImplementedError


class MySqlConnector(DatabaseConnector):
    def __init__(self, host, user, password, db):
        self._conn = pymysql.connect(
            host,
            user,
            password,
            db,
            cursorclass=pymysql.cursors.DictCursor
        )
        self._cursor = self._conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.commit()
        self.connection.close()

    @property
    def connection(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor

    def commit(self):
        self.connection.commit()

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.fetchall()
