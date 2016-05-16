import configparser
import networkx as nx
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from graph.initialize import Base, Node

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
    graph = load_graph_from_database(screen_name)
    nx.write_gml(graph, 'data/graph/' + file_name + '.gml')


def load_graph_from_database(screen_name):
    graph = nx.DiGraph()
    root_user_object = session.query(Node).filter_by(screen_name=screen_name).first()
    graph = traverse(root_user_object, 0, 1, {}, graph)
    
    return graph


def get_statuses_for_screen_name(screen_name):
    element = session.query(Node).filter_by(screen_name=screen_name).first()
    return element.statuses


def traverse(node, depth, depth_limit, cache, graph):
    cache[node] = None
    if (depth > depth_limit):
        return graph
    graph.add_node(node.screen_name, node.construct_dictionary())
    for reference in node.pointer_nodes():
        graph.add_edge(node.screen_name, reference.screen_name)
        if reference in cache:
            continue
        graph = nx.compose(graph, traverse(reference, depth+1, depth_limit, cache, graph))
    
    for reference in node.reference_nodes():
        graph.add_edge(reference.screen_name, node.screen_name)
        if reference in cache:
            continue
        graph = nx.compose(graph, traverse(reference, depth+1, depth_limit, cache, graph))
    
    return graph


if __name__ == "__main__":
    main()
