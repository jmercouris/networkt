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
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
from sklearn.manifold import MDS


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
    print('Data Vectorized')

    km_model = KMeans(n_clusters=clusters)
    km_model.fit(tfidf_model)
 
    clustering = collections.defaultdict(list)
    dist = 1 - cosine_similarity(tfidf_model)

    mds = MDS(n_components=2, dissimilarity="precomputed", random_state=1)
    pos = mds.fit_transform(dist)  # shape (n_components, n_samples)
    xs, ys = pos[:, 0], pos[:, 1]
    
    plt.plot(xs, ys, 'go')
    
    plt.show()
 
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
    print('Using Database: {}'.format(DATABASE_NAME))
    return session


if __name__ == "__main__":
    session = create_session()
    transnational_users = session.query(Node).filter_by(filter_1=True).all()
    for user in transnational_users[0:1]:
        print('User ', user.screen_name)
        statuses = []
        statuses = statuses + user.statuses
        for node in user.reference_nodes()[0:1]:
            statuses = statuses + node.statuses
        for node in user.pointer_nodes()[0:1]:
            statuses = statuses + node.statuses
        
        statuses.sort()
        documents = [i.text for i in statuses]
        print('Documents Gathered')
        cluster_count = 20
        clusters = cluster_texts(documents, cluster_count)
        
        print('Execution Complete')

