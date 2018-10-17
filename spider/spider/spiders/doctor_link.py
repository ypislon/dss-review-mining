# black magic - mac solution
#import sys
#sys.path.insert(0, 'C:\\hdm\\xampp\\htdocs\\dss-mining-review\\database')

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

#
# URLS FOR MINING
#
# for all doctors in amsterdam:
# https://www.zorgkaartnederland.nl/amsterdam
# 428 pages -> pattern: https://www.zorgkaartnederland.nl/amsterdam/pagina2
#
# for all gp's in ams:
# https://www.zorgkaartnederland.nl/huisarts/amsterdam
# 25 pages
#
# for all neurologists in ams:
# https://www.zorgkaartnederland.nl/neuroloog/amsterdam
# 5 pages
#
# for all neurochirugs in ams:
# https://www.zorgkaartnederland.nl/neurochirurg/amsterdam
# 2 pages
#
#
#


class DoctorLinkSpider(scrapy.Spider):
    name = "doctorlinkspider"

    def start_requests(self):
        urls = ("https://www.zorgkaartnederland.nl/amsterdam", "https://www.zorgkaartnederland.nl/huisarts/amsterdam", "https://www.zorgkaartnederland.nl/neuroloog/amsterdam", "https://www.zorgkaartnederland.nl/neurochirurg/amsterdam")

        for url in urls:
            # TODO: add multiple page support for different urls
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        for identifier in Identifier.select().where(Identifier.type == "0").select():
            self.log(identifier.name)
            #self.log(identifier)
            links = response.xpath(identifier.identifier) # TODO and so on...
            self.log(links)
            for link in links:
                doctor = Doctor.get_or_create(url=link.extract())
                # self.log(doctor.url)
                # doctor.url = link.extract()
                # doctor.save()
