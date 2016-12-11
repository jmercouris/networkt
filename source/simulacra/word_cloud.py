'''Word Cloud for All Tweets in a network
'''

import os

from configparser import ConfigParser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from graph.initialize import Base, Node


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
        print('User ', user.screen_name)
        statuses = []
        statuses = statuses + user.statuses
        
        for node in user.reference_nodes()[0:10]:
            statuses = statuses + node.statuses
        print('Reference Nodes Complete')
        
        for node in user.pointer_nodes()[0:10]:
            statuses = statuses + node.statuses
        print('Pointer Nodes Complete')
        
        documents = [i.text for i in statuses]
        print('Documents Gathered')
        
        long_document = ' '.join(documents)
