from psycopg2.extras import RealDictCursor
from psycopg2.pool import ThreadedConnectionPool
from app.core.config import data_source as ds


class PooledDatabase:
    _pool = None

    @classmethod
    def initialize(cls, minconn=ds.DB_MIN_CONNECTION, maxconn=ds.DB_MAX_CONNECTION):
        if cls._pool is None:
            cls._pool = ThreadedConnectionPool(
                minconn,
                maxconn,
                dbname=ds.DB_NAME,
                host=ds.DB_HOST,
                user=ds.DB_USER,
                password=ds.DB_PASSWORD
            )

    @classmethod
    def get_conn(cls):
        if cls._pool is None:
            raise Exception("Connection pool is not initialized.")
        return cls._pool.getconn()

    @classmethod
    def return_conn(cls, conn):
        if cls._pool and conn:
            cls._pool.putconn(conn)

    @classmethod
    def close_all(cls):
        if cls._pool:
            cls._pool.closeall()


class DatabaseSession:
    def __enter__(self):
        self.conn = PooledDatabase.get_conn()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        PooledDatabase.return_conn(self.conn)

    def fetch_one(self, query, params=None):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, params)
            return cursor.fetchone()

    def fetch_all(self, query, params=None):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()

    def execute(self, query, params=None):
        with self.conn.cursor() as cursor:
            cursor.execute(query, params)
            self.conn.commit()
