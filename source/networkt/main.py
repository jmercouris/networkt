from kivy.app import App
from kivy.uix.widget import Widget


class NetworktUI(Widget):
    pass


class NetworktApp(App):
    def build(self):
        return NetworktUI()


if __name__ == '__main__':
    NetworktApp().run()
