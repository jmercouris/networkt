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
def main(root_user='jmercouris'):
    persist_graph(root_user, root_user)


def persist_graph(screen_name, file_name):
    # graph = load_graph_from_database(screen_name)
    graph = nx.DiGraph()
    root_user_object = session.query(Node).filter_by(screen_name=screen_name).first()
    graph = traverse(root_user_object, 0, 10, {}, graph)
    nx.write_gml(graph, 'data/graph/' + file_name + '.gml')


def load_graph_from_database(screen_name):
    root_user_object = session.query(Node).filter_by(screen_name=screen_name).first()
    graph = nx.Graph()
    graph.add_node(root_user_object.screen_name, data=root_user_object.construct_dictionary())
    
    for node in root_user_object.reference_nodes():
        graph.add_node(node.screen_name, data=node.construct_dictionary())
        graph.add_edge(node.screen_name, root_user_object.screen_name)
        for nodey in node.reference_nodes():
            graph.add_node(nodey.screen_name, data=nodey.construct_dictionary())
            graph.add_edge(nodey.screen_name, node.screen_name)
        for nodey in node.pointer_nodes():
            graph.add_node(nodey.screen_name, data=node.construct_dictionary())
            graph.add_edge(node.screen_name, nodey.screen_name)

    for node in root_user_object.pointer_nodes():
        graph.add_node(node.screen_name, data=node.construct_dictionary())
        graph.add_edge(root_user_object.screen_name, node.screen_name)
        for nodey in node.reference_nodes():
            graph.add_node(nodey.screen_name, data=nodey.construct_dictionary())
            graph.add_edge(nodey.screen_name, node.screen_name)
        for nodey in node.pointer_nodes():
            graph.add_node(nodey.screen_name, data=node.construct_dictionary())
            graph.add_edge(node.screen_name, nodey.screen_name)
        
    return graph


def traverse(node, depth, depth_limit, cache, graph):
    cache[node] = None
    # print('__'*depth + node.name)
    if (depth > depth_limit):
        return graph
    graph.add_node(node.screen_name, data=node.construct_dictionary())
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
