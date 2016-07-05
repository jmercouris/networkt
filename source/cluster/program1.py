import os
import string
import collections

from configparser import ConfigParser
from nltk import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from graph.initialize import Base, Node


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
                                 min_df=0.0,
                                 lowercase=True)
 
    tfidf_model = vectorizer.fit_transform(texts)
    km_model = KMeans(n_clusters=clusters)
    km_model.fit(tfidf_model)
 
    clustering = collections.defaultdict(list)
 
    for idx, label in enumerate(km_model.labels_):
        clustering[label].append(idx)
 
    return clustering


def create_session():
    config = ConfigParser()
    config.read(os.path.expanduser('~/.config/networkt/cluster.ini'))
    DATABASE_NAME = 'sqlite:///{}/data_store.db'.format(config.get('persistence-configuration', 'database_path'))
    engine = create_engine(DATABASE_NAME)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session


if __name__ == "__main__":
    session = create_session()
    transnational_users = session.query(Node).filter_by(filter_1=True).all()
    for user in transnational_users[0:1]:
        print(user.screen_name)
        statuses = []
        statuses = statuses + user.statuses
        for node in user.reference_nodes():
            statuses = statuses + node.statuses
        for node in user.pointer_nodes():
            statuses = statuses + node.statuses
        
        statuses.sort()
        documents = [i.text for i in statuses]
        cluster_count = 100
        clusters = cluster_texts(documents, cluster_count)
        clusteri = dict(clusters)
        for key in clusteri:
            print('idx {} cnt {}'.format(key, len(clusteri[key])))
        
        # Assign Cluster and Corresponding Values
        for key in clusteri:
            for idx in clusteri[key]:
                statuses[idx].cluster = key
        
        # Iterate through Transnational Tweets
        for index, status in enumerate(statuses):
            # Transnational Tweet - Check for Diffusion
            if (status.node == user):
                statuses_before = statuses[index - 10:index]
                statuses_after = statuses[index:index + 10]
                
                # Filter Before for Friend Relationships
                statuses_before_filtered = []
                for statusi in statuses_before:
                    if statusi.node in user.reference_nodes():
                        statuses_before_filtered.append(statusi)
                statuses_before = statuses_before_filtered
                
                # Filter After for Follower Relationships
                statuses_after_filtered = []
                for statusi in statuses_after:
                    if statusi.node in user.pointer_nodes():
                        statuses_after_filtered.append(statusi)
                statuses_after = statuses_after_filtered
                
                statuses_before = [i for i in statuses_before if i.cluster == status.cluster]
                statuses_after = [i for i in statuses_after if i.cluster == status.cluster]
                
                # If Statuses of same cluster exist before and after print them
                if (len(statuses_before) > 0 and len(statuses_after) > 0):
                    print('=' * 80)
                    
                    print('friend statuses before tweet')
                    print('-' * 80)
                    for text in [i.text for i in statuses_before]:
                        print(text)
                    
                    print('\ntransnational status')
                    print('-' * 80)
                    print(status.text)
                    
                    print('\nfollower statuses after tweet')
                    print('-' * 80)
                    for text in [i.text for i in statuses_after]:
                        print(text)
                    
                    print('\n')
