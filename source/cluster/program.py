import string
import collections
from configparser import ConfigParser
from graph.graph import Graph
from nltk import word_tokenize
from nltk import FreqDist
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
import os


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
    config = ConfigParser()
    config.read(os.path.expanduser('~/.config/networkt/cluster.ini'))
    DATABASE_NAME = 'sqlite:///{}/data_store.db'.format(config.get('persistence-configuration', 'database_path'))
    
    graph = Graph(DATABASE_NAME)
    statuses = graph.load_statuses()
    articles = []
    count = 0
    for status in statuses:
        count = count + 1
        articles.append(status.text)
    print(count)

    # articles = ['article about stuff',
    #             'another cool article',
    #             'this is what articles are made of',
    #             'another cool article',
    #             'another cool article lol']

    # clusters = cluster_texts(articles, 20)
    # clusteri = dict(clusters)
    
    # for key in clusteri:
    #     print('Key: ', key)
    #     key_articles_index = list(clusteri[key])
        
    #     cluster_data = ''
    #     for index in key_articles_index:
    #         cluster_data += articles[index]
        
    #     # Only Non Stop Words
    #     stop_words = set(stopwords.words('english'))
    #     cluster_data = [word for word in cluster_data if word not in stop_words]
        
    #     freq = FreqDist(cluster_data)
    #     print(list(freq.items())[:10])


