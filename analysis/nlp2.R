library("igraph")
library("dplyr")
library("ggplot2")
library("tidyr")
library("tibble")
library("stringr")
library("lubridate")
library("DBI")
library("tidygraph")
library("magrittr")
library("readr")
library("readxl")
library("purrr")
library("visNetwork")
library("data.table")
library("tm")
library("topicmodels")
library("tidytext")

con <- dbConnect(RMySQL::MySQL(),
                 dbname = "dssreviewmining",
                 host = "localhost",
                 port = 3306,
                 user = "root",
                 password = "1234"
)

##### collect data from the database #####

# collect the data

sql_statement_doctors <- "SELECT * FROM `dssreviewmining`.doctor"

all_doctors <- con %>% tbl(sql(sql_statement_doctors)) %>% collect()

sql_statement_reviews <- "SELECT * FROM `dssreviewmining`.review"

all_reviews <- con %>% tbl(sql(sql_statement_reviews)) %>% collect()

##### get additional ressources #####

stop_words_nl <- read.delim("c:/hdm/xampp/htdocs/dss-review-mining/analysis/utils/stopwords-nl.txt", header=FALSE, stringsAsFactors=FALSE)
stop_words_nl_weak <- read.delim("c:/hdm/xampp/htdocs/dss-review-mining/analysis/utils/stopwords-nl-weak.txt", header=FALSE, stringsAsFactors=FALSE)
additional_stop_words <- c("für", "deze", "the", "nt", "and", "de", "sei", "o", "über", "to", "of", "r", "on", "for", "is", "s", "from", "teilen", "var", "2", "können", "to", "i", "a", "the") %>% as.tibble()

emotion_index <- read_excel("c://hdm/bachelorarbeit/analysis/text_mining/resources/NRC-Emotion-Lexicon-v0.92.xlsx")

emotion_index %<>%
  select(English = 'English (en)', Dutch = 'Dutch (nl)', "Positive", "Negative", "Anger", "Anticipation", "Disgust", "Fear", "Joy", "Sadness", "Surprise", "Trust") %>%
  filter(Dutch != "NO TRANSLATION")

##### clean data #####

docs_with_name <- all_doctors %>%
  filter(!is.na(name))

reviews_with_text <- all_reviews %>%
  filter(!is.na(text))

tidy_review_word <- reviews_with_text %>%
  unnest_tokens(word, text) %>%
  as.tibble()

tidy_review_bigram <- reviews_with_text %>%
  unnest_tokens(word, text, token = "ngrams", n = 2) %>%
  as.tibble()

tidy_review_trigram <- reviews_with_text %>%
  unnest_tokens(word, text, token = "ngrams", n = 3) %>%
  as.tibble()

# tables without stopwords

tidy_review_word_clean <- tidy_review_word %>%
  anti_join(stop_words_nl_weak, by = c("word" = "V1")) %>% 
  anti_join(additional_stop_words, by = c("word" = "value"))

tidy_review_bigram_clean <- tidy_review_bigram %>% 
  separate(word, c("word1", "word2"), sep = " ") %>%
  filter(!word1 %in% stop_words_nl_weak$V1,
         !word2 %in% stop_words_nl_weak$V1,
         !word1 %in% additional_stop_words$value,
         !word2 %in% additional_stop_words$value) %>%
  unite(col = word, word1, word2, sep = " ")

tidy_review_trigram_clean <- tidy_review_trigram %>%
  separate(word, c("word1", "word2", "word3"), sep = " ") %>%
  filter(!word1 %in% stop_words_nl_weak$V1,
         !word2 %in% stop_words_nl_weak$V1,
         !word3 %in% stop_words_nl_weak$V1,
         !word1 %in% additional_stop_words$value,
         !word2 %in% additional_stop_words$value,
         !word3 %in% additional_stop_words$value) %>%
  unite(col = word, word1, word2, word3, sep = " ")

# aggregated data - word level

tidy_review_word_clean %>%
  group_by(word) %>%
  summarise(c = n()) %>%
  arrange(desc(c))

tidy_review_bigram_clean %>%
  group_by(word) %>%
  summarise(c = n()) %>%
  arrange(desc(c))

tidy_review_trigram_clean %>%
  group_by(word) %>%
  summarise(c = n()) %>%
  arrange(desc(c))

# aggregated data - review level

reviews_tf_idf_sentiment <- tidy_review_word %>%
  count(id, word) %>%
  bind_tf_idf(word, id, n) %>%
  arrange(desc(tf_idf)) %>%
  inner_join(emotion_index, by = c("word" = "Dutch")) %>%
  group_by(id) %>%
  summarise_at(vars(tf_idf, Positive, Negative, Anger, Anticipation, Disgust, Fear, Joy, Sadness, Surprise, Trust), median) %>% View()
  
