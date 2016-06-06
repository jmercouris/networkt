import networkx as nx
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Rectangle, Color
from kivy.properties import DictProperty, StringProperty, ObjectProperty, ListProperty, NumericProperty
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.uix.slider import Slider
from graph.graph import Graph
from networkt.status import Status, by_date_key
from networkt.node import Node
from networkt.range_slider import RangeSlider
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


class PreviewSlider(Slider):
    start = NumericProperty(0)
    end = NumericProperty(100)
    markers = ListProperty([])
    
    def on_start(self, *args):
        self.update_graphic()
    
    def on_end(self, *args):
        self.update_graphic()
    
    def update_logic(self):
        pass
    
    def update_graphic(self):
        self.active_markers = []
        for marker in self.markers:
            if (marker.position * 100 > self.start and marker.position * 100 < self.end):
                self.active_markers.append(marker)
        total_difference = self.active_markers[-1].position - self.active_markers[0].position
        for marker in self.active_markers:
            marker.sub_position = abs(self.active_markers[0].position - marker.position) / total_difference
        
        self.canvas.after.clear()
        with self.canvas.after:
            Color(0, 1, 0, .5)
            for marker in self.active_markers:
                Rectangle(size=(1, self.height),
                          pos=(self.width * marker.sub_position, self.pos[1]))


class PreviewRangeSlider(RangeSlider):
    nodes = DictProperty({})
    markers = ListProperty([])
    
    def __init__(self, **kwargs):
        super(PreviewRangeSlider, self).__init__(**kwargs)
    
    def on_nodes(self, *args):
        self.update_logic()
        self.update_graphic()
    
    def on_width(self, *args):
        self.update_logic()
        self.update_graphic()
    
    def update_logic(self):
        tmp_list = []
        for node in self.nodes:
            nodei = self.nodes[node]
            for status in nodei.statuses:
                tmp_list.append(status)
        self.markers = sorted(tmp_list, key=by_date_key)
        
        if len(self.markers) > 0:
            total_difference = PreviewRangeSlider.date_difference(self.markers[0].date, self.markers[-1].date)
            for marker in self.markers:
                marker.position = PreviewRangeSlider.date_difference(self.markers[0].date,
                                                                     marker.date) / total_difference
    
    def update_graphic(self):
        self.canvas.after.clear()
        with self.canvas.after:
            Color(0, 1, 0, .25)
            for marker in self.markers:
                Rectangle(size=(1, self.height),
                          pos=(self.width * marker.position, self.pos[1]))
    
    def date_difference(d1, d2):
        diff = d2 - d1
        diff_minutes = (diff.days * 24 * 60) + (diff.seconds/60)
        return(diff_minutes)


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
