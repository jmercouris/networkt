import configparser
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from graph.initialize import Base, Node, Edge, Status, edge_point, edge_reference
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

class NetworkScrape(object):
    """Documentation for NetworkScrape

    """
    def __init__(self, APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET, DATABASE_NAME):
        
        



def main(root_user='FactoryBerlin'):
    persist_user(root_user)
    pull_remote_status(root_user)
    pull_remote_graph_follow(root_user, scope_depth=10)
    pull_remote_graph_friend(root_user, scope_depth=10)
    root_user_object = session.query(Node).filter_by(screen_name=root_user).first()
    for node in root_user_object.pointer_nodes():
        pull_remote_graph_friend(node.screen_name, scope_depth=10)
        pull_remote_graph_follow(node.screen_name, scope_depth=10)
    for node in root_user_object.reference_nodes():
        pull_remote_graph_friend(node.screen_name, scope_depth=10)
        pull_remote_graph_follow(node.screen_name, scope_depth=10)


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
