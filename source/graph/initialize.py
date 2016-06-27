""" INITIALIZE the database tables, columns, etc
"""
from datetime import datetime
from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer, Text,
                        create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
import configparser

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
    filter_2 = Column(Boolean)
    # Relationship to Status Updates
    statuses = relationship("Status", order_by="Status.date",
                            backref="node", cascade="all, delete")

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
        return {'createdat': str(self.created_at),
                'description': str(self.description),
                'favoritescount': int(self.favorites_count),
                'followerscount': int(self.followers_count),
                'friendscount': int(self.friends_count),
                'idstr': str(self.id_str),
                'lang': str(self.lang),
                'listedcount': int(self.listed_count),
                'location': str(self.location),
                'name': str(self.name),
                'screenname': str(self.screen_name),
                'statusescount': int(self.statuses_count),
                'timezone': str(self.time_zone),
                'utcoffset': int(self.utc_offset),
                'verified': bool(self.verified), }


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


class Status(Base):
    __tablename__ = 'status'
    id = Column(Integer, primary_key=True)
    # Parent
    node_id = Column(Integer, ForeignKey('node.id'))
    # Fields
    coordinate_longitude = Column(Text)
    coordinate_latitude = Column(Text)
    created_at = Column(Text)
    date = Column(DateTime)
    favorite_count = Column(Integer)
    id_str = Column(Text)
    in_reply_to_screen_name = Column(Text)
    in_reply_to_status_id_str = Column(Text)
    in_reply_to_user_id_str = Column(Text)
    lang = Column(Text)
    possibly_sensitive = Column(Boolean)
    quoted_status_id_str = Column(Text)
    retweet_count = Column(Integer)
    retweeted = Column(Boolean)
    source = Column(Text)
    text = Column(Text)
    truncated = Column(Boolean)
    
    def __init__(self, dictionary):
        if dictionary.get('coordinates', None) is not None:
            coordinate = dictionary.get('coordinates', None)
            sub_coordinate = coordinate.get('coordinates', None)
            self.coordinate_longitude = sub_coordinate[0]
            self.coordinate_latitude = sub_coordinate[1]
        self.created_at = dictionary.get('created_at', None)
        self.favorite_count = int(dictionary.get('favorite_count') or -1)
        self.id_str = dictionary.get('id_str', None)
        self.in_reply_to_screen_name = dictionary.get('in_reply_to_screen_name', None)
        self.in_reply_to_status_id_str = dictionary.get('in_reply_to_status_id_str', None)
        self.in_reply_to_user_id_str = dictionary.get('in_reply_to_user_id_str', None)
        self.lang = dictionary.get('lang', None)
        self.possibly_sensitive = bool(dictionary.get('possibly_sensitive', False) or False)
        self.quoted_status_id_str = dictionary.get('quoted_status_id_str', None)
        self.retweet_count = int(dictionary.get('retweet_count') or -1)
        self.retweeted = bool(dictionary.get('retweeted', False) or False)
        self.source = dictionary.get('source', None)
        self.text = dictionary.get('text', None)
        self.truncated = bool(dictionary.get('truncated', False) or False)
        self.id = int(self.id_str)
        self.date = datetime.strptime(self.created_at, '%a %b %d %H:%M:%S +0000 %Y')
    
    def __lt__(self, other):
        return self.date.timestamp() < other.date.timestamp()
    
    def __gt__(self, other):
        return self.date.timestamp() > other.date.timestamp()
    
    def __eq__(self, other):
        return self.date.timestamp() == other.date.timestamp()
    
    def __le__(self, other):
        return self.date.timestamp() <= other.date.timestamp()
    
    def __ge__(self, other):
        return self.date.timestamp() >= other.date.timestamp()
    
    def __ne__(self, other):
        return self.date.timestamp() != other.date.timestamp()


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


def create_database_session(database_name='sqlite:///data/data_store.db'):
    settings = configparser.ConfigParser()
    settings.read('configuration.ini')
    DATABASE_NAME = settings.get('database-configuration', 'database_name')
    
    engine = create_engine(DATABASE_NAME)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session


if __name__ == "__main__":
    create_database()
