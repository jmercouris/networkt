import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from graph.initialize import Base, Node, Edge, Status, edge_point, edge_reference
from graph.filter_node import load_name_list_into_memory, filter_0, filter_1, filter_2
from twython import Twython


class NetworkScrape(object):
    """Documentation for NetworkScrape

    """
    def __init__(self, APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET, DATABASE_NAME):
        self.twitter = Twython(APP_KEY, APP_SECRET,
                               OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
        
        engine = create_engine(DATABASE_NAME)
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()
    
    def persist_user(self, screen_name):
        user_object = self.session.query(Node).filter_by(screen_name=screen_name).first()
        if (user_object is None):
            instance = Node(self.twitter.lookup_user(screen_name=screen_name)[0])
            self.session.add(instance)
            self.session.commit()
    
    def pull_remote_graph_follow(self, screen_name, scope_limit=1, scope_depth=200):
        user_object = self.session.query(Node).filter_by(screen_name=screen_name).first()
        if (len(user_object.pointer_nodes()) < 5):
            self.pull_remote_graph(screen_name, scope_limit, scope_depth,
                                   self.twitter.get_followers_list, self.edge_check_reference, edge_reference)
    
    def pull_remote_graph_friend(self, screen_name, scope_limit=1, scope_depth=200):
        user_object = self.session.query(Node).filter_by(screen_name=screen_name).first()
        if (len(user_object.reference_nodes()) < 5):
            self.pull_remote_graph(screen_name, scope_limit, scope_depth,
                                   self.twitter.get_friends_list, self.edge_check_point, edge_point)
    
    def edge_check_point(self, instance, user_object):
        if (self.session.query(Edge).filter_by(reference_id=instance.id, pointer_id=user_object.id).first() is None):
            return True
        else:
            return False
    
    def edge_check_reference(self, instance, user_object):
        if (self.session.query(Edge).filter_by(reference_id=user_object.id, pointer_id=instance.id).first() is None):
            return True
        else:
            return False
    
    def pull_remote_graph(self, screen_name, scope_limit, scope_depth,
                          twitter_function, edge_check_function, edge_function):
        user_object = self.session.query(Node).filter_by(screen_name=screen_name).first()
        next_cursor = -1
        
        while(next_cursor and scope_limit):
            scope_limit -= 1
            search = twitter_function(screen_name=screen_name, count=scope_depth, cursor=next_cursor)
            for result in search['users']:
                instance = self.session.query(Node).filter_by(id_str=result['id_str']).first()
                if (instance is None):
                    instance = Node(result)
                    self.session.add(instance)
                if edge_check_function(instance, user_object):
                    edge_function(instance, user_object)
                next_cursor = search["next_cursor"]
            self.session.commit()
            time.sleep(65)
    
    def pull_remote_status(self, screen_name, scope_depth=200):
        user_object = self.session.query(Node).filter_by(screen_name=screen_name).first()
        if (user_object is None or len(user_object.statuses) > 0):
            return
        try:
            statuses = self.twitter.get_user_timeline(screen_name=screen_name, count=scope_depth)
            for status in statuses:
                instance = self.session.query(Status).filter_by(id_str=status['id_str']).first()
                if (instance is None):
                    user_object.statuses.append(Status(status))
            self.session.commit()
        except:
            pass
        time.sleep(7)
    
    def get_user_from_data_store(self, screen_name):
        return self.session.query(Node).filter_by(screen_name=screen_name).first()
    
    def get_filter_nodes(self, filter_level):
        arguments = {filter_level: True}
        return self.session.query(Node).filter_by(**arguments).all()
    
    def filter_0(self, root_user, location=''):
        root_user_object = self.get_user_from_data_store(root_user)
        name_list = load_name_list_into_memory(location=location)  # Load list of valid names
        for node in root_user_object.pointer_nodes():
            node.filter_0 = filter_0(node, name_list)
        self.session.commit()
    
    def filter_1(self, root_user):
        root_user_object = self.get_user_from_data_store(root_user)
        for node in root_user_object.pointer_nodes():
            if (node.filter_0):
                node.filter_1 = filter_1(node)
        self.session.commit()
        
    def filter_2(self):
        for node in self.session.query(Node).all():
            node.filter_2 = filter_2(node)
        self.session.commit()


