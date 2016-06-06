from networkt.range_slider import RangeSlider
from kivy.properties import DictProperty, ListProperty
from networkt.status import by_date_key
from kivy.graphics import Color, Rectangle


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
