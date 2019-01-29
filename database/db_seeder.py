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
from db_schema import Identifier

from db_connection import db_connection

identifiers = {
    ("initial_doctor_link", "//*[contains(@class, 'results')]//a/@href", "0"),
    ("doc_name", "//*/h1/text()", "1"),
    ("doc_count_of_reviews", "///*[contains(@class, 'buttons_holder')]/p[1]/text()", "1"),
    ("doc_recommendation", "//*[contains(@class, 'buttons_holder')]/p[1]/b/text()", "1"),
    ("doc_gender", "//*/address/div[1]/span/text()", "1"),
    ("doc_function", "//*/h1/following-sibling::p/text()", "1"),
    ("doc_workplace", "//*/address/div/a[contains(@class, 'address_content')]/text()", "1"),
    ("review_disease", "//*[@class='sliders_holder form_holder holder_small']//ul[@class='striped_box form_holder rating_holder_small']//div[@class='media-body']/text()", "2"),
    ("review_relevance", "//*[@class='rating_like_holder']//span[@class='number_of_persons']/text()", "2"),
    ("level_1", "//section[@class='content_section'][1]//ul[@class='striped_box sliders_list']/li[1]//*/text()", "2"),
    ("level_2", "//section[@class='content_section'][1]//ul[@class='striped_box sliders_list']/li[2]//*/text()", "2"),
    ("level_3", "//section[@class='content_section'][1]//ul[@class='striped_box sliders_list']/li[3]//*/text()", "2"),
    ("level_4", "//section[@class='content_section'][1]//ul[@class='striped_box sliders_list']/li[4]//*/text()", "2"),
    ("level_5", "//section[@class='content_section'][1]//ul[@class='striped_box sliders_list']/li[5]//*/text()", "2"),
    ("level_6", "//section[@class='content_section'][1]//ul[@class='striped_box sliders_list']/li[6]//*/text()", "2"),
    ("review_score", "//*[@class='fractional_number text-right pull-right']//text()", "2"),
    ("review_text", "//*[@class='sliders_holder form_holder holder_small']/div[@class='with_left_margin with_right_margin']/div[2]/text()", "2"),
    ("initial_review_link", "//*[@class='striped_box results_holder']/li//h4/a/@href", "3")
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
