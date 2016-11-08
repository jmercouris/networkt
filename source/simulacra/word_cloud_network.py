''' Word Frequency of Different Networks
'''

import os
import string
from configparser import ConfigParser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from graph.initialize import Base, Node
from nltk import word_tokenize
from wordcloud import WordCloud

from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer


def process(text):
    tknzr = TweetTokenizer(strip_handles=True, reduce_len=True)
    words = tknzr.tokenize(text)
    filtered_words = [word for word in words if word not in stopwords.words('english')]
    
    return filtered_words


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


def tokenize_text(text):
    """ Tokenize text and remove punctuation """
    transtable = {ord(s): None for s in string.punctuation}
    transtable[ord('/')] = u''
    text = text.translate(transtable)
    tokens = word_tokenize(text)
    
    return tokens


if __name__ == "__main__":
    session = create_session()
    transnational_users = session.query(Node).filter_by(filter_1=True).all()
    config = ConfigParser()
    config.read(os.path.expanduser('~/.config/networkt/cluster.ini'))
    WORD_FREQUENCY_PATH = config.get('persistence-configuration', 'word_statistics_path')
    
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
        
        print('Gathering Documents')
        documents = [' '.join(process(i.text)) for i in statuses]
        text = ' '.join(documents)

        print('Generating Word Cloud')
        wordcloud = WordCloud().generate(text)
    
        # Display the generated image:
        # the matplotlib way:
        import matplotlib.pyplot as plt
        plt.imshow(wordcloud)
        plt.axis("off")
        
        # lower max_font_size
        wordcloud = WordCloud(width=2000, height=2000).generate(text)
        plt.figure(figsize=(20, 20), facecolor='k')
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.savefig('{}/{}_network_cloud.png'.format(WORD_FREQUENCY_PATH, user.screen_name))


