"""DB Scan Clustering and Persistence

"""

import os
import string
from bisect import bisect_left, bisect_right
from datetime import timedelta

from configparser import ConfigParser
from nltk import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import DBSCAN
import jellyfish

from graph.data_model import Tag


def process_text(text, stem=True):
    """Tokenize text and stem words removing punctuation
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
    """Transform texts to Tf-Idf coordinates and cluster texts using
    DBSCAN
    
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


def main():
    tag = Tag.nodes.get(name=Tag.FILTER_1)
    for node in tag.users:
        print(node.screen_name)
        """MATCH (connections)-[:STATUS]->(statuses)
        MATCH (statuses {lang:"en"})
        MATCH (statuses)<-[:STATUS]-(nodes)
        RETURN statuses.text, statuses.date, nodes.screen_name
        ORDER BY statuses.date DESC
        LIMIT 100"""


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
            previous_stack = [sts for sts in previous_stack if user in sts.node.pointer_nodes()]
            next_stack = [sts for sts in next_stack if user in sts.node.reference_nodes()]
            
            # Filter Cluster
            previous_stack = [sts for sts in previous_stack if sts.cluster == status.cluster]
            next_stack = [sts for sts in next_stack if sts.cluster == status.cluster]
            
            # Print Output
            if(len(previous_stack) > 0 and len(next_stack) > 0):
                # Average Distance Before / After
                distance = 0
                for sts in previous_stack:
                    distance += jellyfish.jaro_distance(sts.text, status.text)
                previous_average = distance / len(previous_stack)
                
                distance = 0
                comparisons = 0
                for sts in previous_stack:
                    for stsy in next_stack:
                        comparisons += 1
                        distance += jellyfish.jaro_distance(sts.text, stsy.text)
                evolved_average = distance / comparisons
                
                # Print Output
                config = ConfigParser()
                config.read(os.path.expanduser('~/.config/networkt/cluster.ini'))
                path = config.get('persistence-configuration', 'database_path')
                with open('{}/{}'.format(path, user.screen_name), 'a') as f:
                    f.write('Avg.(Friend -> Transnational): {}\n'.format(previous_average))
                    f.write('Avg.(Friend -> Transnational Follower): {}\n'.format(evolved_average))
                    f.write(str([i.text for i in previous_stack]) + '\n')
                    f.write('-' * 40 + '\n')
                    f.write(status.text + '\n')
                    f.write('-' * 40 + '\n')
                    f.write(str([i.text for i in next_stack]) + '\n')
                    f.write('=' * 80 + '\n')

if __name__ == "__main__":
    main()
