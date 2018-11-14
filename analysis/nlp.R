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

##### create network ##### 

review_network <- extratidy_review_text %>%
  select(id, word, score_avg, relevance)

review_words_big <- extratidy_review_text %>%
  select(id, word, score_avg) %>% count(word) %>% filter(n > 200)

review_network_small <- review_network %>%
  filter(word %in% review_words_big$word)

graph2 <- graph_from_data_frame(review_network_small)

V(graph2)$deg_in <- degree(graph2, mode="in")
V(graph2)$size <- V(graph2)$deg_in * 0.05
#V(graph2)$size <- V(graph2)$score_avg

graph2

review_nodes <- which(is.numeric(V(graph2)$name))

# V(graph2)$score_avg <- V(graph2)

for (v in V(graph2)) {
  for (j in reviews_clean) {
    if(V(graph2)[v]$name == j) {
      V(graph2)[v]$score_avg <- reviews_clean[j]$score_avg
    }
  }
}

V(graph2)[18]

graph2

for (v in V(graph2)) {
  if(is.na(as.numeric(V(graph2)[v]$name))) {
    # do something with the keyword nodes
    V(graph2)[v]$color <- "#84a07c"
    V(graph2)[v]$label <- V(graph2)[v]$name
    V(graph2)[v]$type <- TRUE
  } else if(as.numeric(V(graph2)[v]$name) > 0) {
    # do something with the review nodes
    V(graph2)[v]$label <- NA
    V(graph2)[v]$label.color <- "transparent"
    V(graph2)[v]$type <- FALSE
  }
}

# desired layout
# options:
# layout_with_kk
# layout_with_graphopt
# layout_with_lgl
# layout_with_drl
# layout_as_bipartite
desired_layout <- "layout_as_bipartite"

graph2 %>% visIgraph() %>%
  visIgraphLayout(layout = desired_layout) %>%
  visOptions(nodesIdSelection = TRUE, highlightNearest = list(enabled = TRUE, hover = FALSE, degree = 1)) %>%
  visInteraction(navigationButtons = TRUE)

# plotting a static image of the network
# if visnetwork doesn't recognize the layout algo
graph3 <- graph2 %>% add_layout_(as_bipartite())
plot(graph3)


##### nlp & clustering #####

extratidy_review_text %>% filter(disease == "Migraine")

extratidy_review_text %>% filter(relevance > 5)

summarized_text <- extratidy_review_text %>% count(id, word, sort = TRUE)


## term frequency and inverse term frequency
# find the words most distinctive to each document
aggregated_keywods <- summarized_text %>%
  bind_tf_idf(word, id, n) %>%
  arrange(desc(tf_idf))


