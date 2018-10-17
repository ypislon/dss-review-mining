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

# here we extract information about the doctors

class DoctorinfospiderSpider(scrapy.Spider):
    name = 'doctorinfospider'
    allowed_domains = ['example.com']
    start_urls = ['https://www.zorgkaartnederland.nl']

    def start_requests(self):
        doctors = Doctor.select()

        for doctor in doctors:
            url = self.start_urls[0] + doctor.url
            self.log("SCRAPING DOCTOR VIA URL:")
            self.log(url)

            yield scrapy.Request(url=url, callback=self.parse, meta={'doctor_id':doctor.id})


    def parse(self, response):

        doctor_id = response.meta['doctor_id']

        # try:
        doctor = Doctor.get(doctor_id)

        for identifier in Identifier.select().where(Identifier.type == "1").select():
            self.log(identifier.name)
            #self.log(identifier)
            data = response.xpath(identifier.identifier)

            if(identifier.name == "doc_gender"):
                doctor.gender = data.extract_first()
            elif(identifier.name == 'doc_recommendation'):
                doctor.recommendation = data.extract_first()
            elif(identifier.name == 'doc_workplace'):
                doctor.workplace = data.extract_first()
            elif(identifier.name == 'doc_function'):
                doctor.function = data.extract_first()
            elif(identifier.name == 'doc_name'):
                doctor.name = data.extract_first()
            # elif(identifier.name == 'doc_count_of_reviews'):
            #     doctor.count_of_reviews = data.extract_first()

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