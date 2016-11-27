from textwrap import dedent
from kivy.graphics import Line
from kivy.metrics import dp


class Status(object):
    """Documentation for Status
    
    """
    def __init__(self, src_status_object, sender=None, receiver=None):
        super(Status, self).__init__()
        # Initialization
        self.sender = sender
        self.receiver = receiver
        self.initialize()
        # Rendering Specific
        self.position = sender.render_position
        self.render_position = sender.render_position
        self.representation = Line(circle=(self.render_position[0], self.render_position[1], self.radius))
        # Datastore specific
        self.coordinate_longitude = src_status_object.coordinate_longitude
        self.coordinate_latitude = src_status_object.coordinate_latitude
        self.created_at = src_status_object.created_at
        self.date = src_status_object.date
        self.timestamp = self.date.timestamp()
        self.favorite_count = src_status_object.favorite_count
        self.id_str = src_status_object.id_str
        self.in_reply_to_screen_name = src_status_object.in_reply_to_screen_name
        self.in_reply_to_status_id_str = src_status_object.in_reply_to_status_id_str
        self.in_reply_to_user_id_str = src_status_object.in_reply_to_user_id_str
        self.lang = src_status_object.lang
        self.possibly_sensitive = src_status_object.possibly_sensitive
        self.quoted_status_id_str = src_status_object.quoted_status_id_str
        self.retweet_count = src_status_object.retweet_count
        self.retweeted = src_status_object.retweeted
        self.source = src_status_object.source
        self.text = src_status_object.text
        self.truncated = src_status_object.truncated
    
    def initialize(self):
        self.steps = 100
        self.radius = dp(5.0)
        self.refresh_position()
        if (self.receiver is not None):
            self.calculate_delta(steps=self.steps)
    
    def calculate_delta(self, steps=100):
        self.delta_x = (self.receiver.render_position[0] - self.sender.render_position[0]) / steps
        self.delta_y = (self.receiver.render_position[1] - self.sender.render_position[1]) / steps
    
    def refresh_position(self):
        self.position = self.sender.render_position
    
    def act(self):
        if (self.steps > 0):
            self.position = (self.position[0] + self.delta_x, self.position[1] + self.delta_y)
            self.render_position = (int(self.position[0]), int(self.position[1]))
            self.representation.circle = (self.render_position[0], self.render_position[1], self.radius)
            self.steps = self.steps - 1
        else:
            self.refresh_position()
    
    def is_alive(self):
        if (self.steps > 0):
            return True
        else:
            return False
    
    def __str__(self):
        return_string = """\
        {}
        {}
        {}
        """.format(
            self.sender.screen_name,
            self.date,
            self.text,
        )
        return dedent(return_string)
    
    def __lt__(self, other):
        return self.timestamp < other.timestamp
    
    def __gt__(self, other):
        return self.timestamp > other.timestamp
    
    def __eq__(self, other):
        return self.timestamp == other.timestamp
    
    def __le__(self, other):
        return self.timestamp <= other.timestamp
    
    def __ge__(self, other):
        return self.timestamp >= other.timestamp
    
    def __ne__(self, other):
        return self.timestamp != other.timestamp
    
    def get_data_representation(self):
        return {'user': str(self.sender.screen_name), 'date': str(self.date), 'data': str(self.text)}


class StatusIndex(object):
    """Documentation for StatusIndex

    """
    def __init__(self, timestamp):
        super(StatusIndex, self).__init__()
        self.timestamp = timestamp
