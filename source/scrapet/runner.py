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
    if phase <= 1:
        print_phase(1)
        print('Retrieving user {}'.format(root_user_screen_name))
        root_user = _scraper.get_user(root_user_screen_name)
    
    ##########################################################################
    # Persist the root user's follower list
    if phase <= 2:
        print_phase(2)
        print('Retrieving {} followers'.format(root_user.screen_name))
        _scraper.pull_follow_network(root_user, root_user_follower_limit)
    
    # ##########################################################################
    # Perform degree 0 filtering to decide whether to pull 0th degree network
    if phase <= 3:
        print_phase(3)
        print('Filtering {} follower graph'.format(root_user.screen_name))
        _filter.filter_0(root_user, 'Berlin', 0.50)
    
    ##########################################################################
    # Pull sample of filter user's graph - qualifies user as transnational
    if phase <= 4:
        print_phase(4)
        tag = Tag.nodes.get(name=Tag.FILTER_0)
        for index, node in enumerate(tag.users):
            print('{}/{} retrieving {} sample graph'.format(
                index, len(tag.users), node.screen_name),
                ' ' * 20, end='\r')
            _scraper.pull_friend_network(node, filter_graph_sample_limit)
    
    ##########################################################################
    # Filter users to see which have graphs that qualify as transnational
    if phase <= 5:
        print_phase(5)
        print('Transnational graph filtering complete')
        tag = Tag.nodes.get(name=Tag.FILTER_0)
        for node in tag.users:
            _filter.filter_1(node)
    
    ##########################################################################
    # Pull extended graphs of all transnational users
    if phase <= 6:
        print_phase(6)
        tag = Tag.nodes.get(name=Tag.FILTER_1)
        for index, node in enumerate(tag.users):
            print('{}/{} retrieving {} graph'.format(
                index + 1, len(tag.users), node.screen_name),
                ' ' * 20, end='\r')
            _scraper.pull_friend_network(node, extended_graph_limit)
            _scraper.pull_follow_network(node, extended_graph_limit)
    
    ##########################################################################
    # Pull statuses of all nodes in transnational user networks
    if phase <= 7:
        print_phase(7)
        tag = Tag.nodes.get(name=Tag.FILTER_1)
        for index, node in enumerate(tag.users):
            print('\n{}/{} retrieving statuses for {} graph\n'.format(
                index + 1, len(tag.users), node.screen_name))
            
            for index, friend in enumerate(node.friends):
                print('{}/{} friend statuses: {}'.format(
                    index + 1, len(node.friends), friend.screen_name),
                    ' ' * 20, end='\r')
                _scraper.pull_remote_status(friend)
            
            for index, follower in enumerate(node.followers):
                print('{}/{} follow statuses: {}'.format(
                    index + 1, len(node.followers), follower.screen_name),
                    ' ' * 20, end='\r')
                _scraper.pull_remote_status(follower)
    
    ##########################################################################
    # Classify nodes as relevant / non-relevant for tweet analysis
    if phase <= 8:
        print_phase(8)
        tag = Tag.nodes.get(name=Tag.FILTER_1)
        for index, node in enumerate(tag.users):
            print('{}/{} filtering {} graph'.format(
                index + 1, len(tag.users), node.screen_name), ' ' * 20, end='\r')
            _filter.filter_2(node)
    
    print('\nExecution Complete')
    

def print_phase(phase_number):
    print('\nPhase {}'.format(phase_number), '=' * 40)


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
