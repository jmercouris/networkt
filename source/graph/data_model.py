"""Database Definitions

"""
from neomodel import (StructuredNode, StringProperty, IntegerProperty,
                      DateProperty, BooleanProperty, RelationshipTo)
import datetime


class Node(StructuredNode):
    name = StringProperty()
    screen_name = StringProperty(unique_index=True)
    
    created_at = StringProperty()
    description = StringProperty()
    favorites_count = IntegerProperty()
    followers_count = IntegerProperty()
    friends_count = IntegerProperty()
    id_str = StringProperty()
    lang = StringProperty()
    listed_count = IntegerProperty()
    location = StringProperty()
    statuses_count = IntegerProperty()
    time_zone = StringProperty()
    utc_offset = IntegerProperty()
    verified = BooleanProperty()
    
    friends = RelationshipTo('Node', 'FRIEND')
    followers = RelationshipTo('Node', 'FOLLOWER')
    
    def create_from_response(dictionary):
        name = dictionary.get('name', None)
        screen_name = dictionary.get('screen_name', None)
        
        created_at = dictionary.get('created_at', None)
        description = dictionary.get('description', None)
        favorites_count = int(dictionary.get('favourites_count') or -1)
        followers_count = int(dictionary.get('followers_count') or -1)
        friends_count = int(dictionary.get('friends_count') or -1)
        id_str = dictionary.get('id_str', None)
        lang = dictionary.get('lang', None)
        listed_count = int(dictionary.get('listed_count') or -1)
        location = dictionary.get('location', None)
        statuses_count = int(dictionary.get('statuses_count') or -1)
        time_zone = dictionary.get('time_zone', None)
        utc_offset = int(dictionary.get('utc_offset') or -1)
        verified = bool(dictionary.get('verified', False) or False)
        tmp = Node(name=name,
                   screen_name=screen_name,
                   created_at=created_at,
                   description=description,
                   favorites_count=favorites_count,
                   followers_count=followers_count,
                   friends_count=friends_count,
                   id_str=id_str,
                   lang=lang,
                   listed_count=listed_count,
                   location=location,
                   statuses_count=statuses_count,
                   time_zone=time_zone,
                   utc_offset=utc_offset,
                   verified=verified)
        tmp.save()
        
        return tmp


class Status(StructuredNode):
    coordinate_longitude = StringProperty()
    coordinate_latitude = StringProperty()
    created_at = StringProperty()
    date = DateProperty()
    favorite_count = IntegerProperty()
    id_str = StringProperty()
    in_reply_to_screen_name = StringProperty()
    in_reply_to_status_id_str = StringProperty()
    in_reply_to_user_id_str = StringProperty()
    lang = StringProperty()
    possibly_sensitive = BooleanProperty()
    quoted_status_id_str = StringProperty()
    retweet_count = IntegerProperty()
    retweeted = BooleanProperty()
    source = StringProperty()
    text = StringProperty()
    truncated = BooleanProperty()
    cluster = IntegerProperty()
    
    def create_from_response(dictionary):
        """TODO: Persist object
        
        """
        created_at = dictionary.get('created_at', None)
        favorite_count = int(dictionary.get('favorite_count') or -1)
        id_str = dictionary.get('id_str', None)
        in_reply_to_screen_name = dictionary.get('in_reply_to_screen_name', None)
        in_reply_to_status_id_str = dictionary.get('in_reply_to_status_id_str', None)
        in_reply_to_user_id_str = dictionary.get('in_reply_to_user_id_str', None)
        lang = dictionary.get('lang', None)
        possibly_sensitive = bool(dictionary.get('possibly_sensitive', False) or False)
        quoted_status_id_str = dictionary.get('quoted_status_id_str', None)
        retweet_count = int(dictionary.get('retweet_count') or -1)
        retweeted = bool(dictionary.get('retweeted', False) or False)
        source = dictionary.get('source', None)
        text = dictionary.get('text', None)
        truncated = bool(dictionary.get('truncated', False) or False)
        date = datetime.strptime(created_at, '%a %b %d %H:%M:%S +0000 %Y')

        return Status(created_at=created_at,
                      favorite_count=favorite_count,
                      id_str=id_str,
                      in_reply_to_screen_name=in_reply_to_screen_name,
                      in_reply_to_status_id_str=in_reply_to_status_id_str,
                      in_reply_to_user_id_str=in_reply_to_user_id_str,
                      lang=lang,
                      possibly_sensitive=possibly_sensitive,
                      quoted_status_id_str=quoted_status_id_str,
                      retweet_count=retweet_count,
                      retweeted=retweeted,
                      source=source,
                      text=text,
                      truncated=truncated,
                      date=date)
    
    def __lt__(self, other):
        return self.date.timestamp() < other.date.timestamp()
    
    def __gt__(self, other):
        return self.date.timestamp() > other.date.timestamp()
    
    def __eq__(self, other):
        return self.date.timestamp() == other.date.timestamp()
    
    def __le__(self, other):
        return self.date.timestamp() <= other.date.timestamp()
    
    def __ge__(self, other):
        return self.date.timestamp() >= other.date.timestamp()
    
    def __ne__(self, other):
        return self.date.timestamp() != other.date.timestamp()


class Tag(StructuredNode):
    FILTER_0 = 'filter_0'
    FILTER_1 = 'filter_1'
    FILTER_2 = 'filter_2'
    
    name = StringProperty()
    users = RelationshipTo('Node', 'USER')
