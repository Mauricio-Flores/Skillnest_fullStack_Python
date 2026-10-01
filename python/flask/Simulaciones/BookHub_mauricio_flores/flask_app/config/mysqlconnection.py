import pymysql
from flask import current_app


class MySQLConnection:
    """Una conexión por consulta. Los parámetros se envían separados del SQL."""

    def __init__(self, db):
        self.connection = pymysql.connect(
            host=current_app.config['DB_HOST'],
            port=current_app.config['DB_PORT'],
            user=current_app.config['DB_USER'],
            password=current_app.config['DB_PASSWORD'],
            database=db,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=False,
            connect_timeout=5,
        )

    def query_db(self, query, data=None):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, data)
                if cursor.description is not None:
                    return cursor.fetchall()
                self.connection.commit()
                if query.lstrip().upper().startswith('INSERT'):
                    return cursor.lastrowid
                return cursor.rowcount
        except pymysql.MySQLError:
            self.connection.rollback()
            raise
        finally:
            self.connection.close()


def connectToMySQL(db=None):
    return MySQLConnection(db or current_app.config['DB_NAME'])
