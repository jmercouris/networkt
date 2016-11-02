''' DB Scan Clustering and Persistence
'''

import os
import string

from configparser import ConfigParser
from nltk import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

from sklearn.feature_extraction.text import TfidfVectorizer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from graph.initialize import Base, Node

from sklearn.cluster import DBSCAN
from collections import defaultdict


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


def cluster_documents(documents):
    """ Transform texts to Tf-Idf coordinates and cluster texts using K-Means """
    vectorizer = TfidfVectorizer(tokenizer=process_text,
                                 stop_words=stopwords.words('english'),
                                 max_df=0.5,
                                 min_df=0.0,
                                 lowercase=True)
    
    print('Data Vectorizing')
    tfidf_model = vectorizer.fit_transform(documents)
    
    print('Data Clustering')
    db = DBSCAN(eps=1.0, min_samples=3, n_jobs=-1).fit(tfidf_model)
    
    return db.labels_


def create_session():
    config = ConfigParser()
    config.read(os.path.expanduser('~/.config/networkt/cluster.ini'))
    DATABASE_NAME = 'sqlite:///{}/data_store.db'.format(config.get('persistence-configuration', 'database_path'))
    engine = create_engine(DATABASE_NAME)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    print('Using Database: {}'.format(DATABASE_NAME))
    return session


if __name__ == "__main__":
    session = create_session()
    transnational_users = session.query(Node).filter_by(filter_1=True).all()
    
    print('Gathering Documents')
    for user in transnational_users:
        print('User ', user.screen_name)
        statuses = []
        statuses = statuses + user.statuses
        
        print('Gathering Friend Statuses')
        for node in user.reference_nodes(limit=10):
            statuses = statuses + node.statuses
        
        print('Gathering Follower Statuses')
        for node in user.pointer_nodes(limit=10):
            statuses = statuses + node.statuses
        
        # Convert Documents into Plain Text
        documents = [i.text for i in statuses]
        
        print('Clustering Documents')
        labels = cluster_documents(documents)
        
        print('Zipping Cluster Labels')
        for label, status in zip(labels, statuses):
            status.cluster = int(label)
        
        # Group by Cluster for Printing
        # groups = defaultdict(list)
        # for obj in statuses:
        #     groups[obj.cluster].append(obj)
        
        # for key, value in groups.items():
        #     print('CLUSTER {}'.format(key))
        #     print('_' * 80)
        #     for element in value:
        #         print(element.text)
        
        session.commit()
        print('_' * 80)
        
        print('Execution Complete')

