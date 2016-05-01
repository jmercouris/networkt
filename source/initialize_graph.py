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

    def pointer_nodes(self):
        return [x.pointer_node for x in self.reference_edges]

    def reference_nodes(self):
        return [x.reference_node for x in self.pointer_edges]


class Edge(Base):
    __tablename__ = 'edge'

    reference_id = Column(Integer,
                          ForeignKey('node.node_id'),
                          primary_key=True)

    pointer_id = Column(Integer,
                        ForeignKey('node.node_id'),
                        primary_key=True)

    reference_node = relationship(Node,
                                  primaryjoin=reference_id == Node.node_id,
                                  backref='reference_edges')
    pointer_node = relationship(Node,
                                primaryjoin=pointer_id == Node.node_id,
                                backref='pointer_edges')

    def __init__(self, n1, n2):
        self.reference_node = n1
        self.pointer_node = n2


engine = create_engine('sqlite:///data.db', echo=True)
Base.metadata.create_all(engine)

session = sessionmaker(engine)()


n1 = Node(1)
n2 = Node(2)
n3 = Node(3)
n4 = Node(4)

n1.add_edge(n2)
n1.add_edge(n3)

n2.add_edge(n1)
n4.add_edge(n1)

for x in n1.pointer_nodes():
    print(x.node_id)


# session.add_all([n1, n2, n3, n4])
# session.commit()
