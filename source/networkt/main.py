import networkx as nx
from kivy.adapters.simplelistadapter import SimpleListAdapter
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Line
from kivy.properties import DictProperty, StringProperty
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget

from graph.graph import get_statuses_for_screen_name, load_graph_from_database


class NetworktUI(Widget):
    def update(self, dt):
        pass


class ScrollableLabel(ScrollView):
    text = StringProperty('')


class ExpandableLabel(Label):
    text = StringProperty('')


class Network(Widget):
    nodes = DictProperty({})
    
    def __init__(self, **kwargs):
        super(Network, self).__init__(**kwargs)

    def on_touch_down(self, touch):
        dictionary = self.nodes['FactoryBerlin'].__dict__
        dictionary.pop("statuses", None)
        tmp_list = []
        for key in dictionary:
            tmp_list.append(str(key) + ': ' + str(dictionary[key]))
        self.adapter = SimpleListAdapter(data=sorted(tmp_list[:]),
                                         cls=ExpandableLabel)

    def update(self):
        self.canvas.clear()
        with self.canvas:
            diameter = 10.0
            Color(0, 1, 0)
            for node in self.nodes:
                nodei = self.nodes[node]
                Line(circle=(nodei.position[0], nodei.position[1], diameter))
                for edge in nodei.edges:
                    Line(points=(nodei.position[0], nodei.position[1], edge.position[0], edge.position[1]))
    
    def on_nodes(self, *args):
        self.update()


class NetworktApp(App):
    nodes = DictProperty({})
    
    def build(self):
        self.networktUI = NetworktUI()
        self.load_graph()
        Clock.schedule_interval(self.networktUI.update, 1.0 / 60.0)
        return self.networktUI
    
    def load_graph(self):
        # Generate a simple graph
        root_user = 'FactoryBerlin'
        graph = load_graph_from_database(root_user)
        layout = nx.spring_layout(graph)
        # Generate the list of nodes with positions
        for node in layout:
            nodei = Node(graph.node[node])
            nodei.position = Node.true_position(layout[node])
            nodei.statuses = get_statuses_for_screen_name(nodei.screen_name)
            self.nodes[nodei.screen_name] = nodei
        # Add edges to every node in graph
        for edge in graph.edges():
            self.nodes[edge[0]].edges.append(self.nodes[edge[1]])
        # Invoke Update
        self.nodes['0'] = Node(graph.node[root_user])
        self.nodes.pop('0', 0)


class Node(object):
    """Documentation for Node
    
    """
    def __init__(self, dictionary):
        self.position = (0, 0)
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
        self.screen_name = dictionary.get('screenname', 'default')
        self.statuses_count = int(dictionary.get('statusescount') or -1)
        self.time_zone = dictionary.get('timezone', None)
        self.utc_offset = int(dictionary.get('utcoffset') or -1)
        self.verified = bool(dictionary.get('verified', False) or False)
        self.id = int(self.id_str or -1)
    
    def true_position(coordinates):
        return (int(coordinates[0] * 250) + 50, int(coordinates[1] * 250) + 200)


if __name__ == '__main__':
    NetworktApp().run()
