import numpy
from networkt.range_slider import RangeSlider
from kivy.properties import DictProperty, ListProperty
from kivy.graphics import Color, Rectangle
from kivy.graphics.instructions import InstructionGroup


class Marker(object):
    """Documentation for Marker
    
    """
    def __init__(self, position, opacity, opacity_scale_factor=10):
        self.position = position
        self.opacity = opacity * opacity_scale_factor
        self.representation = Rectangle(size=(0, 0), pos=(0, 0))


class PreviewRangeSlider(RangeSlider):
    nodes = DictProperty({})
    markers = ListProperty([])
    
    def __init__(self, **kwargs):
        super(PreviewRangeSlider, self).__init__(**kwargs)
    
    def on_nodes(self, *args):
        self.update_logic()
        self.update_graphic()
        self.update_object_positions()
    
    def on_width(self, *args):
        self.update_object_positions()
    
    def update_logic(self):
        # Generate List of All Markers
        tmp_list = []
        self.markers = []
        
        for node in self.nodes:
            nodei = self.nodes[node]
            for status in nodei.statuses:
                tmp_list.append(status)
        tmp_list = [i.timestamp for i in tmp_list]
        
        # Digitize
        if len(tmp_list) > 0:
            histogram = numpy.histogram(tmp_list, bins=100)
            divisor = max(histogram[0])  # The Largest Possible value
            index = 0
            for element in histogram[0]:
                marker = Marker(index/len(histogram[0]), element / divisor)
                self.markers.append(marker)
                index = index + 1
    
    def update_graphic(self):
        self.canvas.before.clear()
        for marker in self.markers:
            instruction_group = InstructionGroup()
            instruction_group.add(Color(0, 1, 0, marker.opacity))
            instruction_group.add(marker.representation)
            self.canvas.before.add(instruction_group)
    
    def update_object_positions(self):
        for marker in self.markers:
            marker.representation.size = (self.width / len(self.markers), self.height)
            marker.representation.pos = (marker.position * self.width, self.pos[1])
    
    def date_difference(d1, d2):
        diff = d2 - d1
        diff_minutes = (diff.days * 24 * 60) + (diff.seconds/60)
        return(diff_minutes)
