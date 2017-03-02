"""
+ TE Tweet Word Frequencies (Stopwords removed, Wordcloud rendering)

  Only tweets of each transnational
"""
import configparser
import re

from graph.data_model import Tag
from wordcloud import WordCloud

from neomodel import config
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
import matplotlib.pyplot as plt


########################################
settings = configparser.ConfigParser()
settings.read('scrapet.ini')
# Database parameters ##################
config.DATABASE_URL = settings.get('database-configuration', 'url')
########################################


def process(text):
    # remove urls
    text = re.sub(r"http\S+", "", text)
    
    # attempt to remove twitter artifacts
    text = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", text).split())
    
    # Strip RT
    text = text.replace('RT', '')
    
    tknzr = TweetTokenizer(strip_handles=True, reduce_len=True)
    words = tknzr.tokenize(text)
    
    # remove stopwords
    filtered_english_words = [word for word in words
                              if word not in stopwords.words('english')]
    filtered_german_words = [word for word in filtered_english_words
                             if word not in stopwords.words('german')]
    
    return ' '.join(filtered_german_words)


# get transnational users
tag = Tag.nodes.get(name=Tag.FILTER_1)

for node in tag.users:
    text = ''
    
    for status in node.statuses:
        text += process(status.text)
    
    if text:
        # lower max_font_size
        wordcloud = WordCloud(width=2000, height=2000).generate(text)
        plt.figure(figsize=(20, 20), facecolor='k')
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.savefig('{}_word_cloud.png'.format(node.screen_name))
