from peewee import MySQLDatabase

db_connection = MySQLDatabase('ba', user='root', password='1234',
                         host='127.0.0.1', port=3306, charset="utf8mb4", use_unicode=True)
