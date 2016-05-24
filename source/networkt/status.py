from textwrap import dedent


class Status(object):
    """Documentation for Status
    
    """
    def __init__(self, src_status_object, sender=None, receiver=None):
        super(Status, self).__init__()
        # Rendering Specific
        self.sender = sender
        self.position = sender.render_position
        self.render_position = sender.render_position
        self.steps = 10
        self.radius = 5.0
        if (receiver is not None):
            self.receiver = receiver
            self.calculate_delta()
        # Datastore specific
        self.coordinate_longitude = src_status_object.coordinate_longitude
        self.coordinate_latitude = src_status_object.coordinate_latitude
        self.created_at = src_status_object.created_at
        self.date = src_status_object.date
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
        
    def calculate_delta(self):
        self.delta_x = (self.receiver.render_position[0] - self.sender.render_position[0]) / self.steps
        self.delta_y = (self.receiver.render_position[1] - self.sender.render_position[1]) / self.steps
    
    def act(self):
        if (self.steps > 0):
            self.position = (self.position[0] + self.delta_x, self.position[1] + self.delta_y)
            self.render_position = (int(self.position[0]), int(self.position[1]))
            self.steps = self.steps - 1
    
    def is_alive(self):
        if (self.steps > 0):
            return True
        else:
            return False
    
    def __str__(self):
        return_string = """\
        {}
        {}
        """.format(
            self.sender.screen_name,
            self.text,
        )
        return dedent(return_string)
