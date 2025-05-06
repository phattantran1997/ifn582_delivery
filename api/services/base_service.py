from utils.mysql_init import MySQLManager

class BaseService:
    def __init__(self):
        self.mysql = MySQLManager.get_mysql()

    def get_cursor(self):
        return self.mysql.connection.cursor() 