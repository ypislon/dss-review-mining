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
    urls = ("https://www.zorgkaartnederland.nl/amsterdam", "https://www.zorgkaartnederland.nl/huisarts/amsterdam", "https://www.zorgkaartnederland.nl/neuroloog/amsterdam", "https://www.zorgkaartnederland.nl/neurochirurg/amsterdam")

    def start_requests(self):
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

        ##### TAKEN FROM BA ######
        for website in Website.select():
            website, urls_per_website = parse_articles_url(website)

            for url in urls_per_website:
                # construct full url from base url and parsed fragment
                url = urljoin(website.url, url)
                yield scrapy.Request(url=url, callback=self.parse, meta={"website_name" : website.name})

    def parse(self, response):
        for identifier in Identifier.where("type" == "1").select():
            response.xpath(identifier.string) # TODO and so on...
            # create new doctor and assign url to him
            # get the link from the html and save the doctors according to their name (id?)

        ##### TAKEN FROM BA ######
        # get the website from the db
        website_name = response.meta["website_name"]
        website = Website.get(Website.name==website_name)
        # get all links to articles
        if "//" in website.article_identifier:
            r = response.xpath(website.article_identifier)
        else:
            r = response.css(website.article_identifier)
        for r_article in r:
            # create a new article and populate it
            article = Article()
            article.website = website
            article_url = r_article.css("a::attr(href)").extract_first()
            if "http" not in article_url:
                article.url = urljoin(website.url, article_url)
            else:
                article.url = article_url
            article.save()

            self.log('Saved article %s' % article.url)
