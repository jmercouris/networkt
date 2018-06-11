"""DB Scan Clustering and Persistence
https://github.com/scikit-learn/scikit-learn/blob/master/examples/text/document_clustering.py
"""

import csv
import string
from collections import defaultdict

from graph.data_model import Tag

from neomodel import db
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from scipy.stats import skew, kurtosis
from sklearn.cluster import DBSCAN
from sklearn.feature_extraction.text import TfidfVectorizer


def main():
    tag = Tag.nodes.get(name=Tag.FILTER_1)
    with open('results.csv', 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for node in tag.users:
            print('processing {}'.format(node.screen_name))
            diffusion_count = get_transnational_diffusion_count(node)
            time_zone_histogram_data = get_time_zone_histogram_data(node)
            time_zone_kurtosis = kurtosis(time_zone_histogram_data)
            writer.writerow([node.screen_name, diffusion_count, time_zone_kurtosis])


def get_time_zone_histogram_data(node):
    time_zones = ([node.time_zone for node in node.followers] +
                  [node.time_zone for node in node.friends])
    
    time_zone_dictionary = defaultdict(int)
    
    for time_zone in time_zones:
        time_zone_dictionary[time_zone] = time_zone_dictionary[time_zone] + 1
    
    time_zone_histogram_data = []
    
    for time_zone, count in time_zone_dictionary.items():
        time_zone_histogram_data.append(count)
    
    return time_zone_histogram_data


def process_text(text, stem=False):
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
                                 min_df=0.0,
                                 max_df=0.80,
                                 lowercase=True)
    
    # Data Vectorizing
    tfidf_model = vectorizer.fit_transform(documents)
    
    # Data Clustering
    db = DBSCAN(eps=1.25, min_samples=3).fit(tfidf_model)
    
    return db.labels_


def get_transnational_diffusion_count(node):
    diffusion_instances = 0
    
    # get tweets of transnational user
    query = (
        ' MATCH (user:Node {{screen_name:"{}"}})'.format(node.screen_name) +
        ' MATCH (user)-[:STATUS]->(statuses)'
        ' RETURN statuses.text, statuses.date, user.screen_name')
    
    statuses, meta = db.cypher_query(query)
    
    for index, status in enumerate(statuses):
        print('{}, {}/{}'.format(node.screen_name, index, len(statuses)), end='\r')
        
        # five days in unix time
        time_delta = 60 * 60 * 24 * 5
        
        # collect friend statuses before status
        query = (
            ' MATCH (user:Node {{screen_name:"{name}"}})'
            ' MATCH (user)-[:FRIEND]->(connections)'
            ' MATCH (connections)-[:STATUS]->(statuses)'
            ' MATCH (statuses {{lang:"en"}})'
            ' MATCH (statuses)<-[:STATUS]-(nodes)'
            ' WHERE statuses.date > {min_date} and statuses.date < {max_date}'
            ' RETURN statuses.text, statuses.date, nodes.screen_name'
            ' ORDER BY statuses.date DESC').format(
                name=node.screen_name,
                min_date=status[1] - time_delta,
                max_date=status[1])
        friend_statuses, meta = db.cypher_query(query)
        
        # collect follow statuses posted after status
        query = (
            ' MATCH (user:Node {{screen_name:"{name}"}})'
            ' MATCH (user)-[:FOLLOWER]->(connections)'
            ' MATCH (connections)-[:STATUS]->(statuses)'
            ' MATCH (statuses {{lang:"en"}})'
            ' MATCH (statuses)<-[:STATUS]-(nodes)'
            ' WHERE statuses.date > {min_date} and statuses.date < {max_date}'
            ' RETURN statuses.text, statuses.date, nodes.screen_name'
            ' ORDER BY statuses.date DESC').format(
                name=node.screen_name,
                min_date=status[1],
                max_date=status[1] + time_delta)
        follower_statuses, meta = db.cypher_query(query)
        
        if(friend_statuses and follower_statuses):
            # cluster and identify diffusion
            if identify_transnational_diffusion(node, len(friend_statuses),
                                                friend_statuses + [status] + follower_statuses,
                                                output=False):
                diffusion_instances += 1
    print('{} diffusion instances: {}'.format(node.screen_name, diffusion_instances))
    return diffusion_instances


def identify_transnational_diffusion(user, user_index, all_statuses, output=False):
    # extract document from every status and cluster
    clusters = cluster_documents([status[0] for status in all_statuses])
    
    # add cluster id to every document
    results = [l + [r] for l, r in zip(all_statuses, clusters)]
    
    # if user status is not related to any other statuses, return
    if results[user_index][3] == -1:
        return
    
    # gather statuses with same clustering before
    before_statuses = [result for result in results[:user_index]
                       if result[3] == results[user_index][3]]
    
    # gather statuses with same clustering after
    after_statuses = [result for result in results[user_index + 1:]
                      if result[3] == results[user_index][3]]
    
    if before_statuses and after_statuses and output:
        print('=' * 40)
        print('-' * 20, 'before')
        print(before_statuses)
        print('-' * 20, 'status')
        print(results[user_index])
        print('-' * 20, 'after')
        print(after_statuses)
    
    if before_statuses and after_statuses:
        return True


if __name__ == "__main__":
    main()
import csv
import string
from collections import defaultdict

from graph.data_model import Tag

from neomodel import db
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from scipy.stats import skew
from sklearn.cluster import DBSCAN
from sklearn.feature_extraction.text import TfidfVectorizer

def main():
    tag = Tag.nodes.get(name=Tag.FILTER_1)
    with open('results.csv', 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for node in tag.users:
            print('processing {}'.format(node.screen_name))
            diffusion_count = get_transnational_diffusion_count(node)
            skew = calculate_skew(node)
            writer.writerow([node.screen_name, diffusion_count, skew])


def calculate_skew(node):
    time_zones = ([node.time_zone for node in node.followers] +
                  [node.time_zone for node in node.friends])
    
    # count via dictionary
    time_zone_dictionary = defaultdict(int)
    
    # count how many members are in each time zone
    for time_zone in time_zones:
        time_zone_dictionary[time_zone] = time_zone_dictionary[time_zone] + 1
    
    time_zone_histogram_data = []
    
    for time_zone, count in time_zone_dictionary.items():
        time_zone_histogram_data.append(count)
    print(time_zone_histogram_data)
    
    return skew(time_zone_histogram_data)


def process_text(text, stem=False):
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
                                 min_df=0.0,
                                 max_df=0.80,
                                 lowercase=True)
    
    # Data Vectorizing
    tfidf_model = vectorizer.fit_transform(documents)
    
    # Data Clustering
    db = DBSCAN(eps=1.25, min_samples=3).fit(tfidf_model)
    
    return db.labels_


def get_transnational_diffusion_count(node):
    diffusion_instances = 0
    
    # get tweets of transnational user
    query = (
        ' MATCH (user:Node {{screen_name:"{}"}})'.format(node.screen_name) +
        ' MATCH (user)-[:STATUS]->(statuses)'
        ' RETURN statuses.text, statuses.date, user.screen_name')
    
    statuses, meta = db.cypher_query(query)
    
    for index, status in enumerate(statuses):
        print('{}, {}/{}'.format(node.screen_name, index, len(statuses)), end='\r')
        
        # five days in unix time
        time_delta = 60 * 60 * 24 * 5
        
        # collect friend statuses before status
        query = (
            ' MATCH (user:Node {{screen_name:"{name}"}})'
            ' MATCH (user)-[:FRIEND]->(connections)'
            ' MATCH (connections)-[:STATUS]->(statuses)'
            ' MATCH (statuses {{lang:"en"}})'
            ' MATCH (statuses)<-[:STATUS]-(nodes)'
            ' WHERE statuses.date > {min_date} and statuses.date < {max_date}'
            ' RETURN statuses.text, statuses.date, nodes.screen_name'
            ' ORDER BY statuses.date DESC').format(
                name=node.screen_name,
                min_date=status[1] - time_delta,
                max_date=status[1])
        friend_statuses, meta = db.cypher_query(query)
        
        # collect follow statuses posted after status
        query = (
            ' MATCH (user:Node {{screen_name:"{name}"}})'
            ' MATCH (user)-[:FOLLOWER]->(connections)'
            ' MATCH (connections)-[:STATUS]->(statuses)'
            ' MATCH (statuses {{lang:"en"}})'
            ' MATCH (statuses)<-[:STATUS]-(nodes)'
            ' WHERE statuses.date > {min_date} and statuses.date < {max_date}'
            ' RETURN statuses.text, statuses.date, nodes.screen_name'
            ' ORDER BY statuses.date DESC').format(
                name=node.screen_name,
                min_date=status[1],
                max_date=status[1] + time_delta)
        follower_statuses, meta = db.cypher_query(query)
        
        if(friend_statuses and follower_statuses):
            # cluster and identify diffusion
            if identify_transnational_diffusion(node, len(friend_statuses),
                                                friend_statuses + [status] + follower_statuses,
                                                output=False):
                diffusion_instances += 1
    print('{} diffusion instances: {}'.format(node.screen_name, diffusion_instances))
    return diffusion_instances


def identify_transnational_diffusion(user, user_index, all_statuses, output=False):
    # extract document from every status and cluster
    clusters = cluster_documents([status[0] for status in all_statuses])
    
    # add cluster id to every document
    results = [l + [r] for l, r in zip(all_statuses, clusters)]
    
    # if user status is not related to any other statuses, return
    if results[user_index][3] == -1:
        return
    
    # gather statuses with same clustering before
    before_statuses = [result for result in results[:user_index]
                       if result[3] == results[user_index][3]]
    
    # gather statuses with same clustering after
    after_statuses = [result for result in results[user_index + 1:]
                      if result[3] == results[user_index][3]]
    
    if before_statuses and after_statuses and output:
        print('=' * 40)
        print('-' * 20, 'before')
        print(before_statuses)
        print('-' * 20, 'status')
        print(results[user_index])
        print('-' * 20, 'after')
        print(after_statuses)
    
    if before_statuses and after_statuses:
        return True


if __name__ == "__main__":
    main()
