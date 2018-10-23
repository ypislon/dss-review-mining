# -*- coding: utf-8 -*-
import scrapy
# good ol' python black magic
import sys
import os
scriptpath = "."

# Add the directory containing your module to the Python path (wants absolute paths)
sys.path.append(os.path.abspath(scriptpath))

from peewee import *
from db_schema import Identifier, Doctor, Review

class ReviewLinkSpider(scrapy.Spider):
    name = 'reviewlinkspider'
    allowed_domains = ['zorgkaartnederland.nl']
    start_urls = ['http://zorgkaartnederland.nl']

    # URLS FOR MINING
    #
    # for all results of a doctor:
    # https://www.zorgkaartnederland.nl/zorgverlener/_NAME_OF_DOCTOR_/waardering
    # e.g. https://www.zorgkaartnederland.nl/zorgverlener/neuroloog-meulen-b-c-ter-278252/waardering

    def start_requests(self):
        doctors = Doctor.select()

        for doctor in doctors:
            url = self.start_urls[0] + doctor.url + "waardering"
            yield scrapy.Request(url=url, callback=self.parse, meta={'doctor_id':doctor.id})

    def parse(self, response):

        doctor = Doctor.get_by_id(response.meta["doctor_id"])

        identifier = Identifier.get(Identifier.type == "3")

        for review_link in response.xpath(identifier.identifier):
            review = Review()
            review.doctor = doctor
            review.url = review_link.extract()
            review.save()
