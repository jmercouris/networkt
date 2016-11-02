''' Create GML files for Analysis for Users
'''

from graph.graph import Graph
import configparser


def create_graph(database_name, graph_path='', root_user=''):
    graph = Graph(database_name)
    
    ##########################################################################
    # Persist Graphs of all filtered user networks
    print('User Extracted')
    graph.persist_graph(root_user, graph_path, root_user)
    print('Graph Persisted')


if __name__ == "__main__":
    settings = configparser.ConfigParser()
    settings.read('scrapet.ini')
    
    # Network Scrape Parameters
    database_name = 'sqlite:///{}/data_store.db'.format(settings.get('persistence-configuration', 'database_path'))
    graph_path = settings.get('persistence-configuration', 'graph_path')
    root_user = settings.get('scrape-configuration', 'root_user')
    
    # Print Operating Parameters
    print('graph_path {}'.format(graph_path))
    print('root_user {}'.format(root_user))
    
    print('Creating Graph')
    create_graph(database_name, graph_path=graph_path, root_user=root_user)
    print('Graph for user {} created at: {}'.format(root_user, graph_path))
