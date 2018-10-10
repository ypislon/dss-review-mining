
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

class Review(BaseModel):
    text = CharField(null=true)
    date = DateTimeField()
    score_avg = IntegerField(null=true)
    level_1_appointments = IntegerField(null=true)
    level_2_treatment = IntegerField(null=true)
    level_3_friendliness = IntegerField(null=true)
    level_4_information = IntegerField(null=true)
    level_5_listening = IntegerField(null=true)
    level_6_accomodation  = IntegerField(null=true)
    timestamp = DateTimeField(default=datetime.datetime.now)
    reference = IntegerField(null=true)

class Doctor(BaseModel):
    name = CharField()
    function = CharField()
    gender = CharField()
    count_of_reviews = IntegerField()
    workplace = IntegerField()

class Identifier(BaseModel):
    review_disease = CharField()
    review_relevance = CharField()
    level_1_appointments = CharField()
    level_2_treatment = CharField()
    level_3_friendliness = CharField()
    level_4_information = CharField()
    level_5_listening = CharField()
    level_6_accomodation = CharField()
    review_score = CharField()
    review_text = CharField()
    doc_name = CharField()
    doc_count_of_reviews = CharField()
    doc_recommendation = CharField()
    doc_gender = CharField()
    doc_function = CharField()
    doc_workplace = CharField()

list_of_models = [Review, Doctor]

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
