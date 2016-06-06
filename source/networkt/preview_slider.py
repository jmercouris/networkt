from kivy.uix.slider import Slider
from kivy.properties import ListProperty, NumericProperty
from kivy.graphics import Color, Rectangle


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
