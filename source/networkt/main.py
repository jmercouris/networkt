import networkx as nx
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Line
from kivy.properties import DictProperty, StringProperty, ObjectProperty
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.core.window import Window
from graph.graph import get_statuses_for_screen_name, load_graph_from_database
from kivy.uix.stencilview import StencilView
from kivy.metrics import dp
from math import pow
from textwrap import dedent


class NetworktUI(Widget):
    def __init__(self, **kwargs):
        super(NetworktUI, self).__init__()
        self.network = self.ids.network
    
    def update(self, dt):
        self.network.update_logic()
        self.network.update_graphic()


class ScrollableLabel(ScrollView):
    text = StringProperty('')


class Inspector(ScrollableLabel):
    selected_node = ObjectProperty(None)
    
    def on_selected_node(self, *args):
        self.text = self.selected_node.__str__()


class Statuses(ScrollableLabel):
    selected_node = ObjectProperty(None)
    
    def on_selected_node(self, *args):
        statuses_string = ''
        limit = 20
        for status in self.selected_node.statuses:
            if(limit > 0):
                statuses_string = statuses_string + status.__str__() + '\n'
                limit = limit - 1
        self.text = statuses_string


class Camera(object):
    """Documentation for Camera
    
    """
    def __init__(self, **kwargs):
        super(Camera, self).__init__()
        self.position = (0, 0)
        self.zoom = 250
        self.move_speed = 10
        self.zoom_factor = 30
    
    def shift_up(self):
        self.position = (self.position[0], self.position[1] + self.move_speed)
    
    def shift_down(self):
        self.position = (self.position[0], self.position[1] - self.move_speed)
    
    def shift_left(self):
        self.position = (self.position[0] - self.move_speed, self.position[1])
    
    def shift_right(self):
        self.position = (self.position[0] + self.move_speed, self.position[1])
    
    def shift_offset(self, offset):
        self.position = (self.position[0] + offset[0], self.position[1] + offset[1])
    
    def zoom_in(self):
        self.zoom = self.zoom + self.zoom_factor
    
    def zoom_out(self):
        self.zoom = self.zoom - self.zoom_factor


class Network(StencilView):
    """Extends Stencilview to clip drawing to bounding box
    
    
    """
    nodes = DictProperty({})
    selected_node = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super(Network, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self, 'text')
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.camera = Camera()
    
    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None
        
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if (text == 'w'):
            self.camera.shift_down()
            self.update_node_positions()
            return True
        elif (text == 'a'):
            self.camera.shift_right()
            self.update_node_positions()
            return True
        elif (text == 's'):
            self.camera.shift_up()
            self.update_node_positions()
            return True
        elif (text == 'd'):
            self.camera.shift_left()
            self.update_node_positions()
            return True
        elif (text == 'e'):
            self.camera.zoom_in()
            self.update_node_positions()
            return True
        elif (text == 'q'):
            self.camera.zoom_out()
            self.update_node_positions()
            return True
        
        return False
    
    def on_touch_down(self, touch):
        # Handle Mouse Zoom
        # TODO: Check if scroll is within bounds
        if touch.button is 'scrollup':
            self.camera.zoom_out()
            self.update_node_positions()
            return True
        if touch.button is 'scrolldown':
            self.camera.zoom_in()
            self.update_node_positions()
            return True
    
    def on_touch_move(self, touch):
        # Handle Mouse Drag
        # TODO: Check if drag is within bounds
        self.camera.shift_offset((touch.dpos[0], touch.dpos[1]))
        self.update_node_positions()
    
    def on_touch_up(self, touch):
        # Handle Clicks Within Nodes
        if touch.button is 'left':
            for node in self.nodes:
                nodei = self.nodes[node]
                # (R0-R1)^2 <= (x0-x1)^2+(y0-y1)^2 <= (R0+R1)^2
                squared_x = pow((touch.x - nodei.render_position[0]), 2)
                squared_y = pow((touch.y - nodei.render_position[1]), 2)
                squared_radius = pow(nodei.radius, 2)
                if (squared_radius > squared_x + squared_y):
                    self.selected_node = nodei
    
    def update_node_positions(self):
        for node in self.nodes:
            nodei = self.nodes[node]
            nodei.render_position = self.translate_render(nodei.position)
        self.update_graphic()
    
    def translate_render(self, position):
        position = (int(position[0] * self.camera.zoom) + 50, int(position[1] * self.camera.zoom) + 200)
        position = (position[0] + self.camera.position[0], position[1] + self.camera.position[1])
        position = (dp(position[0]), dp(position[1]))
        return position
    
    def update_graphic(self):
        self.canvas.clear()
        with self.canvas:
            Color(0, 1, 0)
            for node in self.nodes:
                nodei = self.nodes[node]
                # Draw All Nodes
                Line(circle=(nodei.render_position[0], nodei.render_position[1], dp(nodei.radius)))
                # Draw All Edges
                for edge in nodei.edges:
                    Line(points=(nodei.render_position[0], nodei.render_position[1],
                                 edge.render_position[0], edge.render_position[1]))
                # Draw All Statuses
                for status in nodei.active_statuses:
                    Line(circle=(status.render_position[0], status.render_position[1], dp(status.radius)))
    
    def update_logic(self):
        for node in self.nodes:
            nodei = self.nodes[node]
            nodei.act()


class NetworktApp(App):
    nodes = DictProperty({})
    
    def build(self):
        self.networktUI = NetworktUI()
        self.load_graph()
        Clock.schedule_interval(self.networktUI.update, 1.0 / 30.0)
        network = self.networktUI.ids.network
        network.update_node_positions()
        return self.networktUI
    
    def load_graph(self):
        # Generate a simple graph
        self.nodes = {}
        root_user = 'FactoryBerlin'
        graph = load_graph_from_database(root_user)
        layout = nx.spring_layout(graph)
        # Generate the list of nodes with positions
        for node in layout:
            nodei = Node(graph.node[node])
            nodei.position = layout[node]
            self.nodes[nodei.screen_name] = nodei
        # Add edges to every node in graph
        for edge in graph.edges():
            self.nodes[edge[0]].edges.append(self.nodes[edge[1]])
        # Invoke Update
        self.nodes['0'] = Node(graph.node[root_user])
        self.nodes.pop('0', 0)
        # Generate graph metadata
        for node in self.nodes:
            nodei = self.nodes[node]
            for status in get_statuses_for_screen_name(nodei.screen_name):
                nodei.statuses.append(Status(status, sender=nodei))


class Node(object):
    """Documentation for Node
    
    """
    def __init__(self, dictionary):
        # Rendering Specific
        self.position = (0, 0)
        self.radius = 10.0
        self.render_position = (0, 0)
        self.edges = []
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

if __name__ == '__main__':
    NetworktApp().run()
