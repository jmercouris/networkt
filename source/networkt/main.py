import networkx as nx
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import DictProperty, StringProperty, ObjectProperty, BooleanProperty, NumericProperty
from kivy.uix.scrollview import ScrollView
from kivy.uix.slider import Slider
from kivy.uix.widget import Widget
from graph.graph import Graph
from kivy.graphics import Line
from networkt.status import Status
from networkt.node import Node
from kivy.factory import Factory
from kivy.uix.recycleview import RecycleView


class NetworktUI(Widget):
    running = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super(NetworktUI, self).__init__()
        self.network = self.ids.network
        self.preview_slider = self.ids.preview_slider
        self.run_button = self.ids.run_button
    
    def run_button_release(self, *args):
        self.running = not self.running
        if (self.running):
            self.run_button.image_source = 'static/img/pause.png'
        else:
            self.run_button.image_source = 'static/img/play.png'
    
    def update_logic(self, dt):
        if (self.running):
            self.network.update_logic()
    
    def update_time(self, dt):
        if (self.running):
            self.preview_slider.step_time()


class ScrollableLabel(ScrollView):
    text = StringProperty('')


class Inspector(RecycleView):
    selected_node = ObjectProperty(None)
    
    def on_selected_node(self, *args):
        self.data = self.selected_node.get_data_representation()


class SpeedSlider(Slider):
    rate = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super(SpeedSlider, self).__init__()
        self.minimum_rate = 60
        self.maximum_rate = 86400
        self.min = self.minimum_rate
        self.max = self.maximum_rate
    
    def on_value(self, *args):
        self.rate = self.value


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
    icon = 'static/img/icon.png'
    nodes = DictProperty({})
    Factory.register('RangeSlider', module='networkt.range_slider')
    Factory.register('Network', module='networkt.network')
    Factory.register('PreviewSlider', module='networkt.preview_slider')
    Factory.register('PreviewRangeSlider', module='networkt.preview_range_slider')
    
    def build(self):
        self.networktUI = NetworktUI()
        self.load_graph()
        Clock.schedule_interval(self.networktUI.update_logic, 1.0 / 30.0)
        Clock.schedule_interval(self.networktUI.update_time, 1.0 / 5.0)
        network = self.networktUI.ids.network
        network.update_object_positions()
        return self.networktUI
    
    def load_graph(self):
        # Generate a simple graph
        self.nodes = {}
        root_user = 'daffunn'
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
            # Generate Placeholder Lines for updating
            self.nodes[edge[0]].edges_representation.append(Line(points=[0, 0, 100, 100]))
        # Generate graph metadata
        for node in self.nodes:
            nodei = self.nodes[node]
            for status in graph_object.get_statuses_for_screen_name(nodei.screen_name):
                nodei.statuses.append(Status(status, sender=nodei))
            # Sort node statuses
            nodei.statuses.sort()
        # Invoke Update
        self.nodes['0'] = Node(graph.node[root_user])
        self.nodes.pop('0', 0)
    

if __name__ == '__main__':
    NetworktApp().run()
