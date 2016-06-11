from kivy.uix.stencilview import StencilView
from kivy.properties import DictProperty, ObjectProperty, NumericProperty
from kivy.core.window import Window
from networkt.camera import Camera
from kivy.graphics import Color
from kivy.graphics.instructions import InstructionGroup
from kivy.metrics import dp
from math import pow
from bisect import bisect_left, bisect_right
from networkt.status import StatusIndex


class Network(StencilView):
    """Extends Stencilview to clip drawing to bounding box
    
    """
    nodes = DictProperty({})
    selected_node = ObjectProperty(None)
    time = NumericProperty(0)
    time_slice_start = NumericProperty(0)
    time_slice_end = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super(Network, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self, 'text')
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.camera = Camera()
        self.event_stack = []
        # Messages Instruction Group
        self.interaction_instruction_group = InstructionGroup()
        self.interaction_instruction_group.add(Color(0, .75, 0, 1))
        self.canvas.add(self.interaction_instruction_group)
        # Node Instruction Group
        self.node_instruction_group = InstructionGroup()
        self.node_instruction_group.add(Color(0, .75, 0, 1))
        self.canvas.add(self.node_instruction_group)
    
    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None
        
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if (text == 'w'):
            self.camera.shift_down()
            self.update_object_positions()
            return True
        elif (text == 'a'):
            self.camera.shift_right()
            self.update_object_positions()
            return True
        elif (text == 's'):
            self.camera.shift_up()
            self.update_object_positions()
            return True
        elif (text == 'd'):
            self.camera.shift_left()
            self.update_object_positions()
            return True
        elif (text == 'e'):
            self.camera.zoom_in()
            self.update_object_positions()
            return True
        elif (text == 'q'):
            self.camera.zoom_out()
            self.update_object_positions()
            return True
        
        return False
    
    def on_touch_down(self, touch):
        # Handle Mouse Zoom
        if touch.button is 'scrollup' and self.collide_point(*touch.pos):
            self.camera.zoom_out()
            self.update_object_positions()
            return True
        if touch.button is 'scrolldown' and self.collide_point(*touch.pos):
            self.camera.zoom_in()
            
            self.update_object_positions()
            return True
    
    def on_touch_move(self, touch):
        # Handle Mouse Drag
        if self.collide_point(*touch.opos):
            self.camera.shift_offset((touch.dpos[0], touch.dpos[1]))
            self.update_object_positions()
    
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
    
    def translate_render(self, position):
        position = (int(position[0] * self.camera.zoom) + 50, int(position[1] * self.camera.zoom) + 200)
        position = (position[0] + self.camera.position[0], position[1] + self.camera.position[1])
        position = (dp(position[0]), dp(position[1]))
        return position
    
    def update_object_positions(self):
        for node in self.nodes:
            nodei = self.nodes[node]
            nodei.render_position = self.translate_render(nodei.position)
            nodei.representation.circle = (nodei.render_position[0], nodei.render_position[1], nodei.radius)
        
        for node in self.nodes:
            nodei = self.nodes[node]
            for index, edge in enumerate(nodei.edges):
                nodei.edges_representation[index].points = (nodei.render_position[0], nodei.render_position[1],
                                                            edge.render_position[0], edge.render_position[1])
    
    def on_nodes(self, *args):
        self.populate_event_stack()
        self.update_graphic()
    
    def populate_event_stack(self):
        self.event_stack = []
        for node in self.nodes:
            nodei = self.nodes[node]
            for status in nodei.statuses:
                self.event_stack.append(status)
        # Sort event stack
        self.event_stack.sort()
    
    def update_graphic(self):
        self.node_instruction_group.clear()
        self.node_instruction_group.add(Color(0, .50, 0, 1))
        for node in self.nodes:
            nodei = self.nodes[node]
            nodei.interaction_instruction_group = self.interaction_instruction_group
            self.node_instruction_group.add(nodei.representation)
            for edge in nodei.edges_representation:
                self.node_instruction_group.add(edge)
    
    def update_logic(self):
        for node in self.nodes:
            nodei = self.nodes[node]
            nodei.act()
    
    # Fire Events within the Time Slice
    def on_time_slice_end(self, *args):
        slice_stack = self.event_stack[bisect_right(self.event_stack, StatusIndex(self.time_slice_start)) - 1:
                                       bisect_left(self.event_stack, StatusIndex(self.time_slice_end))]
        for event in slice_stack:
            if (len(event.sender.edges) > 0):
                event.receiver = event.sender.edges[0]
                event.refresh_position()
                event.calculate_delta()
                event.sender.event_start(event)
