import configparser
import time
import graph
import filter_node
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from initialize import Base, Node, Edge, Status, edge_point, edge_reference
from twython import Twython


settings = configparser.ConfigParser()
settings.read('configuration.ini')

APP_KEY = settings.get('twython-configuration', 'key')
APP_SECRET = settings.get('twython-configuration', 'secret')
OAUTH_TOKEN = settings.get('twython-configuration', 'token')
OAUTH_TOKEN_SECRET = settings.get('twython-configuration', 'token_secret')
DATABASE_NAME = settings.get('database-configuration', 'database_name')

twitter = Twython(APP_KEY, APP_SECRET,
                  OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

engine = create_engine(DATABASE_NAME)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


def main(root_user='FactoryBerlin'):
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
    # graph.persist_graph('CookMal', 'CookMal')
    persist_user(root_user)
    pull_remote_status(root_user)
    pull_remote_graph_follow(root_user)


def persist_user(screen_name):
    user_object = session.query(Node).filter_by(
        screen_name=screen_name).first()
    if (user_object is None):
        instance = Node(twitter.lookup_user(screen_name=screen_name)[0])
        session.add(instance)
        session.commit()


def pull_remote_status(screen_name, scope_depth=200):
    user_object = session.query(Node).filter_by(screen_name=screen_name).first()
    if (user_object is None):
        return
    
    statuses = twitter.get_user_timeline(screen_name=screen_name, count=scope_depth)
    for status in statuses:
        instance = session.query(Status).filter_by(id_str=status['id_str']).first()
        if (instance is None):
            user_object.statuses.append(Status(status))
    session.commit()


def pull_remote_graph(screen_name, scope_limit, scope_depth, twitter_function, edge_check_function, edge_function):
    user_object = session.query(Node).filter_by(screen_name=screen_name).first()
    next_cursor = -1

    while(next_cursor and scope_limit):
        scope_limit -= 1
        search = twitter_function(screen_name=screen_name, count=scope_depth, cursor=next_cursor)
        for result in search['users']:
            instance = session.query(Node).filter_by(screen_name=result['screen_name']).first()
            if (instance is None):
                instance = Node(result)
                session.add(instance)
            if edge_check_function(instance, user_object):
                edge_function(instance, user_object)
        next_cursor = search["next_cursor"]
        session.commit()
        time.sleep(65)


def edge_check_point(instance, user_object):
    if (session.query(Edge).filter_by(reference_id=instance.id, pointer_id=user_object.id).first() is None):
        return True
    else:
        return False


def edge_check_reference(instance, user_object):
    if (session.query(Edge).filter_by(reference_id=user_object.id, pointer_id=instance.id).first() is None):
        return True
    else:
        return False


def pull_remote_graph_friend(screen_name, scope_limit=1, scope_depth=200):
    user_object = session.query(Node).filter_by(
        screen_name=screen_name).first()
    if (len(user_object.reference_nodes()) < 5):
        pull_remote_graph(screen_name, scope_limit, scope_depth,
                          twitter.get_friends_list, edge_check_point, edge_point)


def pull_remote_graph_follow(screen_name, scope_limit=1, scope_depth=200):
    user_object = session.query(Node).filter_by(
        screen_name=screen_name).first()
    if (len(user_object.pointer_nodes()) < 5):
        pull_remote_graph(screen_name, scope_limit, scope_depth,
                          twitter.get_followers_list, edge_check_reference, edge_reference)


if __name__ == "__main__":
    main()
