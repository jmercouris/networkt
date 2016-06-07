from kivy.uix.slider import Slider
from kivy.properties import ListProperty, NumericProperty
from kivy.graphics import Color, Rectangle
from kivy.graphics.instructions import InstructionGroup


class PreviewSlider(Slider):
    start = NumericProperty(0)
    end = NumericProperty(100)
    markers = ListProperty([])
    
    def __init__(self, **kwargs):
        super(PreviewSlider, self).__init__(**kwargs)
        self.active_markers = []
    
    def on_markers(self, *args):
        self.update_graphic()
    
    def on_start(self, *args):
        self.update_logic()
        self.update_object_positions()
    
    def on_end(self, *args):
        self.update_logic()
        self.update_object_positions()
    
    def update_logic(self):
        self.active_markers = []
        for marker in self.markers:
            if (marker.position * 100 >= self.start and marker.position * 100 <= self.end):
                self.active_markers.append(marker)
                marker.active = True
            else:
                marker.active = False
    
    def on_width(self, *args):
        self.update_object_positions()
    
    def update_graphic(self):
        self.canvas.before.clear()
        # Add all Markers to the screen
        for marker in self.markers:
            instruction_group = InstructionGroup()
            instruction_group.add(Color(0, 1, 0, marker.opacity))
            instruction_group.add(marker.sub_representation)
            self.canvas.before.add(instruction_group)
        pass
    
    def update_object_positions(self):
        # Only Display Active Marker
        for index, marker in enumerate(self.active_markers):
            marker.sub_representation.size = (self.width / len(self.active_markers), self.height)
            marker.sub_representation.pos = (self.width * (index/len(self.active_markers)), self.pos[1])
        for marker in self.markers:
            if not marker.active:
                marker.sub_representation.size = (0, 0)
                marker.sub_representation.pos = (-1, -1)
