import networkx as nx
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Line
from kivy.properties import DictProperty, StringProperty, ObjectProperty
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.stencilview import StencilView
from kivy.metrics import dp
from math import pow
from graph.graph import get_statuses_for_screen_name, load_graph_from_database
from networkt.status import Status
from networkt.node import Node
from networkt.camera import Camera


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


if __name__ == '__main__':
    NetworktApp().run()
