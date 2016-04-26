"""a directed graph example."""

from sqlalchemy import Column, ForeignKey, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker


Base = declarative_base()


class Node(Base):
    __tablename__ = 'node'
    node_id = Column(Integer, primary_key=True)

    def __init__(self, id):
        self.node_id = id

    def add_edge(self, *nodes):
        for node in nodes:
            Edge(self, node)
        return self

    def pointer_neighbors(self):
        return [x.pointer_node for x in self.root_edges]

    def root_neighbors(self):
        return [x.root_node for x in self.pointer_edges]


class Edge(Base):
    __tablename__ = 'edge'

    root_id = Column(Integer,
                     ForeignKey('node.node_id'),
                     primary_key=True)

    pointer_id = Column(Integer,
                        ForeignKey('node.node_id'),
                        primary_key=True)

    root_node = relationship(Node,
                             primaryjoin=root_id == Node.node_id,
                             backref='root_edges')
    pointer_node = relationship(Node,
                                primaryjoin=pointer_id == Node.node_id,
                                backref='pointer_edges')

    # here we have root.node_id <= pointer.node_id
    def __init__(self, n1, n2):
        self.root_node = n1
        self.pointer_node = n2


engine = create_engine('sqlite:///data.db', echo=True)
Base.metadata.create_all(engine)

session = sessionmaker(engine)()


n1 = Node(1)
n2 = Node(2)
n3 = Node(3)
n4 = Node(4)

n1.add_edge(n2)
n2.add_edge(n1)

session.add_all([n1, n2, n3, n4])
session.commit()
