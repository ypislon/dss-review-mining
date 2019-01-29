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

install.packages("igraph")
install.packages("dplyr")
install.packages("ggplot2")
install.packages("tidyr")
install.packages("tibble")
install.packages("stringr")
install.packages("lubridate")
install.packages("DBI")
install.packages("tidygraph")
install.packages("tidytext")
install.packages("magrittr")
install.packages("readr")
install.packages("readxl")
install.packages("purrr")
install.packages("visNetwork")
install.packages("data.table")

install.packages("RMariaDB")
install.packages("odbc")
install.packages("dbplyr")

library("dbplyr")

##### setup the database #####
# uncomment the following lines and edit the credentials for your needs
#con <- dbConnect(RMariaDB::MariaDB(),
#                 dbname = "dssreviewmining",
#                 host = "localhost",
#                 port = 3306,
#                 user = "root",
#                 password = "password"
#)

##### collect data from the database #####

# collect the data

sql_statement_doctors <- "SELECT * FROM `dssreviewmining`.doctor"

all_doctors <- con %>% tbl(sql(sql_statement_doctors)) %>% collect()

sql_statement_reviews <- "SELECT * FROM `dssreviewmining`.review"

all_reviews <- con %>% tbl(sql(sql_statement_reviews)) %>% collect()

##### cleanup data ######

### docs
docs_clean <- all_doctors %>%
  filter(!is.na(name)) %>%
  mutate(recommendation = as.numeric(str_extract(recommendation, "[\\d]+"))) %>%
  mutate(name = str_trim(name)) %>%
  mutate(`function` = str_trim(`function`)) %>%
  mutate(gender = str_trim(gender)) %>%
  mutate(workplace = str_trim(workplace))

docs_full_set <- all_doctors %>%
  filter(!is.na(name) & !is.na(`function`) & !is.na(gender) & !is.na(workplace))

### reviews
reviews_clean <- all_reviews %>%
  filter(!is.na(text)) %>%
  mutate(score_avg = as.numeric(score_avg)) %>%
  mutate(reference = as.numeric(reference)) %>%
  mutate(relevance = as.numeric(relevance)) %>%
  mutate(text = str_trim(text)) %>%
  mutate(disease = str_trim(disease)) %>%
  mutate(level_1 = str_trim(level_1)) %>%
  mutate(level_2 = str_trim(level_2)) %>%
  mutate(level_3 = str_trim(level_3)) %>%
  mutate(level_4 = str_trim(level_4)) %>%
  mutate(level_5 = str_trim(level_5)) %>%
  mutate(level_6 = str_trim(level_6))

reviews_full_set <- all_reviews %>%
  filter(!is.na(text) & !is.na(disease) & !is.na(score_avg))

reviews_clean_migraine <- reviews_clean %>%
  filter(disease == "Migraine" | disease == "Spanningshoofdpijn" | disease == "Clusterhoofdpijn")

##### generate descriptive statistics

# example:
#counted_articles <- all_articles %>%
#  filter(as.Date(date_published)>="2016-03-01" | is.na(date_published)) %>%
#  inner_join(all_websites, by = c("website_id" = "id")) %>%
#  group_by(name) %>%
#  summarise(article_count = n(), id = website_id[1])

### doctors
ggplot(docs_clean, aes(x = gender)) +
  geom_bar()

ggplot(docs_clean, aes(x = `function`)) +
  geom_bar()

ggplot(docs_clean, aes(x = `workplace`)) +
  geom_bar()

ggplot(docs_clean, aes(x = `recommendation`)) +
  geom_bar() +
  labs(title = "Distribution of the recommendation score of all doctors", subtitle = "Total number of doctors with a recommendation score: 964") +
  xlab("Recommendation (in %)") +
  ylab("Number of doctors")

### reviews
ggplot(reviews_clean, aes(x = score_avg)) +
  geom_bar() +
  labs(title = "Distribution of the score of all reviews", subtitle = "Total number of reviews: 60455") +
  xlab("Average Score") +
  ylab("Number of reviews")

ggplot(reviews_clean_migraine, aes(x = score_avg)) +
  geom_bar(aes(fill = disease)) +
  labs(title = "Distribution of the score of reviews about headache", subtitle = "Total number of reviews: 466") +
  xlab("Average Score") +
  ylab("Number of reviews")

ggplot(reviews_clean, aes(x = disease)) +
  geom_bar()

# get a look at top diseases
reviews_clean %>%
  group_by(disease) %>%
  summarise(n = n()) %>%
  arrange(desc(n)) %>% View()

# look at relevance of reviews
reviews_clean$relevance <- reviews_clean$relevance %>% replace_na(0)
ggplot((reviews_clean %>% replace_na(relevance = 0)), aes(x = relevance)) +
  geom_bar() +
  xlim(0, 40) +
  ylim(0, 10000)
