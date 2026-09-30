"""Small PyMySQL gateway used by the models."""

import os

import pymysql
import pymysql.cursors


class DatabaseGateway:
    """Execute one parameterized query per short-lived MySQL connection."""

    def __init__(self, database_name):
        self.connection = pymysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=database_name,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True,
        )

    def execute(self, query, parameters=None):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, parameters or {})
                if query.lstrip().lower().startswith("select"):
                    return cursor.fetchall()
                return cursor.lastrowid
        finally:
            self.connection.close()


def connect_to_mysql(database_name):
    """Create the gateway requested by a model."""
    return DatabaseGateway(database_name)
