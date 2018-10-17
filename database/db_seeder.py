# good ol' python black magic
import sys
import os
scriptpath = "."

# Add the directory containing your module to the Python path (wants absolute paths)
sys.path.append(os.path.abspath(scriptpath))

from peewee import *
from db_schema import Identifier

from db_connection import db_connection

identifiers = {
    ("review_disease", "//*/", "2"),
    ("review_relevance", "//*/", "2"),
    ("level_1", "//**/#main-body-content/**/ul[class='striped_box sliders_list']/li[1]/text()", "2"),
    ("level_2", "//**/#main-body-content/**/ul[class='striped_box sliders_list']/li[2]/text()", "2"),
    ("level_3", "//**/#main-body-content/**/ul[class='striped_box sliders_list']/li[3]/text()", "2"),
    ("level_4", "//**/#main-body-content/**/ul[class='striped_box sliders_list']/li[4]/text()", "2"),
    ("level_5", "//**/#main-body-content/**/ul[class='striped_box sliders_list']/li[5]/text()", "2"),
    ("level_6", "//**/#main-body-content/**/ul[class='striped_box sliders_list']/li[6]/text()", "2"),
    ("review_score", "//**/inner_row/div[1]/text()", "2"),
    ("review_text", "//**/div[class='explanation']/p[1]/text()", "2"),
    ("doc_name", "//*/h1/text()", "1"),
    ("doc_count_of_reviews", "///*[contains(@class, 'buttons_holder')]/p[1]/text()", "1"),
    ("doc_recommendation", "//*[contains(@class, 'buttons_holder')]/p[1]/b/text()", "1"),
    ("doc_gender", "//*/address/div[1]/span/text()", "1"),
    ("doc_function", "//*/h1/following-sibling::p/text()", "1"),
    ("doc_workplace", "//*/address/div/a[contains(@class, 'address_content')]/text()", "1"),
    ("initial_doctor_link", "//*[contains(@class, 'results')]//a/@href", "0"),
    ("initial_review_link", "", "3")
}

def seed_db():
    for identifier in identifiers:
        name = identifier[0]
        id = identifier[1]
        type = identifier[2]

        try:
            identifier_db = Identifier()
            identifier_db.name = name
            identifier_db.identifier = id
            identifier_db.type = type
            identifier_db.save()
        except Exception:
            print("An error occured during seeding the websites.\n" + Exception)
            pass
