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

# if you want to remove the logger functionality of peewee:
import logging
logger = logging.getLogger('peewee')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.WARNING)


class ReviewLinkSpider(scrapy.Spider):
    name = 'reviewlinkspider'
    allowed_domains = ['zorgkaartnederland.nl']
    start_urls = ['http://zorgkaartnederland.nl']
    deadend = False

    # URLS FOR MINING
    #
    # for all results of a doctor:
    # https://www.zorgkaartnederland.nl/zorgverlener/_NAME_OF_DOCTOR_/waardering
    # e.g. https://www.zorgkaartnederland.nl/zorgverlener/neuroloog-meulen-b-c-ter-278252/waardering

    def start_requests(self):
        doctors = Doctor.select().where(Doctor.id > 12800)

        for doctor in doctors:

            url = self.start_urls[0] + doctor.url + "waardering"
            r = range(100)
            self.log("##### Scraping doctor with id %s #####" % (doctor.id))

            for i in r:
                if(self.deadend):
                    self.deadend = False
                    break

                if(i == 0):
                    yield scrapy.Request(url=url, callback=self.parse, meta={'doctor_id':doctor.id})
                else:
                    url_2 = url + "/pagina" + str(i)
                    yield scrapy.Request(url=url_2, callback=self.parse, meta={'doctor_id':doctor.id})

    def parse(self, response):

        if(response.status == "404"):
            self.deadend = True
            pass

        doctor = Doctor.get_by_id(response.meta["doctor_id"])

        identifier = Identifier.get(Identifier.type == "3")

        for review_link in response.xpath(identifier.identifier):
            review = Review()
            review.doctor = doctor
            review.url = review_link.extract()

            self.log("Creating review with link")
            self.log(review_link.extract())
            self.log("#############")

            review.save()
