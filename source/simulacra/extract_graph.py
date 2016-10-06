from graph.network_scrape import NetworkScrape
from graph.graph import Graph


def main(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET, DATABASE_NAME, graph_path='', root_user=''):
    network_scrape = NetworkScrape(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET, DATABASE_NAME)
    graph = Graph(DATABASE_NAME)
    
    ##########################################################################
    # Persist Graphs of all filtered user networks
    root_user_object = network_scrape.get_user_from_data_store(root_user)
    graph.persist_graph(root_user_object.screen_name, graph_path, root_user_object.screen_name)

print('Hello World')
