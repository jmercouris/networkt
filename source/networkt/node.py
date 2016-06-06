from textwrap import dedent
from kivy.graphics import Line


class Node(object):
    """Documentation for Node
    
    """
    def __init__(self, dictionary):
        # Rendering Specific
        self.position = (0, 0)
        self.radius = 10.0
        self.render_position = (0, 0)
        self.representation = Line(circle=(self.render_position[0], self.render_position[1], self.radius))
        self.edges = []
        self.edges_representation = []
        self.statuses = []
        self.active_statuses = []
        # Data Store Specific
        self.name = dictionary.get('name', None)
        self.screen_name = dictionary.get('screenname', 'default')
        self.followers_count = int(dictionary.get('followerscount') or -1)
        self.friends_count = int(dictionary.get('friendscount') or -1)
        self.lang = dictionary.get('lang', None)
        self.location = dictionary.get('location', None)
        self.time_zone = dictionary.get('timezone', None)
        self.utc_offset = int(dictionary.get('utcoffset') or -1)
        self.created_at = dictionary.get('createdat', None)
        self.description = dictionary.get('description', None)
        self.statuses_count = int(dictionary.get('statusescount') or -1)
        self.favorites_count = int(dictionary.get('favouritescount') or -1)
        self.listed_count = int(dictionary.get('listedcount') or -1)
        self.verified = bool(dictionary.get('verified', False) or False)
        self.id_str = dictionary.get('idstr', None)
        self.id = int(self.id_str or -1)
    
    def act(self):
        tmp_active_statuses = []
        for status in self.active_statuses:
            if (status.is_alive()):
                status.act()
                tmp_active_statuses.append(status)
        self.active_statuses = tmp_active_statuses
    
    def __str__(self):
        return_string = """\
        Name: {}
        ------------------------------------------------------------
        Screen name: {}
        ------------------------------------------------------------
        Followers count: {}
        ------------------------------------------------------------
        Friends count: {}
        ------------------------------------------------------------
        Lang: {}
        ------------------------------------------------------------
        Location: {}
        ------------------------------------------------------------
        Time zone: {}
        ------------------------------------------------------------
        UTC offset: {}
        ------------------------------------------------------------
        Created at: {}
        ------------------------------------------------------------
        Description: {}
        ------------------------------------------------------------
        Statuses count: {}
        ------------------------------------------------------------
        Favorites count: {}
        ------------------------------------------------------------
        Listed count: {}
        ------------------------------------------------------------
        Verified: {}
        ------------------------------------------------------------
        Id: {}
        """.format(
            self.name,
            self.screen_name,
            self.followers_count,
            self.friends_count,
            self.lang,
            self.location,
            self.time_zone,
            self.utc_offset,
            self.created_at,
            self.description,
            self.statuses_count,
            self.favorites_count,
            self.listed_count,
            self.verified,
            self.id,
        )
        return dedent(return_string)
