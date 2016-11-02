''' Word Frequency of Different Clusters
'''

import os
import string
from configparser import ConfigParser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from graph.initialize import Base, Node
from collections import defaultdict
from nltk import FreqDist
from nltk import word_tokenize


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
        
        # Group by Cluster for Persistence
        groups = defaultdict(list)
        for obj in statuses:
            groups[obj.cluster].append(obj)
        
        with open('{}/{}'.format(WORD_FREQUENCY_PATH, user.screen_name), 'w') as f:
            for key, value in groups.items():
                f.write('Cluster {}\n'.format(key))
                text = ''
                
                for element in value:
                    text += element.text
                
                fdist = FreqDist(tokenize_text(text))
                f.write(str(fdist.most_common(10)) + '\n')
                f.write('_' * 80 + '\n')
        
        print('Execution Complete')

