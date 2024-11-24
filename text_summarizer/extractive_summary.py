import spacy
from heapq import nlargest
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation

def compute_tfidf(sentences):
    #each column is word while each row is a sentence and each cell has the TF-IDF score
    #transforms the text document into matrix
    tfidf_vectorizer=TfidfVectorizer()
    #scoring the occurence of each word in difference sentences  
    tfidf_matrix=tfidf_vectorizer.fit_transform(sentences)
    return tfidf_matrix
def cos_similarity(matrix):
    #checks the similarity between two non-zero vectors
    #helps to reduce redundancy cosine similarity=A.B/|A||B|
    return cosine_similarity(matrix,matrix)
def extractive_summary(text,summary_ratio=2):
    #loading spacy CNN trained model that includes tools for tokenization,POS and etc..
    nlp=spacy.load("en_core_web_sm")
    #process the text using the model
    doc=nlp(text)
    #finding the importance of each word in the text
    word_freq={}
    #weights for each part of speech
    pos_weight={"NOUN":2,"VERB":1.5,"ADV":1,"ADJ":1}
    #loop to check if the word from the txt is not in stopwords and not in punctuation
    for word in doc:
        #word.text because word is a spacy token that might contain many information and we need the string to check here
        if word.text.lower() not in STOP_WORDS and word.text.lower() not in punctuation:
            if word.pos_ in pos_weight:#.pos_ helps to find the part of speech of each word
                #if that part of speec in pos_weight dict and then it checks that if it has already been encountered in the word_freq
                #if not then initializes it to 0 and then adds the pos_weight
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
    tfidf_matrix=compute_tfidf(sents_text)
    cosine_matrix=cos_similarity(tfidf_matrix)
    for i ,sent in enumerate(sentences):
        for j in range(i+1,len(sentences)):
            if cosine_matrix[i][j]>0.3:#if it is greater than 0.3 then there are smilarities 
                sent_scores[sent]-=cosine_matrix[i][j]#removing the sentence
    #length of summary based on the summary ratio.
    select_len=int(len(sentences)*summary_ratio)
    #list of sentences in descending order based on the sentence score.
    summary=nlargest(select_len,sent_scores,key=sent_scores.get)
    #joining
    return " ".join([sent.text for sent in summary])
