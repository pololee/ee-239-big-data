library("tm")
library("topicmodels")
library("slam") #for rollup
library("nnet") #for which.is.max
library("stringr") #for str_replace
library("Rcmdr") # for plot and save plot

# TUAN
# 02-21-2014
# Return a vector containing all the answers from a given file_name
extract_answers <- function(text) {
    num_lines <- length(text)

    # Create an empty document vector
    answers <- {}

    for (line in text) {
        line_length <- nchar(line)
        if (line_length != 0) {
            # This loop is to detect the first space and remove "Answer: "
            for (j in 1:line_length) {
                # Note that topic that does not have the answer is repsented as " "
                # not an empty string.
                if (substring(line,j,j) == " ") {
                    first_word <- substring(line,1,j-1)
                    if (first_word == "Answer:") {
                        extracted_answer <- substring(line,j+1,line_length) 
                        # j+1 to not include the space
                        if (extracted_answer != "") {
                        answers <- c(answers, extracted_answer) # ignore empty document
                        }
                        # print(extracted_answer)
                    }
                    break # Stop searching for the space
                }
            }
        }
    }

    return(answers)
}

# TUAN, POLO, LAUREN
# 02-20-2014
# Return a DocumentTermMatrix
get_dtm<-function(docs) {
    # Create a Corpus from docs
    corpus <- Corpus(VectorSource(docs), readerControl = list(language = "en"))

    # convert to lower case 
    # because if not, it will not remove stopwords
    # uppercase refer to a name
    # print("tm_map 1")
    corpus <- tm_map(corpus, tolower)

    # Remove stopwords
    # print("tm_map 2") 
    corpus <- tm_map(corpus, removeWords, stopwords("SMART"))

    # remove stopwords
    corpus <- tm_map(corpus, removeWords, stopwords("english"))

    # Remove extra whitespace
    # print("tm_map 3")
    corpus <- tm_map(corpus, stripWhitespace)

    # Remove Punctuation
    # print("tm_map 4")
    corpus <- tm_map(corpus, removePunctuation, preserve_intra_word_dashes = TRUE)

    # Remove numbers
    # print("tm_map 5")
    corpus <- tm_map(corpus, removeNumbers)
    # dont, doesnt, itll, theyll, nbsp)
    # remove

    # remove (hes, shes, im, its, youre, theyre, 
    # embed and quote
    # (embed quote appears from 
    # HTML tags that are not removed properly when crawling)
    # print("tm_map 6")
    nonMeaningWords <- c("embed", "quote", "hes", "shes",
                         "im", "its", "youre", "theyre",
                         "dont", "doesnt", "itll", "theyll",
                         "nbsp", "people", "quoteanswered",
                         "time", "quora", "aap", "quotethis")
    corpus <- tm_map(corpus, removeWords, nonMeaningWords)

    # Create document-term matrix
    # print("construct dtm")
    dtm <- DocumentTermMatrix(corpus)
    # print("done")

    return(dtm)
}


# POLO
# 02-20-2014
# To take care of the following error:
#   Error in LDA(dtm, 50, method = "VEM") : 
#   Each row of the input matrix needs to contain at least one non-zero entry
get_zero_row<-function(docTm, delimit){
    dtmPart <- docTm[,1:delimit]
    rowTotal <- as.vector(rollup(dtmPart, 2))
    numRow <- length(rowTotal)
    indexVec <- vector()
    for (i in 1:numRow) {
        if(rowTotal[i] == 0) {
            indexVec <- c(indexVec, i)
        }
    }
    rm(dtmPart)
    return(indexVec)
}


# TUAN
# 02-20-2014
write_vector_to_file <- function(vec, num_of_topic, num_of_top_word, file_name) {
    sink(file_name)
    start <- 1
    end <- num_of_top_word
    for (i in 1:num_of_topic) {
        local_vec <- vec[start:end] #inclusive
        start <- start + num_of_top_word
        end <- end + num_of_top_word

        words <- paste(local_vec, collapse=", ") #result: "word1, word2, ..."
        line <- paste("Topic ", i, ": ", words, sep="") #result: "Topic i: word1, word2, ..."
        cat(line)
        if (i < num_of_topic) {
            cat("\n")
        } else {
            sink() #return output to the terminal
        }
    }
}

# TUAN
# 02-21-2014
# Count number of words in a document
count_words <- function(doc) {
    # makes sure all words are separated by one space only,
    # by replacing all occurences of two or more spaces with one space
    doc <- gsub(' {2,}',' ',doc)
    result <- length(strsplit(doc,' ')[[1]])
    return(result)
}

# TUAN
# 02-21-2014
# Return a random number in [start,end] (inclusive)
# that does not appear in num_vec
random_number <- function(start, end, num_vec) {
    while (1) {
        #get a single random number in [start,end]
        rand_num <- sample(seq(start, end), 1)
        if (!any(num_vec == rand_num)) { #not in the list
            return(rand_num)
        }
    }
}

# TUAN
# 02-21-2014
# Given all documents, return 5 random documents
# that have more than 100 words each
get_five_random_docs <- function(all_docs) {
    result <- {}
    random_list <- {} #list of unique random numbers seen so far
    count <- 1
    num_doc <- length(all_docs)
    while (count <= 5) {
        #get a random number that is not yet in the random_list
        rand_num <- random_number(1, num_doc, random_list)
        doc <- all_docs[rand_num]
        if (count_words(doc) > 100) {
            count <- count + 1
            result <- c(result, doc)
            random_list <- c(random_list, rand_num)
        }
    }
    return(result)
}

# Help function
# input: dtm (document term matrix)
# output: dtm
# In order to avoid the following error
#   Each row of the input matrix needs to contain 
#   at least one non-zero entry
# process DTM to make LDA comfortable
remove_zero_row <- function(dtm) {
    delimit <- ncol(dtm)
    indexVector <- get_zero_row(dtm, delimit)
    if(length(indexVector) == 0 ){
        return(dtm)
    }
    dtm <- dtm[-indexVector,]
    return(dtm)
}

draw_All_bars <- function(distriMatrix, picName) {
    num_of_row <- nrow(distriMatrix)
    for (i in 1:num_of_row) {
        onePicName <- paste(i, picName, sep = "-")
        draw_barplot(distriMatrix[i,], onePicName)
    }
}

draw_barplot <- function(distriVec, picName) {
    jpeg(picName)
    num_of_index <- length(distriVec)
    barplot(distriVec, horiz=TRUE, names.arg=c(1:num_of_index))
    dev.off()
}

# Help function: use LDA to do model training
# input: 
#   document term matrix
#   k value
# output:
#   the output of LDA, that is topic model
#  
# Note: automatically estimated alpha is default configuration
get_trained_model <- function(dtm, k_Value) {
    lda <- LDA(dtm, method="VEM", k=k_Value)
    return(lda)
}

# Help function
# input: 
#   doc: which is vector
#   lda: trained topic model
# output: the topic num which has highest probability
get_closest_topic_num <- function(doc, lda) {
    doc_term_matrix <- get_dtm(doc)
    if(ncol(doc_term_matrix) == 0) {
        return(-1)
    }
    doc_term_matrix <- remove_zero_row(doc_term_matrix)
    if(nrow(doc_term_matrix) == 0) {
        return(-1)
    }
    distri <- posterior(lda, doc_term_matrix)
    distri_matrix <- distri$topics
    prob_vec <- distri_matrix[1,]
    return(which.is.max(prob_vec))
}

# TUAN
# 02-22-2014
# For each label in top_label_vec,
# extract top n words from file lda_k_topics.txt
# return a list of vectors. Each vector stores top 10 words
extract_top_n_words <- function(top_label_vec, n, k) {
    file_name <- paste("lda_",k,"_topics.txt",sep="")
    lines <- readLines(file_name)
    result <- list()
    top_label_vec_length <- length(top_label_vec)
    length(result) <- top_label_vec_length
    for (i in 1:top_label_vec_length) {
        label <- top_label_vec[i]
        topic <- paste("Topic ", label, ": ", sep="")
        top_words <- str_replace(lines[label], topic, "")
        temp <- unlist( strsplit(top_words, ", "))
        result[[i]] <- temp[1:n] #get top n words
    }
    return(result)
}



################# END OF HELPER FUNCTIONS #################



# TUAN, POLO, LAUREN
# 02-20-2014
# Question 1
question_1 <- function(dtm) {
    # process DTM to make LDA comfortable
    delimit <- ncol(dtm)
    indexVector <- get_zero_row(dtm, delimit)
    dtm <- dtm[-indexVector,]

    # Train the model
    lda_result_2 <- LDA(dtm, 2, method="VEM")
    lda_result_2_vec <- terms(lda_result_2, 20)
    lda_2_topics_file_name <- "lda_2_topics.txt"
    write_vector_to_file(lda_result_2_vec, 2, 20, lda_2_topics_file_name)

    lda_result_10 <- LDA(dtm, 10, method="VEM")
    lda_result_10_vec <- terms(lda_result_10, 20)
    lda_10_topics_file_name <- "lda_10_topics.txt"
    write_vector_to_file(lda_result_10_vec, 10, 20, lda_10_topics_file_name)

    lda_result_50 <- LDA(dtm, 50, method="VEM")
    lda_result_50_vec <- terms(lda_result_50, 20)
    lda_50_topics_file_name <- "lda_50_topics.txt"
    write_vector_to_file(lda_result_50_vec, 50, 20, lda_50_topics_file_name)
}



# POLO
# 02-21-2014
# for question 2
question_2 <- function(dtmAll, dtmFiveDoc, k_Value) {

    dtmAll <- remove_zero_row(dtmAll)
    dtmFiveDoc <- remove_zero_row(dtmFiveDoc)
    ############################################
    #
    # first case: automatically estimate alpha
    # 
    # ##########################################
    # training the topic model with automatically estimated alpha
    
    lda_esti_alpha <- LDA(dtmAll,k_Value ,method="VEM", control=list(estimate.alpha=TRUE))

    # get estimated value of alpha
    esti_value_alpha <- attr(lda_esti_alpha, "alpha") # $ is used to access the member of the class

    #show estimated value of alpha on screen
    sink("alpha-Q2.txt")
    esti_value_alpha
    sink()

    # write the top 20 words of each topic in a file
    lda_vec <- terms(lda_esti_alpha, 20)
    lda_vec_file <- paste("lda_",k_Value,"_topics.txt",sep="")
    write_vector_to_file(lda_vec, k_Value, 20, lda_vec_file)

    # Determine the posterior probabilities of the topics for each document
    distri_esti_alpha <- posterior(lda_esti_alpha, dtmFiveDoc)

    # get the probability distribution matrix
    # row: document
    # column: topics
    # # value of each position: 
    # #  the probability that the document falls into this topic
    distriMatrix_esti_alpha <- round(distri_esti_alpha$topics, digits = 2)
    
    # show you the current directory
    # the barplot will be saved in this folder
    getwd()
    picName_esti_alpha <- "esti-alpha.jpg"
    draw_All_bars(distriMatrix_esti_alpha, picName_esti_alpha)

    # plot values of beta for 3 different topics
    betaMatrix_esti_alpha <- attr(lda_esti_alpha,"beta")[1:3, ]
    betaPic_esti_alpha <- "beta-esti-alpha.jpg"
    draw_All_bars(betaMatrix_esti_alpha, betaPic_esti_alpha)
    betaPic_Exp_esti_alpha <- "beta-exp-esti-alpha.jpg"
    draw_All_bars(exp(betaMatrix_esti_alpha), betaPic_Exp_esti_alpha)

    #############################################
    #
    # second case: fix alpha value
    # 
    # ###########################################
    # training the model with fixed alpha = 50/k
    lda_fixed_alpha <- LDA(dtmAll, k_Value ,method="VEM", control = list(alpha = 50/k_Value))

    # get the distribution given the new training topic Model
    distri_fixed_alpha <- posterior(lda_fixed_alpha, dtmFiveDoc)
    distriMatrix_fixed_alpha <- round(distri_fixed_alpha$topics, digits=2)
    picName_fixed_alpha <- "fixed-alpha.jpg"
    draw_All_bars(distriMatrix_fixed_alpha, picName_fixed_alpha)

    # plot values of beta for 3 different topics
    betaMatrix_fixed_alpha <- attr(lda_fixed_alpha,"beta")[1:3,]
    betaPic_fixed_alpha <- "beta-fixed-alpha.jpg"
    draw_All_bars(betaMatrix_fixed_alpha, betaPic_fixed_alpha)
    betaPic_Exp_fixed_alpha <- "beta-exp-fixed-alpha.jpg"
    draw_All_bars(exp(betaMatrix_fixed_alpha), betaPic_Exp_fixed_alpha)


    ##################
    #
    # After question 2, we always use this topic model
    # 
    # @@@@@@@@@@@@@@@
    
    return(lda_esti_alpha)
}

# TUAN
# 02-21-2014
# k is the number of topics. For example, k=50
question_3 <- function(text, k, num_quora_topics, num_labels, lda) {
    topic_line_numbers <- grep("Topic:",text)
    topic_line_numbers_length <- length(topic_line_numbers)
    topics <- {}
    for (i in 1:topic_line_numbers_length) {
        topic_line <- topic_line_numbers[i]
        topics <- c(topics,text[topic_line])
    }

    # We do not worry about grep the entire answer that has the topic name
    # appears there. When we call "table", topic names will be aggregated
    # correctly.
    count_table <- table(topics) # show the number of occurances for each topic
    count_table_length <- length(count_table) #1120 unique topics
    count_values <- unname(count_table) #get frequency list only, ignore topic

    top_five_quora_topics <- {}
    for (i in 1:num_quora_topics) {
        max_index <- which.is.max(count_values)
        count_values[max_index] <- -1 #next time, we won't find this index again
        topic_name <- names(count_table[max_index])
        top_five_quora_topics <- c(top_five_quora_topics, topic_name)
        print(count_table[max_index])
    }

    topic_answers <- list()
    length(topic_answers) <- num_quora_topics #vector of 5 vectors
                               #do this to prevent index out of bound
    i <- 1

    num_of_lines <- length(text)
    while (i < num_of_lines) {
        if (substring(text[i],1,1) == "T") {
            for (j in 1:num_quora_topics) {
                if (text[i] == top_five_quora_topics[j]) {
                    #print("Match")
                    answer <- str_replace(text[i+1], "Answer:","")
                    if (answer != "" || answer != " ") {
                        topic_answers[[j]] <- c(topic_answers[[j]], answer)
                    }
                    i <- i+1 #skip answer line in next i iteration
                    break #break the for loop
                }
            }
            i <- i+1
        } else {
            i <- i+1
        }
    }

    sink("quora_topics_output.txt")

    # Assign a label for each answer for each Quora topic
    # (what topic it belongs to)
    for (i in 1:num_quora_topics) {
        label_count <- vector(mode="numeric",length=k)
        top_label_count <- vector(mode="numeric",length=num_labels)
        top_label  <- vector(mode="numeric",length=num_labels)

        answers_per_quora_topic <- topic_answers[[i]]
        num_answer_per_quora_topic <- length(answers_per_quora_topic)
        for (j in 1:num_answer_per_quora_topic) {
            label <- get_closest_topic_num(answers_per_quora_topic[j], lda)
            if (label != -1) {
                label_count[label]  <- label_count[label] + 1
            }
        }

        # get top num_labels that have highest count
        for (w in 1:num_labels) {
            max_index <- which.is.max(label_count)
            top_label[w] <- max_index
            top_label_count[w] <- label_count[max_index] 
            label_count[max_index] <- -1 #next time, we won't find this index again
        }

        #print("TUANTUAN DEBUG DEBUG TUANTUAN")
        #print(top_label)
        #print(top_label_count)

        ### Write to file quora_topics_output.txt

        #extract top 10 words from file lda_k_topics.txt        
        list_result <- extract_top_n_words(top_label, 10, k)
        
        line <- paste("[", top_five_quora_topics[i], "]:\n", sep="")
        cat(line)

        for (counter in 1:num_labels) {
            line <- paste("top topic ", counter, ":", "[", top_label_count[counter], "]\n", sep="")
            cat(line)
            word_vector <- list_result[[counter]]
            word_vector_length <- length(word_vector)
            line <- ""
            for (counter2 in 1:word_vector_length) {
                line <- paste(line, "[", word_vector[counter2], "]", sep="")
                if (counter2 < word_vector_length) {
                    line <- paste(line, ", ", sep="")
                } else {
                    line <- paste(line, "\n", sep="")
                }
            }
            cat(line)
        }

        if (i < num_quora_topics) {
            cat("\n\n")
        }
    }

    sink() #return output to the terminal
}

# TUAN
# 02-22-2014
# k is the number of topics. For example, k=50
question_4 <- function(answers, k, lda) {
    label_count <- vector(mode="numeric",length=k)
    num_of_docs <- length(answers)

    for (answer in answers) {
        # Assign a topic to each document
        label <- get_closest_topic_num(answer, lda)
        if (label != -1) {
            # Aggregate number of documents classified as topic "label"
            label_count[label] <- label_count[label] + 1
        } else { #ignore document that will not be classified
            num_of_docs <- num_of_docs - 1
        }
    }

    # print(sum(label_count))
    # print(num_of_docs)
    # print(label_count)

    prior_prob_vec <- vector(mode="numeric",length=k)
    for (i in 1:k) {
        prob <- label_count[i] / num_of_docs
        prior_prob_vec[i] <- prob
    }

    # print(prior_prob_vec)

    # draw the topic probabilities
    draw_barplot(prior_prob_vec, "topic-prob-Q4.jpg")
    return(prior_prob_vec)
}


# Question 5
# doc: a single document, it's a vector
#   assume the doc has more than 100 words (spec of question 2)
# lda: the LDA topic model from question 2
# return: probability of the doc falls into each topic
oneDoc_topic_dis<-function(prior_prob_vec, doc, lda) {
    one_dtm <- get_dtm(doc)
    words_vec <- colnames(one_dtm) # all the words in the dtm


    num_of_topic <- attr(lda, "k") # number of topics


    terms_vec <- attr(lda, "terms") # all the term in lda 

    # the probability that a word occurring in the topic
    # matrix
    # row: topic label or id
    # column: term or word
    betaMatrix <- attr(lda,"beta")
    wtp_matrix <- exp(betaMatrix) ## word occurrence probability in topic

    result_prob_vec <- vector(mode="numeric",length=num_of_topic)

    for (idx_topic in 1:num_of_topic) {
        one_prob <- 1
        for (word in words_vec) {
            term_idx <- which(terms_vec == word)
            if(term_idx != 0) {
                word_occur_prob <- wtp_matrix[idx_topic, term_idx]
                one_prob <- one_prob * word_occur_prob
            }
        }
        # for loop: get the product of all the word occurring probability P(w_j | T_i)
        # the result is P(doc | T_i)
        if(one_prob ==1 ) {
            result_prob_vec[idx_topic] <- 0
        }
        else {
            result_prob_vec[idx_topic] <- one_prob * prior_prob_vec[idx_topic]
            # get the product = P(doc | T_i) P(T_i)
        }
    }
    # From spec: "You can calculate p(doc) using the equation sum p(T_i|doc) = 1"
    if(sum(result_prob_vec) != 0) {
        return(result_prob_vec/sum(result_prob_vec))        
    }
    return(vector(mode="numeric",length=num_of_topic))
}

# topic_prob_vec: the result of question 4
# five_doc: created in question 2
#   each topic has more than 100 words
# lda: created in question 2
# 
question_5 <- function(topic_prob_vec, five_doc, lda) {
    num_of_doc <- length(five_doc)
    q_5_name <- "doc-Topic_dis.jpg"
    for (idx in 1:num_of_doc) {
        t_distri_vec <- oneDoc_topic_dis(topic_prob_vec, five_doc[idx], lda)
        plotName <- paste(idx, q_5_name, sep="-")
        draw_barplot(t_distri_vec, plotName)
    }
}

############################# MAIN ########################################

#file_name <- "C:\\Users\\tuanle.tuanle-PC\\Dropbox\\ee239as-proj\\proj2\\answers_text.txt"
#
print("please check the file path")
print("for question 4")
print("make sure lda_k_topics.txt in current folder")

file_name <- "answers_text.txt"
text <- readLines(file_name, encoding = "UTF-8")

print("start reading answers")
answers <- extract_answers(text)

# DEBUG:
# print("start debugging")
# file_name <- "/Users/pololee/Dropbox/proj2/small_answers_text2.txt"
# answers <- extract_answers(file_name)

print("start create dtm")
dtm <- get_dtm(answers)

# question_1(dtm)


### Question 2
five_doc <- get_five_random_docs(answers)
dtm_five_doc <- get_dtm(five_doc)
k_Value <- 13
print("start question 2")
lda <- question_2(dtm, dtm_five_doc, k_Value)



### Question 3
print("start question 3")
question_3(text,k_Value,5,5,lda)


### Question 4
print("start question 4")
prior_prob_vec <- question_4(answers, k_Value, lda)

### Question 5
print("start question 5")
question_5(prior_prob_vec, five_doc, lda)

