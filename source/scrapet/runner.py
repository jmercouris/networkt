# from graph.network_scrape import persist_user, pull_remote_graph_follow, pull_remote_graph_friend
# from graph.initialize import create_database_session
# from graph.initialize import Node
# from graph.graph import persist_graph
from graph.network_scrape import NetworkScrape


def main(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET, DATABASE_NAME,
         root_user='FactoryBerlin'):
    network_scrape = NetworkScrape(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET, DATABASE_NAME)
    network_scrape.persist_user(root_user)
    print(root_user)
    
    # session = create_database_session()
    # root_user_object = session.query(Node).filter_by(screen_name=root_user).first()
    # pull_remote_graph_friend(root_user, scope_depth=10)
    # pull_remote_graph_follow(root_user, scope_depth=10)
    # persist_graph(root_user, root_user)
    # pull_remote_status(root_user)


if __name__ == "__main__":
    main()

    # ##########################################################################
    # # Save the Root User to the Database
    # persist_user(root_user)
    # print('Root User: {} Persisted.'.format(root_user))
    
    # ##########################################################################
    # # Pull the Graph for the Root User
    # pull_remote_graph_follow(root_user)
    # print('Root User: {} follower graph extracted.'.format(root_user))
    
    # ##########################################################################
    # # Perform level 0 filtering on user - determine if their 1th degree network
    # # is something that should be retrieved
    # root_user_object = session.query(Node).filter_by(
    #     screen_name=root_user).first()
    # name_list = filter_node.load_name_list_into_memory()  # Load list of valid names
    # for node in root_user_object.pointer_nodes():
    #     node.filter_0 = filter_node.filter_0(node, name_list)
    # session.commit()
    # print(
    #     'Root User: {} follower graph filtered. [Filter level 0]'.format(root_user))
    
    # ##########################################################################
    # # Pull partial graphs of all filtered users following root user
    # root_user_object = session.query(Node).filter_by(
    #     screen_name=root_user).first()
    # for node in root_user_object.pointer_nodes():
    #     if (node.filter_0):
    #         pull_remote_graph_friend(node.screen_name)
    #         graph.persist_graph(node.screen_name, node.screen_name)
    # print('Root User: {} follower graphs extracted.'.format(root_user))
    
    # ##########################################################################
    # # Perform level 1 filtering on user - determine if their 1th degree network
    # # is something that should be retrieved
    # root_user_object = session.query(Node).filter_by(
    #     screen_name=root_user).first()
    # for node in root_user_object.pointer_nodes():
    #     if (node.filter_0):
    #         node.filter_1 = filter_node.filter_1(node)
    # session.commit()
    # print(
    #     'Root User: {} follower graphs filtered. [Filter level 1]'.format(root_user))
    
    # ##########################################################################
    # # Pull extended graphs of all filtered users
    # root_user_object = session.query(Node).filter_by(
    #     screen_name=root_user).first()
    # for root_node in root_user_object.pointer_nodes():
    #     if (root_node.filter_0 and root_node.filter_1):
    #         for node in root_node.reference_nodes():
    #             pull_remote_graph_friend(node.screen_name)
    #             print(root_node.screen_name, node.screen_name)
    
    # ##########################################################################
    # # Persist graphs of all filtered users
