from kivy.app import App
from kivy.graphics import Color, Ellipse
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.properties import StringProperty, DictProperty
from kivy.clock import Clock
import networkx as nx
from graph.graph import load_graph_from_database, get_statuses_for_screen_name


class NetworktUI(Widget):
    def change_text(self):
        self.ids.messages.text = 'LOL'
    
    def update(self, dt):
        pass


class ScrollableLabel(ScrollView):
    text = StringProperty('')


class Network(Widget):
    def __init__(self, **kwargs):
        super(Network, self).__init__(**kwargs)

    def on_touch_down(self, touch):
        x = touch.x
        y = touch.y
        if self.collide_point(x, y):
            with self.canvas:
                Color(0, 1, 0)
                diameter = 30.
                Ellipse(pos=(touch.x - diameter / 2, touch.y - diameter / 2), size=(diameter, diameter))
                Ellipse(pos=(200, 200), size=(30.0, 30.0))
        else:
            return False
    
    def on_nodes(self, *args):
        print('lol')


class NetworktApp(App):
    def build(self):
        networktUI = NetworktUI()
        self.load_graph()
        Clock.schedule_interval(networktUI.update, 1.0 / 60.0)
        return networktUI
    
    nodes = DictProperty({})
    
    def load_graph(self):
        # generate a simple graph
        graph = load_graph_from_database('FactoryBerlin')
        layout = nx.spring_layout(graph)
        # Generate the list of nodes with positions
        for node in layout:
            nodei = Node(graph.node[node])
            nodei.position = Node.true_position(layout[node])
            nodei.statuses = get_statuses_for_screen_name(nodei.screen_name)
            self.nodes[nodei.screen_name] = nodei


class Node(object):
    """Documentation for Node
    
    """
    def __init__(self, dictionary):
        self.tick = 0
        self.position = ''
        self.active_statuses = []
        self.edges = []
        self.created_at = dictionary.get('createdat', None)
        self.description = dictionary.get('description', None)
        self.favorites_count = int(dictionary.get('favouritescount') or -1)
        self.followers_count = int(dictionary.get('followerscount') or -1)
        self.friends_count = int(dictionary.get('friendscount') or -1)
        self.id_str = dictionary.get('idstr', None)
        self.lang = dictionary.get('lang', None)
        self.listed_count = int(dictionary.get('listedcount') or -1)
        self.location = dictionary.get('location', None)
        self.name = dictionary.get('name', None)
        self.screen_name = dictionary.get('screenname', None)
        self.statuses_count = int(dictionary.get('statusescount') or -1)
        self.time_zone = dictionary.get('timezone', None)
        self.utc_offset = int(dictionary.get('utcoffset') or -1)
        self.verified = bool(dictionary.get('verified', False) or False)
        self.id = int(self.id_str)
    
    def true_position(coordinates):
        return (int(coordinates[0] * 250) + 50, int(coordinates[1] * 250) + 50)


if __name__ == '__main__':
    NetworktApp().run()
