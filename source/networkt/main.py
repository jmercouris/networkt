import networkx as nx
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import DictProperty, StringProperty, ObjectProperty
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from graph.graph import Graph
from networkt.status import Status
from networkt.node import Node
from kivy.factory import Factory


class NetworktUI(Widget):
    def __init__(self, **kwargs):
        super(NetworktUI, self).__init__()
        self.network = self.ids.network
    
    def update(self, dt):
        self.network.update_logic()
        # self.network.update_graphic()


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


class NetworktApp(App):
    nodes = DictProperty({})
    Factory.register('RangeSlider', module='networkt.range_slider')
    Factory.register('Network', module='networkt.network')
    Factory.register('PreviewSlider', module='networkt.preview_slider')
    Factory.register('PreviewRangeSlider', module='networkt.preview_range_slider')
    
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
        # Generate Graph Object
        graph_object = Graph('sqlite://///Users/jmercouris/Documents/TUB/Transnational/source/data/data_store.db')
        graph = graph_object.load_graph_from_database(root_user)
        layout = nx.spring_layout(graph)
        # Generate the list of nodes with positions
        for node in layout:
            nodei = Node(graph.node[node])
            nodei.position = layout[node]
            self.nodes[nodei.screen_name] = nodei
        # Add edges to every node in graph
        for edge in graph.edges():
            self.nodes[edge[0]].edges.append(self.nodes[edge[1]])
        # Generate graph metadata
        for node in self.nodes:
            nodei = self.nodes[node]
            for status in graph_object.get_statuses_for_screen_name(nodei.screen_name):
                nodei.statuses.append(Status(status, sender=nodei))
        # Invoke Update
        self.nodes['0'] = Node(graph.node[root_user])
        self.nodes.pop('0', 0)


if __name__ == '__main__':
    NetworktApp().run()
