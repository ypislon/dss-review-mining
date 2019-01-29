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

##### clean data #####

docs_with_name <- all_doctors %>%
  filter(!is.na(name))

reviews_with_text <- all_reviews %>%
  filter(!is.na(text))

tidy_review_text <- reviews_with_text %>%
  unnest_tokens(word, text) %>%
  as.tibble()

# tidy_review_text %>% count(word, sort = TRUE)
#
# tidy_review_text %>% group_by(word) %>% summarise(n()) %>% View()

# get stop words (english and dutch)
# watch out for the utf-encoding (!)
# could lead to problems with special chars
stop_words_nl <- read.delim("~/Documents/projects/dss-review-mining/analysis/utils/stopwords-nl.txt", header=FALSE, stringsAsFactors=FALSE)
stop_words_nl_weak <- read.delim("~/Documents/projects/dss-review-mining/analysis/utils/stopwords-nl-weak.txt", header=FALSE, stringsAsFactors=FALSE)
additional_stop_words <- c("für", "the", "sei", "o", "über", "to", "of", "r", "on", "for", "is", "s", "from", "teilen", "var", "2", "können") %>% as.tibble()

extratidy_review_text <- tidy_review_text %>% anti_join(stop_words_nl_weak, by = c("word" = "V1")) %>% anti_join(additional_stop_words, by = c("word" = "value"))

# take a first look at the filtered set of words, sorted by occurences
extratidy_review_text %>% count(word, sort = TRUE) %>% View()

##### create networks #####
# we want to look at the reviews in a network, and see which words connect to which reviews
# the goal is to find cluster of words or central words, maybe even cluster the reviews based on their network measurements

review_network <- extratidy_review_text %>%
  select(id, word, score_avg, relevance)

review_words_big <- extratidy_review_text %>%
  select(id, word, score_avg) %>% count(word) %>% filter(n > 20000)

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

# render an interactive network inside of
# can be saved as a html page as well
# take a look at https://datastorm-open.github.io/visNetwork/more.html
graph2 %>% visIgraph() %>%
  visIgraphLayout(layout = desired_layout) %>%
  visOptions(nodesIdSelection = TRUE, highlightNearest = list(enabled = TRUE, hover = FALSE, degree = 1)) %>%
  visInteraction(navigationButtons = TRUE)

# plotting a static image of the network
# if visnetwork doesn't recognize the layout algo
plot(graph2)

graph3 <- graph2 %>% add_layout_(as_bipartite())
plot(graph3)

##### nlp & clustering #####

reviews_headache <- extratidy_review_text %>% filter(disease == "Migraine" | disease == "Clusterhoofdpijn" | disease == "Spanningshoofdpijn")

extratidy_review_text %>% filter(relevance > 5)

# summarized text per keyword
#summarized_text <- extratidy_review_text %>% count(word, sort = TRUE)

# summarized text per review
summarized_text <- extratidy_review_text %>% count(id, word, sort = TRUE)

# summarized_text_migraine <- migraine_text %>% count(id, word, sort = TRUE)
#
# aggregated_keywods_migriane <- summarized_text_migraine %>%
#   bind_tf_idf(word, id, n) %>%
#   arrange(desc(tf_idf))

## term frequency and inverse term frequency
# find the words most distinctive to each document
aggregated_keywods_per_review <- summarized_text %>%
  bind_tf_idf(word, id, n) %>%
  arrange(desc(tf_idf))

## aggregate the keywords and filter the keywords by n() and tf_idf
# "r way" of doing it
#aggregate(aggregated_keywods_per_review$tf_idf, list(aggregated_keywods_per_review$word), median) %>% View()
aggregated_keywords <- aggregated_keywods_per_review %>%
  group_by(word) %>%
  summarise_all(funs(median, sum)) %>%
  select(word, n_sum, tf_median, idf_median, tf_idf_median)

top_keywords <- aggregated_keywords %>% filter(n_sum > 20) %>% filter(tf_idf_median > 0.2)

top_keywords_migraine <- reviews_headache %>%
  count(id, word, sort = TRUE) %>%
  bind_tf_idf(word, id, n) %>%
  arrange(desc(tf_idf)) %>%
  group_by(word) %>%
  summarise_all(funs(median, sum)) %>% select(word, n_sum, tf_median, idf_median, tf_idf_median) %>%
  filter(n_sum > 0)

comparison_migraine <- aggregated_keywords %>%
  inner_join(top_keywords_migraine, by = "word")

## tokenizing by n-grams
# look at the context of the words and word embedding

# tidy_review_text_ngrams <- reviews_with_text %>%
#   unnest_tokens(word, text, token = "ngrams", n = 3) %>%
#   as.tibble() %>%
#   count(word, sort = TRUE)

reviews_bigrams_per_review <- reviews_with_text %>%
  unnest_tokens(word, text, token = "ngrams", n = 2) %>%
  separate(word, c("word1", "word2"), sep = " ") %>%
  filter(!word1 %in% stop_words_nl_weak$V1,
         !word2 %in% stop_words_nl_weak$V1,
         !word1 %in% additional_stop_words$value,
         !word2 %in% additional_stop_words$value) %>%
  unite(col = word, word1, word2, sep = " ")

# count by word and disease
reviews_bigram_per_disease <- reviews_bigrams_per_review %>%
  count(word, disease, sort = TRUE) %>%
  filter(!is.na(disease) & n > 5)
  #count(word, sort = TRUE) %>% View()

aggregated_reviews_bigram_per_review <- reviews_bigrams_per_review %>%
  count(id, word, sort = TRUE) %>%
  bind_tf_idf(word, id, n) %>%
  arrange(desc(tf_idf))

aggregated_reviews_per_disease <- aggregated_reviews_bigram_per_review %>%
  inner_join(reviews_bigram_per_disease, by = c("word" = "word"), copy = TRUE)

reviews_bigrams_per_review_score <- reviews_bigrams_per_review %>%
  group_by(id) %>%
  summarise(n(), score_avg[1])

aggregated_reviews_per_disease %<>%
  inner_join(reviews_bigrams_per_review_score, by = c("id" = "id"), copy = TRUE)

aggregated_reviews_headache <- aggregated_reviews_per_disease %>%
  filter(disease == "Migraine" | disease == "Clusterhoofdpijn" | disease == "Spanningshoofdpijn" | disease == "Nekhernia" | disease == "Nekpijn") %>%
  mutate(score_avg = as.numeric(`score_avg[1]`))

top_n(x = aggregated_reviews_per_disease, n = 10, wt = tf_idf)

ggplot(aggregated_reviews_headache, aes(x = as.numeric(score_avg), y = tf_idf)) +
  geom_point(data = transform(aggregated_reviews_headache, disease = NULL), colour = "grey65") +
  geom_point() +
  facet_wrap(~ disease)

aggregated_reviews_headache

###### network of bi-grams ######
# create network out of tokens

aggregated_reviews_bigram_filtered <- reviews_with_text %>%
  unnest_tokens(word, text, token = "ngrams", n = 2) %>%
  separate(word, c("word1", "word2"), sep = " ") %>%
  filter(!word1 %in% stop_words_nl_weak$V1,
         !word2 %in% stop_words_nl_weak$V1,
         !word1 %in% additional_stop_words$value,
         !word2 %in% additional_stop_words$value) %>%
  count(word1, word2) %>%
  filter(n > 20)

keyword_graph <- ccc2 %>% graph_from_data_frame() %>% as.undirected(mode = c("collapse"))

keyword_graph %>% visIgraph() %>%
  #visIgraphLayout(layout = desired_layout) %>%
  visOptions(nodesIdSelection = TRUE, highlightNearest = list(enabled = TRUE, hover = FALSE, degree = 1)) %>%
  visInteraction(navigationButtons = TRUE)

###### topic modelling ######

review_dtm <- summarized_text %>%
  cast_dtm("id", "word", "n")

review_dtm <- summarized_text %>% cast_dtm(document = "id", term = "word", value = "n")

review_lda <- LDA(review_dtm, k = 3)

review_topics <- tidy(review_lda, matrix = "beta")

top_n(review_topics, 20) %>% arrange(desc(beta))

# ggplot(review_topics, aes(x = round(beta, digits = 5))) +
#   geom_bar() +
#   facet_wrap(~ topic)

review_top_terms <- review_topics %>%
  group_by(topic) %>%
  top_n(10, beta) %>%
  ungroup() %>%
  arrange(topic, desc(beta))

review_top_terms %>%
  mutate(term = reorder(term, beta)) %>%
  ggplot(aes(term, beta, fill = factor(topic))) +
  geom_col(show.legend = FALSE) +
  facet_wrap(~ topic, scales = "free") +
  coord_flip()

# install.packages("tm")
# install.packages("topicmodels")
# library("topicmodels")

review_bigram_dtm <- aggregated_reviews_bigram_per_review %>%
  cast_dtm(document = id, term = word, value = n)

review_bigram_lda <- LDA(review_bigram_dtm, k = 3)

review_bigram_topics <- tidy(review_bigram_lda, matrix = "beta")

# top_n(review_bigram_topics, 20) %>% arrange(desc(beta))

# get an overview of the top terms
review_bigram_top_terms <- review_bigram_topics %>%
  group_by(topic) %>%
  top_n(15, beta) %>%
  ungroup() %>%
  arrange(topic, desc(beta))

review_bigram_top_terms %>%
  mutate(term = reorder(term, beta)) %>%
  ggplot(aes(term, beta, fill = factor(topic))) +
  geom_col(show.legend = FALSE) +
  facet_wrap(~ topic, scales = "free_y") +
  coord_flip()

# see which terms are most common in which groups
review_bigram_top_terms %>% ggplot(aes(x = term, y = beta)) +
  geom_col() +
  facet_wrap(~ topic) +
  coord_flip()

##### Sentiment analysis ######

emotion_index <- read_excel("c://hdm/bachelorarbeit/analysis/text_mining/resources/NRC-Emotion-Lexicon-v0.92.xlsx")

emotion_index %<>%
  select(English = 'English (en)', Dutch = 'Dutch (nl)', "Positive", "Negative", "Anger", "Anticipation", "Disgust", "Fear", "Joy", "Sadness", "Surprise", "Trust") %>%
  filter(Dutch != "NO TRANSLATION")

# get emotion scores for each review
review_emotion_scores <- extratidy_review_text %>%
  inner_join(emotion_index, by = c("word" = "Dutch")) %>%
  group_by(id) %>%
  summarise_if(is.numeric, sd)

# get emotion score for each word
# TODO

###### Per disease analysis ######

aggregated_reviews_headache <- reviews_headache %>%
  count(id, word, sort = TRUE) %>%
  inner_join(reviews_with_text, by = c("id" = "id")) %>%
  select(id, word, n, score_avg, disease)

# interesting: change document = (id, disease)
reviews_headache_topics <- aggregated_reviews_headache %>%
  cast_dtm(document = id, term = word, value = n) %>%
  LDA(k = 3) %>%
  tidy(matrix = "beta")

reviews_headache_top_terms <- reviews_headache_topics %>%
  group_by(topic) %>%
  top_n(15, beta) %>%
  ungroup() %>%
  arrange(topic, desc(beta))

reviews_headache_top_terms %>%
  mutate(term = reorder(term, beta)) %>%
  ggplot(aes(term, beta, fill = factor(topic))) +
  geom_col(show.legend = FALSE) +
  facet_wrap(~ topic, scales = "free") +
  coord_flip()
