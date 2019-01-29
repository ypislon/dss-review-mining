# Web crawler and analysis tools for healthcare reviews in the Netherlands
___

Data mining, processing and analysis for doctors and their reviews in and around Amsterdam, with the focus on headache and migraine patients.
___

This repository was created as part of the "Digital Society School" programme at the University of Applied Sciences Amsterdam.

The goal of this prototype is understand better how people who suffer from migraine or severe headache think about doctors and what possible points of friction there are. The quantitative methods of data mining, natural language processing, network analysis and topic modelling are applied to gather said results.

The repo contains the setup for a web crawler, the database needed to store the results of the crawler, and scripts to analyse the fetched data.

## Database

The database is implemented with the help of the ORM Peewee in Python. A main reason is that the web crawler, which needs to access the database, is written in Python. Implementing the ORM in Python helps you to easily store data with the web crawler. If you want, you can implement any common type of database, in this project we chose MySQL / MariaDB. It provides sufficient support for both Peewee and R.

## Web crawler

The web crawler is written in Python, using the `scrapy` framework. There are four crawlers, which take care of gathering all links for doctors and reviews, as well as fetching the available data for doctors and reviews. The data gets written to the database synchronously while crawling. For the sake of simplicity the crawlers are split up and can be executed directly from the terminal.

## Analysis

Analysing the dataset is done in R. We can fetch the data from the database and perform our analysis in runtime. The results of the analysis range from descriptive statistics to modelling different topics, based on keywords in the reviews.

## Run the project

- Install your favorite python distribution with a version >3.6. ([Python](https://www.python.org/downloads/) or [Anaconda](https://www.anaconda.com/download/)).
- Make sure you add it to your path or in case of Anaconda, create a virtual environment and use the anaconda prompt to be able to execute terminal commands
- Install [R (version > 3.5)](https://cran.r-project.org/mirrors.html)

#### Database

- Before you set up the database the first time, you need to install the [`peewee` package](http://docs.peewee-orm.com/en/latest/) with a Python package manager of your preference ([pip](https://pypi.org/project/pip/))
- If you want to understand the schema of the database, look at `db_schema.py`. There are tables for doctors, reviews and identifiers (for the spider). All fields and relationships are defined in this script with the help of peewee.
- Edit `db_connection.py` to fit your preferences
- Run the python script `db_init.py` from the terminal to create and initialize the database

#### Web cralwer

- Before running the web crawler for the first time, you need to install the [`scrapy` package](https://scrapy.org/) with a Python package manager of your preference
- To run the spider and mine data about doctors and the respective reviews, navigate in the terminal to the `/spider/spider/spiders` folder and execute following commands:
  - Fetch all links to the pages of doctors: `scrapy crawl doctorlinkspider`
  - Fetch all information from the pages of doctors: `scrapy crawl doctorinfospider`
  - Fetch all links to the reviews of each doctor: `scrapy crawl reviewlinkspider`   
  - Fetch all information from the review pages, including review text: `scrapy crawl reviewinfospider`

#### Analysis

- We worked with [RStudio](https://www.rstudio.com/) and highly recommend working with the editor. It makes it easy to understand the steps taken in the project and look at results before exporting graphs/numbers.
- Run the different scripts inside the `analysis` folder
- Running the scripts will first install all needed scripts (see the "packages" section of each file)
- Set up the database connection according to your needs in each script
- Afterwards you can choose to render the different results
  - `descriptive_statistics.r`: provides descriptive statistics about the gathered data and provides a first look into standard measurements like average score, number of reviews per doctor, number of review per disease etc. Here you can export graphs with the `ggplot2` package which provide basic information about the dataset.
  - `nlp.r` and `nlp2.r` provide further analysis to gain a better understanding of important topics, using the methods of natural language processing, network analysis and unsupervised topic modelling. Here you can export network graphs via `visNetwork` as well as results of NLP/topic modelling via `ggplot2`.
