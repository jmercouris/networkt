""" Initialize the database tables, columns, etc
"""
from sqlalchemy import Column, Text, Boolean, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapper, relationship, sessionmaker
from sqlalchemy import MetaData, Table, Column, Integer, ForeignKey, create_engine


Base = declarative_base()


class Node(Base):
    __tablename__ = 'node'
    id = Column(Integer, primary_key=True)
    node_id = Column(Integer, primary_key=True)
    created_at = Column(Text)
    description = Column(Text)
    favorites_count = Column(Integer)
    followers_count = Column(Integer)
    friends_count = Column(Integer)
    id_str = Column(Text)
    lang = Column(Text)
    listed_count = Column(Integer)
    location = Column(Text)
    name = Column(Text)
    screen_name = Column(Text)
    statuses_count = Column(Integer)
    time_zone = Column(Text)
    utc_offset = Column(Integer)
    verified = Column(Boolean)

    def __init__(self, dictionary):
        self.created_at = dictionary.get('created_at', None)
        self.description = dictionary.get('description', None)
        self.favorites_count = int(dictionary.get('favourites_count') or -1)
        self.followers_count = int(dictionary.get('followers_count') or -1)
        self.friends_count = int(dictionary.get('friends_count') or -1)
        self.id_str = dictionary.get('id_str', None)
        self.lang = dictionary.get('lang', None)
        self.listed_count = int(dictionary.get('listed_count') or -1)
        self.location = dictionary.get('location', None)
        self.name = dictionary.get('name', None)
        self.screen_name = dictionary.get('screen_name', None)
        self.statuses_count = int(dictionary.get('statuses_count') or -1)
        self.time_zone = dictionary.get('time_zone', None)
        self.utc_offset = int(dictionary.get('utc_offset') or -1)
        self.verified = bool(dictionary.get('verified', False) or False)
        self.node_id = int(self.id_str)

    def add_neighbors(self, *nodes):
        for node in nodes:
            Edge(self, node)
        return self

    def higher_neighbors(self):
        return [x.higher_node for x in self.lower_edges]

    def lower_neighbors(self):
        return [x.lower_node for x in self.higher_edges]


class Edge(Base):
    __tablename__ = 'edge'

    lower_id = Column(Integer,
                      ForeignKey('node.node_id'),
                      primary_key=True)

    higher_id = Column(Integer,
                       ForeignKey('node.node_id'),
                       primary_key=True)

    lower_node = relationship(Node,
                              primaryjoin=lower_id == Node.node_id,
                              backref='lower_edges')
    higher_node = relationship(Node,
                               primaryjoin=higher_id == Node.node_id,
                               backref='higher_edges')

    # here we have lower.node_id <= higher.node_id
    def __init__(self, n1, n2):
        if n1.node_id < n2.node_id:
            self.lower_node = n1
            self.higher_node = n2
        else:
            self.lower_node = n2
            self.higher_node = n1


def create_database(database_name='sqlite:///data/data_store.db'):
    # Create an engine that stores data in the local directory's
    # 'sqlite:///data/data_store.db' file.
    engine = create_engine(database_name)

    # Create all tables in the engine. This is equivalent to "Create Table"
    # statements in raw SQL.
    Base.metadata.create_all(engine)
    print('Database {} Initialized'.format(database_name))


if __name__ == "__main__":
    create_database()
