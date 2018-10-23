# -*- coding: utf-8 -*-
import scrapy

# python black magic - win solution
import sys
import os
scriptpath = "./../database"
# Add the directory containing your module to the Python path (wants absolute paths)
sys.path.append(os.path.abspath(scriptpath))


import scrapy
from urllib.parse import urljoin
from db_schema import Identifier, Doctor, Review
#from helper import *

# if you want to remove the logger functionality of peewee:
import logging
logger = logging.getLogger('peewee')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.WARNING)

class ReviewinfospiderSpider(scrapy.Spider):
    name = 'reviewinfospider'
    start_urls = ['http://zorgkaartnederland.nl']

    def start_requests(self):
        reviews = Review.select()

        for review in reviews:
            url = self.start_urls[0] + review.url
            yield scrapy.Request(url=url, callback=self.parse, meta={'review_id':review.id})

    def parse(self, response):
        review_id = response.meta['review_id']
        review = Review.get_by_id(review_id)

        for identifier in Identifier.select().where(Identifier.type == "2"):
            data = response.xpath(identifier.identifier)

            if(identifier.name == "review_disease"):
                if(data.extract_first()):
                    review.disease = data.extract_first().strip()
            elif(identifier.name == 'review_relevance'):
                if(data.extract_first()):
                    review.relevance = data.extract_first().strip()
            elif(identifier.name == 'review_score'):
                if(data.extract_first()):
                    review.score_avg = data.extract_first().strip()
            elif(identifier.name == 'review_text'):
                if(data.extract_first()):
                    review.text = data.extract_first().strip()
            elif(identifier.name == 'level_1'):
                if(data.extract_first()):
                    review.level_1 = data.extract_first().strip()
            elif(identifier.name == 'level_2'):
                if(data.extract_first()):
                    review.level_2 = data.extract_first().strip()
            elif(identifier.name == 'level_3'):
                if(data.extract_first()):
                    review.level_3 = data.extract_first().strip()
            elif(identifier.name == 'level_4'):
                if(data.extract_first()):
                    review.level_4 = data.extract_first().strip()
            elif(identifier.name == 'level_5'):
                if(data.extract_first()):
                    review.level_5 = data.extract_first().strip()
            elif(identifier.name == 'level_6'):
                if(data.extract_first()):
                    review.level_6 = data.extract_first().strip()

            review.save()

        self.log("Scraping info for review with id")
        self.log(review_id)
        self.log("#############")
