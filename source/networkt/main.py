from kivy.app import App
from kivy.graphics import Color, Ellipse
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.properties import StringProperty, DictProperty, ObjectProperty
from kivy.clock import Clock
import networkx as nx
from graph.graph import load_graph_from_database, get_statuses_for_screen_name
from kivy.adapters.simplelistadapter import SimpleListAdapter
from kivy.uix.label import Label


class NetworktUI(Widget):
    def update(self, dt):
        pass

    def on_nodes(self, *args):
        self.ids.network.update()


class ScrollableLabel(ScrollView):
    text = StringProperty('')


class Network(Widget):
    nodes = DictProperty({})
    adapter = ObjectProperty(SimpleListAdapter(data=[],
                                               cls=Label))
    
    def __init__(self, **kwargs):
        super(Network, self).__init__(**kwargs)

    def on_touch_down(self, touch):
        dictionary = self.nodes['FactoryBerlin'].__dict__
        tmp_list = []
        for key in dictionary:
            tmp_list.append(str(key) + ': ' + str(dictionary[key]))
        self.adapter = SimpleListAdapter(data=sorted(tmp_list[:]),
                                         cls=Label)

    def update(self):
        diameter = 10.0
        with self.canvas:
            Color(0, 1, 0)
            for node in self.nodes:
                nodei = self.nodes[node]
                Ellipse(pos=(nodei.position), size=(diameter, diameter))
    
    def on_nodes(self, *args):
        self.update()


class NetworktApp(App):
    def build(self):
        self.networktUI = NetworktUI()
        self.load_graph()
        Clock.schedule_interval(self.networktUI.update, 1.0 / 60.0)
        return self.networktUI
    
    def load_graph(self):
        # generate a simple graph
        graph = load_graph_from_database('FactoryBerlin')
        layout = nx.spring_layout(graph)
        network = self.networktUI.ids.network
        # Generate the list of nodes with positions
        for node in layout:
            nodei = Node(graph.node[node])
            nodei.position = Node.true_position(layout[node])
            nodei.statuses = get_statuses_for_screen_name(nodei.screen_name)
            network.nodes[nodei.screen_name] = nodei


class Node(object):
    """Documentation for Node
    
    """
    def __init__(self, dictionary):
        self.position = ''
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
        return (int(coordinates[0] * 250) + 50, int(coordinates[1] * 250) + 200)


if __name__ == '__main__':
    NetworktApp().run()
