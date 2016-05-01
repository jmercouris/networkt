import configparser
import networkx as nx
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from initialize import Base, Node


settings = configparser.ConfigParser()
settings.read('configuration.ini')

DATABASE_NAME = settings.get('database-configuration', 'database_name')

engine = create_engine(DATABASE_NAME)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# Main Function
def main(root_user='FactoryBerlin'):
    persist_graph(root_user, root_user)


def persist_graph(screen_name, file_name):
    root_user_object = session.query(Node).filter_by(screen_name=screen_name).first()

    graph = nx.Graph()
    # graph.add_node(root_user_object)

    # for node in root_user_object.reference_nodes():
    #     graph.add_node(node)
    #     graph.add_edge(node, root_user_object)

    graph.add_nodes_from([2, 3])
    graph.add_edge(2, 3)

    nx.write_gml(graph, 'data/graph/' + file_name + '.gml')


if __name__ == "__main__":
    main()
