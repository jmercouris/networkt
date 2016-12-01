import configparser
from graph.network_scrape import NetworkScrape


def main(app_key, app_secret, oauth_token, oauth_token_secret,
         root_user='',
         root_user_follower_limit=200,
         filter_graph_follower_limit=200,
         extended_graph_follower_limit=200,
         name_list_path='', graph_path=''):
    
    network_scrape = NetworkScrape(app_key, app_secret, oauth_token, oauth_token_secret)
    
    ##########################################################################
    # Persist the root user
    network_scrape.persist_user(root_user)
    
    ##########################################################################
    # Persist the root user's follower list
    network_scrape.pull_follow_network(root_user, root_user_follower_limit)
    
    # ##########################################################################
    # # Perform degree 0 filtering to decide whether to pull 0th degree network
    # if (network_scrape.nodes_filtered_at_level('filter_1') is None):
    #     network_scrape.filter_0(root_user, location=name_list_path)
    #     LOGGER.log_event(0, 'Root User: {} follower graph filtered [Filter level 0]'.format(root_user))
    #     LOGGER.update_progress(0.20)
    # else:
    #     LOGGER.log_event(0, 'Skipped Root User follower graph filtering (already done)')

    print('Execution Complete')
    
    # ##########################################################################
    # # Pull partial graphs of all filtered users following root user
    # if (network_scrape.nodes_filtered_at_level('filter_1') is None):
    #     root_user_object = network_scrape.get_user_from_data_store(root_user)
    #     for node in root_user_object.pointer_nodes():
    #         if (node.filter_0):
    #             try:
    #                 network_scrape.pull_remote_graph_friend(node.screen_name, extended_graph_follower_limit)
    #                 LOGGER.log_event(0, 'Partial Graph: {} extracted.'.format(node.screen_name))
    #             except:
    #                 LOGGER.log_event(0, 'Could not extract partial graph: {}'.format(node.screen_name))
    #     LOGGER.log_event(0, 'Root User: {} follower graphs extracted'.format(root_user))
    #     LOGGER.update_progress(0.30)
    # else:
    #     LOGGER.log_event(0, 'Skipped pulling partial graphs of filtered users (already done)')
    
    # ##########################################################################
    # # Perform level 1 filtering on root_user - determine if their 1th degree network
    # # is something that should be retrieved
    # if (network_scrape.statuses_exist() is None):
    #     network_scrape.filter_1(root_user)
    #     LOGGER.log_event(0, 'Root User: {} follower graphs filtered [Filter level 1]'.format(root_user))
    #     LOGGER.update_progress(0.35)
    # else:
    #     LOGGER.log_event(0, 'Skipped filter level 1 of transnational users (already done)')
    
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
    
    # Network Scrape Parameters
    app_key = settings.get('twython-configuration', 'key')
    app_secret = settings.get('twython-configuration', 'secret')
    oauth_token = settings.get('twython-configuration', 'token')
    oauth_token_secret = settings.get('twython-configuration', 'token_secret')
    graph_path = settings.get('persistence-configuration', 'graph_path')
    # Scrape Specific Configuration Details
    root_user = settings.get('scrape-configuration', 'root_user')
    name_list_path = settings.get('scrape-configuration', 'name_list_path')
    root_user_follower_limit = int(settings.get('scrape-configuration', 'root_user_follower_limit'))
    filter_graph_follower_limit = int(settings.get('scrape-configuration', 'filter_graph_follower_limit'))
    extended_graph_follower_limit = int(settings.get('scrape-configuration', 'extended_graph_follower_limit'))

    main(app_key, app_secret, oauth_token, oauth_token_secret,
         root_user=root_user, root_user_follower_limit=root_user_follower_limit,
         extended_graph_follower_limit=extended_graph_follower_limit,
         filter_graph_follower_limit=filter_graph_follower_limit,
         name_list_path=name_list_path, graph_path=graph_path)
