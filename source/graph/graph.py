import networkx as nx
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from graph.initialize import Base, Node


class Graph(object):
    """Documentation for Graph

    """
    def __init__(self, DATABASE_NAME, graph_path):
        engine = create_engine(DATABASE_NAME)
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()
        self.graph_path = graph_path
        
    def persist_graph(self, screen_name, file_name):
        graph = self.load_graph_from_database(screen_name)
        nx.write_gml(graph, '{}/{}.gml'.format(self.graph_path, file_name))
    
    def load_graph_from_database(self, screen_name):
        graph = nx.DiGraph()
        root_user_object = self.session.query(Node).filter_by(screen_name=screen_name).first()
        graph = self.traverse(root_user_object, 0, 1, {}, graph)
        return graph
    
    def get_statuses_for_screen_name(self, screen_name):
        element = self.session.query(Node).filter_by(screen_name=screen_name).first()
        return element.statuses
    
    def traverse(self, node, depth, depth_limit, cache, graph):
        cache[node] = None
        if (depth > depth_limit):
            return graph
        graph.add_node(node.screen_name, node.construct_dictionary())
        for reference in node.pointer_nodes():
            graph.add_edge(node.screen_name, reference.screen_name)
            if reference in cache:
                continue
            graph = nx.compose(graph, self.traverse(reference, depth+1, depth_limit, cache, graph))
        
        for reference in node.reference_nodes():
            graph.add_edge(reference.screen_name, node.screen_name)
            if reference in cache:
                continue
            graph = nx.compose(graph, self.traverse(reference, depth+1, depth_limit, cache, graph))
        
        return graph

