# good ol' python black magic
# by adding the local folder to the system path, we can import other python classes without a hassle
# and structure the setup for the database backend better
# not optimal for production
import sys
import os
scriptpath = "."

# Add the directory containing your module to the Python path (wants absolute paths)
sys.path.append(os.path.abspath(scriptpath))

from peewee import *
from playhouse.migrate import *
import datetime

from db_connection import db_connection

# db_connection is available from db_schema
# and looks like this
## db_connection = MySQLDatabase('ba', user='root', password='1234',
#                          host='127.0.0.1', port=3306)

# define the models
## id as PK is always included as a default (thanks to peewee)

class BaseModel(Model):

    class Meta:
        database = db_connection

class Doctor(BaseModel):
    url = CharField(null=True)
    name = CharField(null=True)
    function = CharField(null=True)
    gender = CharField(null=True)
    count_of_reviews = CharField(null=True)
    workplace = CharField(null=True)
    recommendation = CharField(null=True)

class Review(BaseModel):
    text = TextField(null=True)
    disease = CharField(null=True)
    relevance = CharField(null=True)
    url = CharField(null=True)
    date = DateTimeField(null=True)
    score_avg = CharField(null=True)
    level_1 = CharField(null=True)
    level_2 = CharField(null=True)
    level_3 = CharField(null=True)
    level_4 = CharField(null=True)
    level_5 = CharField(null=True)
    level_6  = CharField(null=True)
    timestamp = DateTimeField(default=datetime.datetime.now)
    reference = CharField(null=True)
    doctor = ForeignKeyField(Doctor, backref='reviews')

class Identifier(BaseModel):
    name = CharField()
    identifier = CharField()
    type = CharField()

list_of_models = [Review, Doctor, Identifier]

def create_tables(hard_reset = False):
    if(hard_reset):
        with db_connection:
            db_connection.drop_tables(list_of_models)
            db_connection.create_tables(list_of_models)
    else:
        with db_connection:
            db_connection.create_tables(list_of_models)

def drop_tables():
    with db_connection:
        db_connection.drop_tables(list_of_models)
