from configparser import ConfigParser
from graph.graph import Graph
import os

import string
import collections
from nltk import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from pprint import pprint


def process_text(text, stem=True):
    """ Tokenize text and stem words removing punctuation """
    transtable = {ord(s): None for s in string.punctuation}
    transtable[ord('/')] = u''
    text = text.translate(transtable)
    tokens = word_tokenize(text)
    
    if stem:
        stemmer = PorterStemmer()
        tokens = [stemmer.stem(t) for t in tokens]
        
    return tokens


def cluster_texts(texts, clusters=3):
    """ Transform texts to Tf-Idf coordinates and cluster texts using K-Means """
    vectorizer = TfidfVectorizer(tokenizer=process_text,
                                 stop_words=stopwords.words('english'),
                                 max_df=0.5,
                                 min_df=0.1,
                                 lowercase=True)
 
    tfidf_model = vectorizer.fit_transform(texts)
    km_model = KMeans(n_clusters=clusters)
    km_model.fit(tfidf_model)
 
    clustering = collections.defaultdict(list)
 
    for idx, label in enumerate(km_model.labels_):
        clustering[label].append(idx)
 
    return clustering
 
 
if __name__ == "__main__":
    # config = ConfigParser()
    # config.read(os.path.expanduser('~/.config/networkt/cluster.ini'))
    # DATABASE_NAME = 'sqlite:///{}/data_store.db'.format(config.get('persistence-configuration', 'database_path'))
    
    # graph = Graph(DATABASE_NAME)
    # statuses = graph.load_statuses()
    # articles = []
    # count = 0
    # for status in statuses:
    #     articles.append(status.text)

    articles = ['article about stuff',
                'another cool article',
                'this is what articles are made of',
                'another cool article',
                'article about stuff',
                'another cool article',
                'this is what articles are made of',
                'another cool article lol']

    clusters = cluster_texts(articles, 4)
    clusteri = dict(clusters)
    for key in clusteri:
        print('idx {} cmp {}'.format(key, len(clusteri[key])))
    pprint(clusteri)

