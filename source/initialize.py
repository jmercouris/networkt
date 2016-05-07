""" Initialize the database tables, columns, etc
"""
from sqlalchemy import (Boolean, Column, ForeignKey,
                        Integer, Text, create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class Node(Base):
    __tablename__ = 'node'
    id = Column(Integer, primary_key=True)
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
    # Filtering Levels
    filter_0 = Column(Boolean)
    filter_1 = Column(Boolean)

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
        self.id = int(self.id_str)

    def add_edge(self, *nodes):
        for node in nodes:
            Edge(self, node)
        return self

    def add_edge_reference(self, *nodes):
        for node in nodes:
            Edge(node, self)
        return self

    def pointer_nodes(self):
        return [i.pointer_node for i in self.reference_edges]

    def reference_nodes(self):
        return [i.reference_node for i in self.pointer_edges]

    def __str__(self):
        return self.id_str

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return self.id_str == other.id_str

    def construct_dictionary(self):
        return {'screenname': str(self.screen_name),
                'timezone': str(self.time_zone)}


class Edge(Base):
    __tablename__ = 'edge'

    reference_id = Column(Integer,
                          ForeignKey('node.id'),
                          primary_key=True)

    pointer_id = Column(Integer,
                        ForeignKey('node.id'),
                        primary_key=True)

    reference_node = relationship(Node,
                                  primaryjoin=reference_id == Node.id,
                                  backref='reference_edges')
    pointer_node = relationship(Node,
                                primaryjoin=pointer_id == Node.id,
                                backref='pointer_edges')

    def __init__(self, n1, n2):
        self.reference_node = n1
        self.pointer_node = n2


def edge_point(n1, n2):
    try:
        return Edge(n1, n2)
    except:
        pass


def edge_reference(n1, n2):
    try:
        return Edge(n2, n1)
    except:
        pass


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
