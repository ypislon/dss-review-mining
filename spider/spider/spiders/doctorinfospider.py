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
from db_schema import Identifier, Doctor
#from helper import *

# if you want to remove the logger functionality of peewee:
import logging
logger = logging.getLogger('peewee')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.WARNING)

# here we extract information about the doctors

class DoctorinfospiderSpider(scrapy.Spider):
    name = 'doctorinfospider'
    start_urls = ['https://www.zorgkaartnederland.nl']

    def start_requests(self):
        doctors = Doctor.select()

        for doctor in doctors:
            url = self.start_urls[0] + doctor.url
            yield scrapy.Request(url=url, callback=self.parse, meta={'doctor_id':doctor.id})

    def parse(self, response):

        doctor_id = response.meta['doctor_id']

        # try:
        doctor = Doctor.get_by_id(doctor_id)
        self.log("Mining data for doctor number:")
        self.log(doctor.id)

        for identifier in Identifier.select().where(Identifier.type == "1"):
            data = response.xpath(identifier.identifier)

            if(identifier.name == "doc_gender"):
                if(data.extract_first()):
                    doctor.gender = data.extract_first().strip()
            elif(identifier.name == 'doc_recommendation'):
                if(data.extract_first()):
                    doctor.recommendation = data.extract_first().strip()
            elif(identifier.name == 'doc_workplace'):
                if(data.extract_first()):
                    doctor.workplace = data.extract_first().strip()
            elif(identifier.name == 'doc_function'):
                if(data.extract_first()):
                    doctor.function = data.extract_first().strip()
            elif(identifier.name == 'doc_name'):
                if(data.extract_first()):
                    doctor.name = data.extract_first().strip()
            # elif(identifier.name == 'doc_count_of_reviews'):
            #     doctor.count_of_reviews = data.extract_first()

            self.log("Scraping info for doctor with id")
            self.log(doctor.id)
            self.log("#############")

            doctor.save()

                # identifier.name
                #
                # self.log(links)
                # for link in links:
                #     doctor = Doctor.get_or_create(url=link.extract())
                #     # self.log(doctor.url)
                #     # doctor.url = link.extract()
                #     # doctor.save()

        # except:
        #     self.log("Something went wrong while receiving the doctor.")
