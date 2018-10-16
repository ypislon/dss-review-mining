# -*- coding: utf-8 -*-
import scrapy


class ReviewLinkSpider(scrapy.Spider):
    name = 'review-link'
    allowed_domains = ['zorgkaart.nl']
    start_urls = ['http://zorgkaart.nl/']

    # URLS FOR MINING
    #
    # for all results of a doctor:
    # https://www.zorgkaartnederland.nl/zorgverlener/_NAME_OF_DOCTOR_/waardering
    # e.g. https://www.zorgkaartnederland.nl/zorgverlener/neuroloog-meulen-b-c-ter-278252/waardering

    def parse(self, response):
        pass

        # get all review urls
        # scrape the review urls and get the needed information with the identifiers
        # 
