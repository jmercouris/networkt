import networkx as nx
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from graph.initialize import Base, Node


class Graph(object):
    """Documentation for Graph

    """
    def __init__(self, DATABASE_NAME):
        engine = create_engine(DATABASE_NAME)
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()
    
    def get_statuses_for_screen_name(self, screen_name):
        element = self.session.query(Node).filter_by(screen_name=screen_name).first()
        return element.statuses
    
    def persist_graph(self, screen_name, graph_path, file_name):
        graph = self.load_graph_from_database(screen_name)
        nx.write_gml(graph, '{}/{}.gml'.format(graph_path, file_name))
    
    def load_graph_from_database(self, screen_name, depth_limit=0):
        graph = nx.DiGraph()
        root_user_object = self.session.query(Node).filter_by(screen_name=screen_name).first()
        graph = self.traverse(root_user_object, 0, depth_limit, {}, graph)
        return graph
    
    def traverse(self, node, depth, depth_limit, cache, graph):
        cache[node] = None
        if (depth > depth_limit):
            return graph
        graph.add_node(node.screen_name, node.construct_dictionary())
        for reference in node.pointer_nodes():
            graph.add_node(reference.screen_name, reference.construct_dictionary())
            graph.add_edge(node.screen_name, reference.screen_name)
            if reference in cache:
                continue
            graph = nx.compose(graph, self.traverse(reference, depth+1, depth_limit, cache, graph))
        
        for reference in node.reference_nodes():
            graph.add_node(reference.screen_name, reference.construct_dictionary())
            graph.add_edge(reference.screen_name, node.screen_name)
            if reference in cache:
                continue
            graph = nx.compose(graph, self.traverse(reference, depth+1, depth_limit, cache, graph))
        
        return graph

