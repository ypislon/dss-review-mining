# this is an example file!
# to use the web crawler, you need to insert the right credentials
# you might want to adjust the charset, if the database has problems with the default encoding
# in this case, MySQL8 was used
# default encodings between MySQL5 and MySQL8 changed, so make sure to pick the right one here,
# otherwise the crawler will fail to save the fetched content into the database

from peewee import MySQLDatabase

db_connection = MySQLDatabase('ba', user='root', password='1234', host='127.0.0.1', port=3306, charset="utf8mb4", use_unicode=True)
