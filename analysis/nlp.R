library("igraph")
library("dplyr")
library("ggplot2")
library("tidyr")
library("tibble")
library("stringr")
library("lubridate")
library("DBI")
library("tidygraph")
library("tidytext")
library("magrittr")
library("readr")
library("readxl")
library("purrr")
library("visNetwork")
library("data.table")

con <- dbConnect(RMySQL::MySQL(),
                 dbname = "dss-mining-review",
                 host = "localhost",
                 port = 3306,
                 user = "root",
                 password = "1234"
)

##### collect data from the database #####

# collect the data

sql_statement_doctors <- "SELECT * FROM `dss-mining-review`.doctor"

all_doctors <- con %>% tbl(sql(sql_statement_doctors)) %>% collect()

sql_statement_reviews <- "SELECT * FROM `dss-mining-review`.review"

all_reviews <- con %>% tbl(sql(sql_statement_reviews)) %>% collect()

##### clean data #####

docs_name <- all_doctors %>%
  filter(!is.na(name))

clean_reviews <- all_reviews %>%
  filter(!is.na(text))


tidy_review_text <- clean_reviews %>%
  unnest_tokens(word, text) %>%
  as.tibble()

tidy_review_text %>% count(word, sort = TRUE)

tidy_review_text %>% group_by(word) %>% summarise(n()) %>% View()

# get stop word (en and ger)
# watch out: utf-encoding (!)
stop_words_nl <- read.delim("c:/hdm/xampp/htdocs/dss-review-mining/analysis/utils/stopwords-nl.txt", header=FALSE, stringsAsFactors=FALSE)
stop_words_nl_weak <- read.delim("c:/hdm/xampp/htdocs/dss-review-mining/analysis/utils/stopwords-nl-weak.txt", header=FALSE, stringsAsFactors=FALSE)
additional_stop_words <- c("für", "the", "sei", "o", "über", "to", "of", "r", "on", "for", "is", "s", "from", "teilen", "var", "2", "können") %>% as.tibble()

extratidy_review_text <- tidy_review_text %>% anti_join(stop_words_nl, by = c("word" = "V1"))

extratidy_review_text %>% count(word, sort = TRUE) %>% View()
