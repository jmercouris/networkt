from random import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Ellipse, Color, Line


class NetworktUI(Widget):
    pass


class Network(Widget):
    def on_touch_down(self, touch):
        with self.canvas:
            color = (random(), random(), random())
            Color(*color)
            diameter = 30.
            Ellipse(pos=(touch.x - diameter / 2, touch.y - diameter / 2), size=(diameter, diameter))
            touch.ud['line'] = Line(points=(touch.x, touch.y))
    
    def on_touch_move(self, touch):
        touch.ud['line'].points += [touch.x, touch.y]


class NetworktApp(App):
    def build(self):
        return NetworktUI()


if __name__ == '__main__':
    NetworktApp().run()
