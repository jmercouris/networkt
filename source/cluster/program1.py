from configparser import ConfigParser
from graph.graph import Graph
import os
import re
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
import nltk
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans

# Load StopWords
stopwords = stopwords.words('english')
    
# Load English Stemmer
stemmer = SnowballStemmer("english")


def tokenize_and_stem(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    stems = [stemmer.stem(t) for t in filtered_tokens]
    return stems


def tokenize_only(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    return filtered_tokens


if __name__ == "__main__":
    config = ConfigParser()
    config.read(os.path.expanduser('~/.config/networkt/cluster.ini'))
    DATABASE_NAME = 'sqlite:///{}/data_store.db'.format(config.get('persistence-configuration', 'database_path'))
    
    graph = Graph(DATABASE_NAME)
    statuses = graph.load_statuses()
    documents = []
    
    for status in statuses[0:5000]:
        # Apply Transformation to Strip URLS
        tmp_text = status.text
        tmp_text = re.sub(r"http\S+", "", tmp_text)
        documents.append(tmp_text)
    print(len(documents))
    
    # Use extend so it's a big flat list of vocab
    totalvocab_stemmed = []
    totalvocab_tokenized = []
    for i in documents:
        allwords_stemmed = tokenize_and_stem(i)  # for each item in 'documents', tokenize/stem
        totalvocab_stemmed.extend(allwords_stemmed)  # extend the 'totalvocab_stemmed' list
    
        allwords_tokenized = tokenize_only(i)
        totalvocab_tokenized.extend(allwords_tokenized)
    
    vocab_frame = pd.DataFrame({'words': totalvocab_tokenized}, index=totalvocab_stemmed)
    print('there are ' + str(vocab_frame.shape[0]) + ' items in vocab_frame')
    print(vocab_frame.head())
    
    # TF - IDF Generation
    # define vectorizer parameters
    tfidf_vectorizer = TfidfVectorizer(max_df=0.8, max_features=200000,
                                       min_df=0.005, stop_words='english',
                                       use_idf=True, tokenizer=tokenize_and_stem, ngram_range=(1, 2))

    tfidf_matrix = tfidf_vectorizer.fit_transform(documents)  # Fit the vectorizer to documents
    # print(tfidf_matrix.shape)
    
    terms = tfidf_vectorizer.get_feature_names()
    # print(terms)
    
    dist = 1 - cosine_similarity(tfidf_matrix)
    
    # Clustering
    num_clusters = 20
    km = KMeans(n_clusters=num_clusters)
    km.fit(tfidf_matrix)
    clusters = km.labels_.tolist()
    
    print("Top terms per cluster:")
    order_centroids = km.cluster_centers_.argsort()[:, ::-1]
    
    for i in range(num_clusters):
        print("Cluster %d words:" % i, end='')
        for ind in order_centroids[i, :6]:  # Replace 6 with n words per cluster
            print('%s' % vocab_frame.ix[terms[ind].split(' ')].values.tolist()[0][0], end=', ')
        print('\n')



















    


