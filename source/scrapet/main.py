from kivy.app import App
from kivy.uix.settings import SettingsWithSidebar
from scrapet.settings_panel import settings_json


class ScrapetApp(App):
    def build(self):
        self.settings_cls = SettingsWithSidebar
    
    def build_config(self, config):
        config.setdefaults('example', {
            'boolexample': True,
            'numericexample': 10,
            'optionsexample': 'option2',
            'stringexample': 'some_string',
            'pathexample': '~/'})
    
    def build_settings(self, settings):
        settings.add_json_panel('Panel name',
                                self.config,
                                data=settings_json)

if __name__ == '__main__':
    ScrapetApp().run()
