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


class Statuses(RecycleView):
    selected_node = ObjectProperty(None)
    
    def on_selected_node(self, *args):
        tmp_data = []
        for status in self.selected_node.statuses:
            tmp_data.append(status.get_data_representation())
        self.data = tmp_data


class Timeline(RecycleView):
    selected_node = ObjectProperty(None)
    
    def on_selected_node(self, *args):
        tmp_data = []
        # Add Own Statuses
        tmp_data = tmp_data + self.selected_node.statuses
        # Gather All Statuses
        for edge in self.selected_node.inbound_edges:
            tmp_data = tmp_data + edge.statuses
        tmp_data.sort()
        # Generate Data
        tmp_data_representation = []
        for status in tmp_data:
            tmp_data_representation.append(status.get_data_representation())
        self.data = tmp_data_representation


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
        root_user = 'dtaschik'
        
        # Generate Graph Object
        graph_object = Graph('sqlite://///Users/jmercouris/Documents/TUB/Transnational/source/data/data_store.db')
        graph = graph_object.load_ego_graph_from_database(root_user, 50)
        layout = nx.spring_layout(graph)
        
        # Generate the list of nodes with positions
        for node in layout:
            nodei = Node(graph.node[node])
            nodei.position = layout[node]
            self.nodes[nodei.screen_name] = nodei
        
        # Add edges to every node in graph
        for edge in graph.edges():
            # Add Outbound edges
            self.nodes[edge[0]].edges.append(self.nodes[edge[1]])
            # Add Inbound edges
            self.nodes[edge[1]].inbound_edges.append(self.nodes[edge[0]])
            # Generate Placeholder Lines for updating
            self.nodes[edge[0]].edges_representation.append(Line(points=[0, 0, 100, 100]))
        
        # Mark Users as Followers or Friends in Ego-Centric Sense
        for index, node in enumerate(self.nodes):
            nodei = self.nodes[node]
            if len(nodei.edges) > 0 and len(nodei.inbound_edges) <= 0:
                nodei.connection = 'friend'
            elif len(nodei.inbound_edges) > 0 and len(nodei.edges) <= 0:
                nodei.connection = 'follower'
        
        # Generate graph metadata
        for index, node in enumerate(self.nodes):
            nodei = self.nodes[node]
            print('{}/{} Loading Statuses {}'.format(index, len(self.nodes), nodei.screen_name), end='\r')
            for status in graph_object.get_statuses_for_screen_name(nodei.screen_name)[:10]:
                nodei.statuses.append(Status(status, sender=nodei))
            # Sort node statuses
            nodei.statuses.sort()
        # Invoke Update
        self.nodes['0'] = Node(graph.node[root_user])
        self.nodes.pop('0', 0)
    

if __name__ == '__main__':
    NetworktApp().run()
