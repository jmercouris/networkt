import configparser
from graph.network_scrape import NetworkScrape
from graph.graph import Graph
from graph.initialize import create_database
from math import ceil as ceiling
from scrapet.logger import Logger


def main(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET, DATABASE_NAME, LOGGER,
         root_user='', root_user_follower_limit=200,
         filter_graph_follower_limit=200,
         extended_graph_follower_limit=200,
         name_list_path='', graph_path=''):
    network_scrape = NetworkScrape(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET, DATABASE_NAME)
    graph = Graph(DATABASE_NAME)

    ##########################################################################
    # Create the database
    create_database(DATABASE_NAME)
    
    ##########################################################################
    # Persist the root user
    network_scrape.persist_user(root_user)
    print('Persisted Root User')
    
    ##########################################################################
    # Persist the root user's follower list
    network_scrape.pull_remote_graph_follow(root_user,
                                            scope_limit=ceiling(root_user_follower_limit / 200))
    print('Persisted Root user follower graph')
    
    ##########################################################################
    # Perform degree 0 filtering to decide whether to pull 0th degree network
    network_scrape.filter_0(root_user, location=name_list_path)
    print('Root User: {} follower graph filtered. [Filter level 0]'.format(root_user))
    
    ##########################################################################
    # Pull partial graphs of all filtered users following root user
    root_user_object = network_scrape.get_user_from_data_store(root_user)
    for node in root_user_object.pointer_nodes():
        if (node.filter_0):
            network_scrape.pull_remote_graph_friend(node.screen_name,
                                                    scope_limit=ceiling(filter_graph_follower_limit / 200))
    print('Root User: {} follower graphs extracted.'.format(root_user))
    
    ##########################################################################
    # Perform level 1 filtering on root_user - determine if their 1th degree network
    # is something that should be retrieved
    network_scrape.filter_1(root_user)
    print('Root User: {} follower graphs filtered. [Filter level 1]'.format(root_user))
    
    ##########################################################################
    # Pull extended graphs of all filtered users
    root_user_object = network_scrape.get_user_from_data_store(root_user)
    for root_node in root_user_object.pointer_nodes():
        if (root_node.filter_0 and root_node.filter_1):
            network_scrape.pull_remote_graph_follow(root_node.screen_name,
                                                    scope_limit=ceiling(extended_graph_follower_limit / 200))
            network_scrape.pull_remote_graph_friend(root_node.screen_name,
                                                    scope_limit=ceiling(extended_graph_follower_limit / 200))
    
    ##########################################################################
    # Pull statuses of all filtered user networks
    root_user_object = network_scrape.get_user_from_data_store(root_user)
    for root_node in root_user_object.pointer_nodes():
        if (root_node.filter_0 and root_node.filter_1):
            network_scrape.pull_remote_status(root_node.screen_name)
            for node in root_node.reference_nodes():
                network_scrape.pull_remote_status(node.screen_name)
            for node in root_node.pointer_nodes():
                network_scrape.pull_remote_status(node.screen_name)
    
    ##########################################################################
    # Persist Graphs of all filtered user networks
    root_user_object = network_scrape.get_user_from_data_store(root_user)
    for root_node in root_user_object.pointer_nodes():
        if (root_node.filter_0 and root_node.filter_1):
            graph.persist_graph(root_node.screen_name, graph_path, root_node.screen_name)
    graph.persist_graph(root_user_object.screen_name, graph_path, root_user_object.screen_name)


class LoggerConsole(Logger):
    """Documentation for LoggerConsole
    
    """
    def __init__(self, args):
        super(LoggerConsole, self).__init__()
        self.args = args
        
    def update_progress(self, percent_complete):
        print('percent complete', percent_complete)
    
    # Importance is a number from 0-1
    def log_event(self, importance, text):
        print(importance, text)


if __name__ == "__main__":
    settings = configparser.ConfigParser()
    settings.read('scrapet.ini')
    
    # Network Scrape Parameters
    APP_KEY = settings.get('twython-configuration', 'key')
    APP_SECRET = settings.get('twython-configuration', 'secret')
    OAUTH_TOKEN = settings.get('twython-configuration', 'token')
    OAUTH_TOKEN_SECRET = settings.get('twython-configuration', 'token_secret')
    DATABASE_NAME = 'sqlite:///{}/data_store.db'.format(settings.get('persistence-configuration', 'database_path'))
    graph_path = settings.get('persistence-configuration', 'graph_path')
    # Scrape Specific Configuration Details
    root_user = settings.get('scrape-configuration', 'root_user')
    name_list_path = settings.get('scrape-configuration', 'name_list_path')
    root_user_follower_limit = int(settings.get('scrape-configuration', 'root_user_follower_limit'))
    filter_graph_follower_limit = int(settings.get('scrape-configuration', 'filter_graph_follower_limit'))
    extended_graph_follower_limit = int(settings.get('scrape-configuration', 'extended_graph_follower_limit'))
        
    main(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET, DATABASE_NAME, LoggerConsole(),
         root_user=root_user, root_user_follower_limit=root_user_follower_limit,
         extended_graph_follower_limit=extended_graph_follower_limit,
         filter_graph_follower_limit=filter_graph_follower_limit,
         name_list_path=name_list_path, graph_path=graph_path)

