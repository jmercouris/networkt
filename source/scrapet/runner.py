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
        print('Retrieving user {}'.format(root_user_screen_name))
        root_user = _scraper.get_user(root_user_screen_name)
    
    ##########################################################################
    # Persist the root user's follower list
    if phase < 2:
        print('Retrieving {} followers'.format(root_user.screen_name))
        _scraper.pull_follow_network(root_user, root_user_follower_limit)
    
    # ##########################################################################
    # Perform degree 0 filtering to decide whether to pull 0th degree network
    if phase < 3:
        print('Filtering {} follower graph'.format(root_user.screen_name))
        _filter.filter_0(root_user, 'Berlin', 0.25)
    
    ##########################################################################
    # Pull sample of filter user's graph - qualifies user as transnational
    if phase < 4:
        tag = Tag.nodes.get(name=Tag.FILTER_0)
        for node in tag.users:
            print('Retrieving {} sample graph'.format(node.screen_name))
            _scraper.pull_friend_network(node, filter_graph_sample_limit)
    
    ##########################################################################
    # Filter users to see which have graphs that qualify as transnational
    if phase < 5:
        print('Transnational graph filtering complete')
        tag = Tag.nodes.get(name=Tag.FILTER_0)
        for node in tag.users:
            _filter.filter_1(node)
    
    ##########################################################################
    # Pull extended graphs of all filtered users
    if phase < 6:
        tag = Tag.nodes.get(name=Tag.FILTER_1)
        for node in tag.users:
            print('Retrieving {} graph'.format(node.screen_name))
            _scraper.pull_friend_network(node, extended_graph_limit)
            _scraper.pull_follow_network(node, extended_graph_limit)
    
    ##########################################################################
    # Pull statuses of all filtered user networks
    
    print('Execution Complete')
    
    # ##########################################################################
    # # Perform filter level 2 filtering on all nodes
    # # Show only interesting nodes - not spam, reasonable follower ratio, etc
    # network_scrape.filter_2()
    # LOGGER.log_event(0, 'Graph filtered [Filter level 2]')
    # LOGGER.update_progress(1.0)


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
