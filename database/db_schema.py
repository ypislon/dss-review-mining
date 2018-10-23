# good ol' python black magic
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
    doctor = ForeignKeyField(Doctor, backref='reviews') # TODO look up how this works

class Identifier(BaseModel):
    name = CharField()
    identifier = CharField()
    type = CharField()
    # review_disease = CharField()
    # review_relevance = CharField()
    ### -> can't assign single levels, since they differ for every review
    # level_1_appointments = CharField()
    # level_2_treatment = CharField()
    # level_3_friendliness = CharField()
    # level_4_information = CharField()
    # level_5_listening = CharField()
    # level_6_accomodation = CharField()
    # review_score = CharField()
    # review_text = CharField()
    # doc_name = CharField()
    # doc_count_of_reviews = CharField()
    # doc_recommendation = CharField()
    # doc_gender = CharField()
    # doc_function = CharField()
    # doc_workplace = CharField()
    # initial_review_link = CharField()

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
