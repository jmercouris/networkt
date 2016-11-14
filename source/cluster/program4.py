''' DB Scan Clustering and Persistence
'''

import os
import string
from bisect import bisect_left, bisect_right
from datetime import timedelta
from graph.initialize import Status

from configparser import ConfigParser
from nltk import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

from sklearn.feature_extraction.text import TfidfVectorizer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from graph.initialize import Base, Node

from sklearn.cluster import DBSCAN
import numpy as np


def process_text(text, stem=True):
    """ Tokenize text and stem words removing punctuation
    """
    transtable = {ord(s): None for s in string.punctuation}
    transtable[ord('/')] = u''
    text = text.translate(transtable)
    tokens = word_tokenize(text)
    
    if stem:
        stemmer = PorterStemmer()
        tokens = [stemmer.stem(t) for t in tokens]
        
    return tokens


def cluster_documents(documents):
    """ Transform texts to Tf-Idf coordinates and cluster texts using K-Means
    """
    vectorizer = TfidfVectorizer(tokenizer=process_text,
                                 stop_words=stopwords.words('english'),
                                 max_df=0.5,
                                 min_df=0.0,
                                 lowercase=True)
    
    # Data Vectorizing
    tfidf_model = vectorizer.fit_transform(documents)
    
    # Data Clustering
    db = DBSCAN(min_samples=3).fit(tfidf_model)
    
    return db.labels_


def create_session():
    config = ConfigParser()
    config.read(os.path.expanduser('~/.config/networkt/cluster.ini'))
    DATABASE_NAME = 'sqlite:///{}/data_store.db'.format(
        config.get('persistence-configuration', 'database_path'))
    engine = create_engine(DATABASE_NAME)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    print('Using Database: {}'.format(DATABASE_NAME))
    return session


def identify_transnational_diffusion(user, statuses):
    # Remove Non Clustered Tweets
    statuses = [sts for sts in statuses if sts.cluster != -1 and sts.cluster is not None]
    
    for index, status in enumerate(statuses):
        # Transnational Tweet - Check for Diffusion
        if (status.node == user):
            # Gather Tweets from Previous 1 Day
            tmp_status = type('', (), {})  # Create Pseudo Object for Comparison
            tmp_status.date = status.date - timedelta(days=1)
            left_bound = bisect_left(statuses, tmp_status, lo=0, hi=index)
            previous_stack = statuses[left_bound:index]
            
            # Gather Tweets from Next 1 Day
            tmp_status.date = status.date + timedelta(days=1)
            right_bound = bisect_right(statuses, tmp_status, lo=index)
            next_stack = statuses[index:right_bound]
            
            # Filter Type Tweets
            friend_stack = [sts for sts in previous_stack if user in sts.node.pointer_nodes()]
            follower_stack = [sts for sts in next_stack if user in sts.node.reference_nodes()]
            
            # Filter Cluster
            friend_stack = [sts for sts in friend_stack if sts.cluster == status.cluster]
            follower_stack = [sts for sts in follower_stack if sts.cluster == status.cluster]
            
            # Print Output
            if(len(friend_stack) > 0 and len(follower_stack) > 0):
                print([i.text for i in friend_stack])
                print('-' * 40)
                print(status.text)
                print('-' * 40)
                print([i.text for i in follower_stack])
                print('=' * 80)

if __name__ == "__main__":
    session = create_session()
    transnational_users = session.query(Node).filter_by(filter_1=True).all()
    
    for user in transnational_users:
        print('User: {} '.format(user.screen_name))
        print('Friends: {}'.format(user.friends_count))
        print('Followers: {}'.format(user.followers_count))
        statuses = []
        statuses = statuses + user.statuses
        
        for index, edge in enumerate(user.pointer_edges):
            node = edge.reference_node
            statuses = statuses + node.statuses
            print('{} followers gathered (limit 1,000)'.format(index + 1), end='\r')
        print('')
        
        for index, edge in enumerate(user.reference_edges):
            node = edge.pointer_node
            statuses = statuses + node.statuses
            print('{} friends gathered (limit 1,000)'.format(index + 1), end='\r')
        print('')
        
        # Sort Statuses by Date to Cluster in Increments of 10000
        statuses.sort()
        split_statuses = np.array_split(statuses, int(len(statuses) / 10000))
        
        for index, status_group in enumerate(split_statuses):
            print('Cluster Group: {}'.format(index), end='\r')
            documents = [i.text for i in status_group]
            labels = cluster_documents(documents)
            
            print('Zipping Group: {}'.format(index))
            for label, status in zip(labels, status_group):
                status.cluster = int(label)
            
            # Identify Transnational Interactions
            identify_transnational_diffusion(user, status_group)
        
        session.commit()
        print('_' * 80)

'''TODO:
Add prefix to Cluster to Indicate what sub array it was part of
Create Program that generates table of Transnational Interactions
Create Program that calculates distance between tweets to show evolution
Work on Documentation
'''
