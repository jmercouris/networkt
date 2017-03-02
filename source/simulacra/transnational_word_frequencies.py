"""
+ TE Tweet Word Frequencies (Stopwords removed, Wordcloud rendering)

  Only tweets of each transnational
"""
import configparser
from graph.data_model import Tag

from neomodel import config


########################################
settings = configparser.ConfigParser()
settings.read('scrapet.ini')
# Database parameters ##################
config.DATABASE_URL = settings.get('database-configuration', 'url')
########################################


# get transnational users
tag = Tag.nodes.get(name=Tag.FILTER_1)

for node in tag.users:
    print('lol')
