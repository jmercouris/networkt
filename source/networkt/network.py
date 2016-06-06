from kivy.uix.stencilview import StencilView
from kivy.properties import DictProperty, ObjectProperty, NumericProperty
from kivy.core.window import Window
from networkt.camera import Camera
from kivy.graphics import Color, Line
from kivy.graphics.instructions import InstructionGroup
from kivy.metrics import dp
from math import pow


class Network(StencilView):
    """Extends Stencilview to clip drawing to bounding box
    
    """
    nodes = DictProperty({})
    selected_node = ObjectProperty(None)
    time = NumericProperty(0)
    
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
            nodei.representation.circle = (nodei.render_position[0], nodei.render_position[1], nodei.radius)
    
    def translate_render(self, position):
        position = (int(position[0] * self.camera.zoom) + 50, int(position[1] * self.camera.zoom) + 200)
        position = (position[0] + self.camera.position[0], position[1] + self.camera.position[1])
        position = (dp(position[0]), dp(position[1]))
        return position
    
    def on_nodes(self, *args):
        self.update_graphic()
    
    def update_graphic(self):
        self.canvas.clear()
        green = InstructionGroup()
        green.add(Color(0, 1, 0, 0.5))
        for node in self.nodes:
            nodei = self.nodes[node]
            green.add(nodei.representation)
        
        self.canvas.add(green)
        
        with self.canvas:
            Color(0, 1, 0)
            for node in self.nodes:
                nodei = self.nodes[node]
                nodei.representation
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