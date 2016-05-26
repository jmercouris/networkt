import networkx as nx
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Line, Rectangle
from kivy.properties import DictProperty, StringProperty, ObjectProperty, ListProperty, NumericProperty
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.uix.slider import Slider
from kivy.core.window import Window
from kivy.uix.stencilview import StencilView
from kivy.metrics import dp
from math import pow
from graph.graph import get_statuses_for_screen_name, load_graph_from_database
from networkt.status import Status, by_date_key
from networkt.node import Node
from networkt.camera import Camera
from networkt.range_slider import RangeSlider
from kivy.factory import Factory


class NetworktUI(Widget):
    def __init__(self, **kwargs):
        super(NetworktUI, self).__init__()
        self.network = self.ids.network
    
    def update(self, dt):
        self.network.update_logic()
        self.network.update_graphic()


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
        self.canvas.after.clear()
        with self.canvas.after:
            for marker in self.markers:
                if (marker.position * 100 > self.start and marker.position * 100 < self.end):
                    Rectangle(size=(1, self.height),
                              pos=(self.width * marker.position, self.pos[1]))
            

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
        if touch.button is 'scrollup' and self.collide_point(*touch.pos):
            self.camera.zoom_out()
            self.update_node_positions()
            return True
        if touch.button is 'scrolldown' and self.collide_point(*touch.pos):
            self.camera.zoom_in()
            self.update_node_positions()
            return True
    
    def on_touch_move(self, touch):
        # Handle Mouse Drag
        if self.collide_point(*touch.opos):
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
                if (dp(squared_radius) > squared_x + squared_y):
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
    Factory.register('RangeSlider', module='networkt.range_slider')
    
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
        # Generate graph metadata
        for node in self.nodes:
            nodei = self.nodes[node]
            for status in get_statuses_for_screen_name(nodei.screen_name):
                nodei.statuses.append(Status(status, sender=nodei))
        # Invoke Update
        self.nodes['0'] = Node(graph.node[root_user])
        self.nodes.pop('0', 0)


if __name__ == '__main__':
    NetworktApp().run()
