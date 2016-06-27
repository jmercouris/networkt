from configparser import ConfigParser
from graph.graph import Graph
import os
import re
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

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
    
    for status in statuses:
        tmp_text = status.text
        # Strip URLs
        tmp_text = re.sub(r"http\S+", "", tmp_text)
        # Strip the word Retweet
        tmp_text = re.sub(r"(?i)rt", "", tmp_text)
        # Strip @Username Mentions
        tmp_text = re.sub(r'@([A-Za-z0-9_]+)', "", tmp_text)
        documents.append(tmp_text)
    
    print('Documents: {}'.format(len(documents)))
    
    # # Use extend so it's a big flat list of vocab
    # totalvocab_stemmed = []
    # totalvocab_tokenized = []
    # for i in documents:
    #     allwords_stemmed = tokenize_and_stem(i)  # for each item in 'documents', tokenize/stem
    #     totalvocab_stemmed.extend(allwords_stemmed)  # extend the 'totalvocab_stemmed' list
    #     allwords_tokenized = tokenize_only(i)
    #     totalvocab_tokenized.extend(allwords_tokenized)
    
    # vocab_frame = pd.DataFrame({'words': totalvocab_tokenized}, index=totalvocab_stemmed)
    # print('there are ' + str(vocab_frame.shape[0]) + ' items in vocab_frame')
    
    # TF - IDF Generation
    # Define vectorizer parameters
    tfidf_vectorizer = TfidfVectorizer(max_df=0.75, max_features=500000,
                                       min_df=0.0, stop_words='english',
                                       use_idf=True, tokenizer=tokenize_and_stem, ngram_range=(1, 3))
    tfidf_matrix = tfidf_vectorizer.fit_transform(documents)  # Fit the vectorizer to documents
    print('TF IDF Matrix Generated')
    
    terms = tfidf_vectorizer.get_feature_names()
    print('Terms: {}'.format(len(terms)))
    
    # Clustering
    num_clusters = 50
    km = KMeans(n_clusters=num_clusters)
    print('Clusters Defined')
    km.fit(tfidf_matrix)
    print('Clusters Fitted')
    clusters = km.labels_.tolist()

    # print("Top terms per cluster:")
    # order_centroids = km.cluster_centers_.argsort()[:, ::-1]
        
    # for i in range(num_clusters):
    #     print("Cluster %d words:" % i, end='')
    #     for ind in order_centroids[i, :6]:  # Replace 6 with n words per cluster
    #         print('%s' % vocab_frame.ix[terms[ind].split(' ')].values.tolist()[0][0], end=', ')
    #     print('\n')
        
    # Print Clusters and Groups
    for i in range(num_clusters):
        cluster_print_limit = 15
        print("\nCluster {}\n".format(i))
        for idx, value in enumerate(clusters):
            if (value == i):
                cluster_print_limit = cluster_print_limit - 1
                if (not cluster_print_limit):
                    break
                print(documents[idx])



















    


