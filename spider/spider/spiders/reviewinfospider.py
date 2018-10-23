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

class ReviewinfospiderSpider(scrapy.Spider):
    name = 'reviewinfospider'
    start_urls = ['http://zorgkaartnederland.nl/']

    def start_requests(self):
        reviews = Review.select()

        for review in reviews:
            url = review.url
            yield scrapy.Request(url=url, callback=self.parse, meta={'review_id':review.id})

    def parse(self, response):
        pass
