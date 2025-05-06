# api/core/mysql_singleton.py
from flask_mysqldb import MySQL

class MySQLManager:
    _mysql_instance = None

    @classmethod
    def init_app(cls, app):
        if cls._mysql_instance is None:
            cls._mysql_instance = MySQL(app)
        return cls._mysql_instance

    @classmethod
    def get_mysql(cls):
        if cls._mysql_instance is None:
            raise Exception("MySQL not initialized. Call init_app(app) first.")
        return cls._mysql_instance
