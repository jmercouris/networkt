import time
from math import ceil as ceiling
from twython import Twython
from twython.exceptions import TwythonAuthError
from graph.data_model import Node, Status
import neomodel


class NetworkScrape(object):
    """Documentation for NetworkScrape
    
    """
    def __init__(self, app_key, app_secret, oauth_token, oauth_token_secret):
        self.twitter = Twython(app_key, app_secret,
                               oauth_token, oauth_token_secret)
        self.scope_depth = 200
    
    def get_user(self, screen_name):
        try:
            instance = Node.create_from_response(self.twitter.lookup_user(screen_name=screen_name)[0])
            return instance
        except neomodel.exception.UniqueProperty:
            # user already exists, retrieve
            return Node.nodes.get(screen_name=screen_name)
        except Exception as e:
            print('System failure: {}'.format(e))
    
    def pull_follow_network(self, user, limit):
        scope_limit = ceiling(limit / self.scope_depth)
        
        self.pull_remote_graph(user, user.followers,
                               scope_limit, self.twitter.get_followers_list)
    
    def pull_friend_network(self, user, limit):
        scope_limit = ceiling(limit / self.scope_depth)
        
        self.pull_remote_graph(user, user.friends,
                               scope_limit, self.twitter.get_friends_list)
    
    def pull_remote_graph(self, user, relationship,
                          scope_limit, twitter_function):
        next_cursor = -1
        while(next_cursor and scope_limit):
            scope_limit -= 1
            try:
                search = twitter_function(screen_name=user.screen_name,
                                          count=self.scope_depth, cursor=next_cursor)
            except TwythonAuthError:
                # This user is not accessible to us, delete them
                user.delete()
                return
            
            for result in search['users']:
                tmp = None
                try:
                    tmp = Node.create_from_response(result)
                except neomodel.exception.UniqueProperty:
                    # user already exists, retrieve
                    tmp = Node.nodes.get(screen_name=result['screen_name'])
                except Exception as e:
                    print('System failure: {}'.format(e))
                relationship.connect(tmp)
            next_cursor = search["next_cursor"]
            
            time.sleep(60)
    
    def pull_remote_status(self, user, scope_depth=200):
        # if we have already retrieved statuses, or they have no statuses, return
        if len(user.statuses) > 0 or user.statuses_count <= 0:
            return
        
        try:
            statuses = self.twitter.get_user_timeline(screen_name=user.screen_name, count=scope_depth)
        except TwythonAuthError:
            # This user is not accessible to us, delete them
            user.delete()
            return
        
        for status in statuses:
            try:
                user.statuses.connect(Status.create_from_response(status))
            except neomodel.exception.UniqueProperty:
                print('Error: status already exists in database')
            except Exception as e:
                print('System failure: {}'.format(e))
        
        time.sleep(5)
