from peewee import MySQLDatabase

# Peewee supports MySQL, sqllite and postgresql databases
# For this project, a MySQL database is used

db_connection = MySQLDatabase('DssReviewMining', user='root', password='password', host='127.0.0.1', port=3306)
