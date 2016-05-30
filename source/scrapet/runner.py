from graph.network_scrape import NetworkScrape
from graph.graph import Graph
# from math import floor


def main(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET, DATABASE_NAME,
         root_user='', root_user_follower_limit=200,
         name_list_path='', graph_path=''):
    network_scrape = NetworkScrape(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET, DATABASE_NAME)
    
    ##########################################################################
    # Persist the root user
    network_scrape.persist_user(root_user)
    print('Persisted Root User')
    
    ##########################################################################
    # Persist the root user's follower list
    # network_scrape.pull_remote_graph_follow(root_user, scope_limit=floor(int(root_user_follower_limit) / 200) + 1)
    network_scrape.pull_remote_graph_follow(root_user)
    print('Persisted Root user follower graph')
    
    ##########################################################################
    # Perform degree 0 filtering to decide whether to pulll 0th degree network
    network_scrape.filter_0(root_user, location=name_list_path)
    print('Root User: {} follower graph filtered. [Filter level 0]'.format(root_user))
    
    ##########################################################################
    # Pull partial graphs of all filtered users following root user
    graph = Graph(DATABASE_NAME, graph_path)
    root_user_object = network_scrape.get_user_from_data_store(root_user)
    for node in root_user_object.pointer_nodes():
        if (node.filter_0):
            network_scrape.pull_remote_graph_friend(node.screen_name)
            graph.persist_graph(node.screen_name, node.screen_name)
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
            for node in root_node.reference_nodes():
                network_scrape.pull_remote_graph_friend(node.screen_name)


if __name__ == "__main__":
    pass
    # Load Config File and Execute Main
    # main()
