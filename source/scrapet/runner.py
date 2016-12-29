import configparser
import argparse
from graph.network_scrape import NetworkScrape
from graph.data_model import Tag
from graph.filter_node import Filter

parser = argparse.ArgumentParser(description='Scrapet: Twitter scraping tool.')
parser.add_argument('--phase', dest='phase', action='store', nargs='?', type=int, default=0,
                    help='Which phase of extraction to resume operation at')


def main(app_key, app_secret, oauth_token, oauth_token_secret,
         phase, root_user_screen_name='',
         root_user_follower_limit=200,
         filter_graph_sample_limit=200,
         extended_graph_limit=200,
         graph_path=''):
    
    # Declaration / Initialization
    _scraper = NetworkScrape(app_key, app_secret, oauth_token, oauth_token_secret)
    _filter = Filter()
    root_user = None
    
    ##########################################################################
    # Persist the root user
    if phase < 1:
        root_user = _scraper.get_user(root_user_screen_name)
        print('Root user {} retrieved'.format(root_user_screen_name))
    
    ##########################################################################
    # Persist the root user's follower list
    if phase < 2:
        _scraper.pull_follow_network(root_user, root_user_follower_limit)
        print('{} followers retrieved'.format(root_user.screen_name))
    
    # ##########################################################################
    # Perform degree 0 filtering to decide whether to pull 0th degree network
    if phase < 3:
        _filter.filter_0(root_user, 'Berlin', 0.25)
        print('{} follower graph filtered'.format(root_user.screen_name))
    
    ##########################################################################
    # Pull sample of filter user's graph - qualifies user as transnational
    if phase < 4:
        tag = Tag.nodes.get(name=Tag.FILTER_0)
        for node in tag.users:
            _scraper.pull_friend_network(node, filter_graph_sample_limit)
            _scraper.pull_follow_network(node, filter_graph_sample_limit)
            print('{} sample graph extracted'.format(node.screen_name))
    
    ##########################################################################
    # Filter users to see which have graphs that qualify as transnational
    if phase < 5:
        tag = Tag.nodes.get(name=Tag.FILTER_0)
        for node in tag.users:
            _filter.filter_1(node)
        print('Transnational graph filtering complete')
    
    print('Execution Complete')
    
    # ##########################################################################
    # # Pull extended graphs of all filtered users, pull their followers as well
    # if (network_scrape.statuses_exist() is None):
    #     for node in network_scrape.get_users_from_filter_level('filter_1'):
    #         try:
    #             network_scrape.pull_remote_graph_follow(node.screen_name, extended_graph_follower_limit)
    #             LOGGER.log_event(0, '{} follower subgraph extracted'.format(node.screen_name))
    #         except:
    #             LOGGER.log_event(0, '{} follower subgraph could not be extracted'.format(node.screen_name))
    #             LOGGER.update_progress(0.60)
    # else:
    #     LOGGER.log_event(0, 'Skipped subgraph extraction of all filter 1 users (already done)')
    
    # ##########################################################################
    # # Pull statuses of all filtered user networks
    # if (network_scrape.nodes_filtered_at_level('filter_2') is None):
    #     for node in network_scrape.get_users_from_filter_level('filter_1'):
    #         # If length is less than 0, probably have already worked on this network
    #         if(len(node.statuses) <= 0):
    #             print('Working on {}'.format(node.screen_name))
    #             network_scrape.pull_remote_status(node.screen_name)
                    
    #             for nodey in node.reference_nodes():
    #                 network_scrape.pull_remote_status(nodey.screen_name)
    #                 LOGGER.log_event(0, '{} friend {} stat extracted'.format(node.screen_name, nodey.screen_name))
    #             for nodey in node.pointer_nodes():
    #                 network_scrape.pull_remote_status(nodey.screen_name)
    #                 LOGGER.log_event(0, '{} follow {} stat extracted'.format(node.screen_name, nodey.screen_name))
    #         else:
    #             print('Skipped user {}'.format(node.screen_name))
            
    #     LOGGER.update_progress(0.70)
    # else:
    #     LOGGER.log_event(0, 'Skipped statuses extraction (already done)')
    
    # ##########################################################################
    # # Persist Graphs of all filtered user networks
    # if (network_scrape.nodes_filtered_at_level('filter_2') is None):
    #     root_user_object = network_scrape.get_user_from_data_store(root_user)
    #     for node in root_user_object.pointer_nodes():
    #         if (node.filter_0 and node.filter_1):
    #             graph.persist_graph(node.screen_name, graph_path, node.screen_name)
    #     graph.persist_graph(root_user_object.screen_name, graph_path, root_user_object.screen_name)
    #     LOGGER.update_progress(0.90)
    # else:
    #     LOGGER.log_event(0, 'Skipped graph persistence to disk (already done)')
    
    # ##########################################################################
    # # Perform filter level 2 filtering on all nodes
    # # Show only interesting nodes - not spam, reasonable follower ratio, etc
    # network_scrape.filter_2()
    # LOGGER.log_event(0, 'Graph filtered [Filter level 2]')
    # LOGGER.update_progress(1.0)
    
    # ##########################################################################
    # # Finished
    # LOGGER.log_event(0, 'Finished!')


if __name__ == "__main__":
    settings = configparser.ConfigParser()
    settings.read('scrapet.ini')
    
    # Network scrape parameters
    app_key = settings.get('twython-configuration', 'key')
    app_secret = settings.get('twython-configuration', 'secret')
    oauth_token = settings.get('twython-configuration', 'token')
    oauth_token_secret = settings.get('twython-configuration', 'token_secret')
    graph_path = settings.get('persistence-configuration', 'graph_path')
    
    # Scrape specific configuration details
    root_user_screen_name = settings.get('scrape-configuration', 'root_user')
    root_user_follower_limit = int(settings.get('scrape-configuration', 'root_user_follower_limit'))
    filter_graph_sample_limit = int(settings.get('scrape-configuration', 'filter_graph_sample_limit'))
    extended_graph_limit = int(settings.get('scrape-configuration', 'extended_graph_limit'))
    
    # Command line arguments
    args = parser.parse_args()
    phase = args.phase
    
    main(app_key, app_secret, oauth_token, oauth_token_secret, phase,
         root_user_screen_name=root_user_screen_name, root_user_follower_limit=root_user_follower_limit,
         extended_graph_limit=extended_graph_limit,
         filter_graph_sample_limit=filter_graph_sample_limit,
         graph_path=graph_path)
