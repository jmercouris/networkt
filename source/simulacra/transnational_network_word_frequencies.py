"""
+ Ego Centric Graph Word Frequencies (Stopwords removed, Wordcloud rendering)

  Tweets of all users in a transnational's network
"""
import configparser

from utility.tweet_processing import process
from graph.data_model import Tag
from wordcloud import WordCloud

from neomodel import config
import matplotlib.pyplot as plt
from nltk import FreqDist
import csv


########################################
settings = configparser.ConfigParser()
settings.read('scrapet.ini')
# Database parameters ##################
config.DATABASE_URL = settings.get('database-configuration', 'url')
########################################


# get transnational users
tag = Tag.nodes.get(name=Tag.FILTER_1)

for node in tag.users:
    text = []
    
    for status in node.statuses:
        text += process(status.text)
    
    string_text = ' '.join(text)
    
    # create word cloud
    if text:
        # lower max_font_size
        wordcloud = WordCloud(width=2000, height=2000).generate(string_text)
        plt.figure(figsize=(20, 20), facecolor='k')
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.savefig('{}_word_cloud.png'.format(node.screen_name))
        
        # create frequency statistics
        fdist = FreqDist(text)
        with open('usr_{}_freq_distribution.csv'.format(node.screen_name), 'w', newline='') as f:
            writer = csv.writer(f)
            for key in fdist.keys():
                writer.writerow([key, fdist[key]])
