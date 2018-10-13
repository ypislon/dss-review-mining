from peewee import *
from db_schema import Identifier

from db_connection import db_connection

identifiers = {
    ("review_disease", ""),
    ("review_relevance", ""),
    ("level_1", "**/#main-body-content/**/ul[class='striped_box sliders_list']/li[1]/text()"),
    ("level_2", "**/#main-body-content/**/ul[class='striped_box sliders_list']/li[2]/text()"),
    ("level_3", "**/#main-body-content/**/ul[class='striped_box sliders_list']/li[3]/text()"),
    ("level_4", "**/#main-body-content/**/ul[class='striped_box sliders_list']/li[4]/text()"),
    ("level_5", "**/#main-body-content/**/ul[class='striped_box sliders_list']/li[5]/text()"),
    ("level_6", "**/#main-body-content/**/ul[class='striped_box sliders_list']/li[6]/text()"),
    ("review_score", "**/inner_row/div[1]/text()"),
    ("review_text", "**/div[class='explanation']/p[1]/text()"),
    ("doc_name", "**/h1/text()"),
    ("doc_count_of_reviews", "/**/buttons_holder/p[1]/text()"),
    ("doc_recommendation", "/**/buttons_holder/p[1]/b/text()"),
    ("doc_gender", "/**/div[1]/span/text()"),
    ("doc_function", "/**/div[1]/span/text()"),
    ("doc_workplace", "/**/div[2]/a/text()"),
    ("initial_doctor_link", "/**/results/**/a[href]"),
    ("initial_review_link", "")
}

def seed_db():
    for identifiers in identifier:
        name = identifier[0]
        id = identifier[1]

    try:
        identifier_db = Identifier()
        identifier_db.name = name
        identifier_db.identifier = id
        identifier_db.save()
    except Exception:
        print("An error occured during seeding the websites.\n" + Exception)
        pass
