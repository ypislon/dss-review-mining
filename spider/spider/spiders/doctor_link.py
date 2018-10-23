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

# if you want to remove the logger functionality of peewee:
import logging
logger = logging.getLogger('peewee')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.WARNING)

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
        # urls = ("https://www.zorgkaartnederland.nl/amsterdam", "https://www.zorgkaartnederland.nl/huisarts/amsterdam", "https://www.zorgkaartnederland.nl/neuroloog/amsterdam", "https://www.zorgkaartnederland.nl/neurochirurg/amsterdam")
        urls = ("https://www.zorgkaartnederland.nl/huisarts/amsterdam", "https://www.zorgkaartnederland.nl/neuroloog/amsterdam", "https://www.zorgkaartnederland.nl/neurochirurg/amsterdam")

        for url in urls:
            # TODO: add multiple page support for different urls
            r = range(25)
            if(url == "https://www.zorgkaartnederland.nl/amsterdam"):
                r = range(500)
            for i in r:
                url_2 = url + "/pagina" + str(i)
                self.log(url_2)
                yield scrapy.Request(url=url_2, callback=self.parse)


    def parse(self, response):
        for identifier in Identifier.select().where(Identifier.type == "0").select():
            links = response.xpath(identifier.identifier) # TODO and so on...

            for link in links:
                doctor = Doctor.get_or_create(url=link.extract())
                self.log("Logging doctor with url")
                self.log(link.extract())
                self.log("#############")
