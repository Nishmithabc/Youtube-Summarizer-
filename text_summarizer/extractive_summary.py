import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation

def compute_tfidf(sentences):
    #each column is document while each row is a word ad each cell has the TF-IDF score
    #transforms the text document into matrix
    tfidf_vectorizer=TfidfVectorizer()
    #scoring the occurence of each word in difference sentences  
    tfidf_matrix=tfidf_vectorizer.fit_transform(sentences)
    return tfidf_matrix
def cos_similarity(matrix):
    #checks the similarity between two non-zero vectors
    #helps to reduce redundancy cosine similarity=A.B/|A||B|
    return cosine_similarity(matrix,matrix)
def extractive_summary(text,summary_ratio=0.4):
    #loading spacy small model that includes tools for tokenization,POS and etc..
    nlp=spacy.load("en_core_web_sm")
    #text processed by spacy
    doc=nlp(text)
    #importance of each word in the text
    word_freq={}#dict
    #weights for each part of speech
    pos_weight={"NOUN":2,"VERB":1.5,"ADV":1,"ADJ":1}
    #a loop to check if the word from the txt is not in stopwords and not in punctuation
    for word in doc:
        #word.text because word is a spacy token that might contain many information and we need the string to check here
        if word.text.lower() not in STOP_WORDS and word.text.lower() not in punctuation:
            if word.pos_ in pos_weight:
                #if that word is a pos then it checks that if it has already been encountered in the word_freq
                #if not then initializes to 0 and then adds the pos_weight
                word_freq[word.text]=word_freq.get(word.text,0)+pos_weight[word.pos_]
    #normalization of the word_frequency while taking maximum frequency and dividing it with freq of each words in the dict 
    max_freq=max(word_freq.values())
    word_freq={word:freq/max_freq for word,freq in word_freq.items()}
    #sentence segmentation from the processed doc
    sentences=list(doc.sents)
    #extracting the line from the text
    sents_text=[sent.text for sent in sentences]
    sent_scores={}
    '''looping over each sentence and word in that sentence and checking if that word is in word_freq
    if yes then the value of word_freq is going to get added with sent 
    this value is then inputed into sent_scores'''
    for sentence in sentences:
        for word in sentence:
            if word.text in word_freq:
                #sentence with many high freq words scores higher
                sent_scores[sentence]=sent_scores.get(sentence,0)+word_freq[word.text]
    '''TF-IDF term frequency inverse document frequency
    used to determine importance of each word in a document'''
    tfidf_matrix=compute_tfidf(sentences)
    cosine_matrix=cos_similarity(tfidf_matrix)


