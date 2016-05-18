from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Ellipse, Color


class NetworktUI(Widget):
    pass


class Network(Widget):
    def on_touch_down(self, touch):
        x = touch.x
        y = touch.y
        if self.collide_point(x, y):
            with self.canvas:
                Color(0, 1, 0)
                diameter = 30.
                Ellipse(pos=(touch.x - diameter / 2, touch.y - diameter / 2), size=(diameter, diameter))


class NetworktApp(App):
    def build(self):
        return NetworktUI()


if __name__ == '__main__':
    NetworktApp().run()
