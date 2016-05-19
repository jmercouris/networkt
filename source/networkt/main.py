from kivy.app import App
from kivy.graphics import Color, Ellipse
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.properties import StringProperty
from kivy.clock import Clock


class NetworktUI(Widget):
    def change_text(self):
        self.ids.messages.text = 'LOL'
    
    def update(self, dt):
        pass


class ScrollableLabel(ScrollView):
    text = StringProperty('')


class Network(Widget):
    def on_touch_down(self, touch):
        x = touch.x
        y = touch.y
        if self.collide_point(x, y):
            with self.canvas:
                Color(0, 1, 0)
                diameter = 30.
                Ellipse(pos=(touch.x - diameter / 2, touch.y - diameter / 2), size=(diameter, diameter))
        else:
            return False


class NetworktApp(App):
    def build(self):
        networktUI = NetworktUI()
        Clock.schedule_interval(networktUI.update, 1.0 / 60.0)
        return networktUI


if __name__ == '__main__':
    NetworktApp().run()
