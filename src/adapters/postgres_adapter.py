import psycopg2

from src.utils.config import secrets


class PostgreSQL:
    def __init__(self):
        self.database=secrets.get('POSTGRES_DB_NAME')
        self.user=secrets.get('POSTGRES_USERNAME')
        self.host=secrets.get('POSTGRES_HOST')
        self.password=secrets.get('POSTGRES_PASSWORD')
        self.port=secrets.get('POSTGRES_PORT')

        self.conn = None

        self._create_connection()


    def _create_connection(self):
        conn = psycopg2.connect(
            database=self.database,
            user=self.user,
            host=self.host,
            password=self.password,
            port=self.port
        )
        self.conn = conn
    

    def close_connection(self):
        self.conn.close()


    def commit_changes(self):
        self.conn.commit()


    def fetch_data(self, query):
        cur = self.conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()

        self.commit_changes()

        self.close_connection()
        return rows
    

