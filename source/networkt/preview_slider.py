from kivy.uix.slider import Slider
from kivy.properties import ListProperty, NumericProperty
from kivy.graphics import Color, Rectangle


class PreviewSlider(Slider):
    start = NumericProperty(0)
    end = NumericProperty(100)
    markers = ListProperty([])
    
    def on_markers(self, *args):
        self.update_graphic()
    
    def on_start(self, *args):
        self.update_logic()
    
    def on_end(self, *args):
        self.update_logic()
    
    def update_logic(self):
        pass
    
    def on_width(self, *args):
        self.update_object_positions()
    
    def update_graphic(self):
        # self.active_markers = []
        # for marker in self.markers:
        #     if (marker.position * 100 > self.start and marker.position * 100 < self.end):
        #         self.active_markers.append(marker)
        # total_difference = self.active_markers[-1].position - self.active_markers[0].position
        # for marker in self.active_markers:
        #     marker.sub_position = abs(self.active_markers[0].position - marker.position) / total_difference
        
        # self.canvas.after.clear()
        # with self.canvas.after:
        #     Color(0, 1, 0, .5)
        #     for marker in self.active_markers:
        #         Rectangle(size=(self.width / len(self.active_markers), self.height),
        #                   pos=(self.width * marker.sub_position, self.pos[1]))
        pass
    
    def update_object_positions(self):
        pass
    
    # def update_graphic(self):
    #     self.canvas.before.clear()
    #     for marker in self.markers:
    #         instruction_group = InstructionGroup()
    #         instruction_group.add(Color(0, 1, 0, marker.opacity))
    #         instruction_group.add(marker.representation)
    #         self.canvas.before.add(instruction_group)
