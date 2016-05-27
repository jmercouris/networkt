from kivy.app import App
from kivy.uix.settings import SettingsWithSidebar
from scrapet.settings_panel import settings_twitter_json, settings_persistence_json


class ScrapetApp(App):
    def build(self):
        self.settings_cls = SettingsWithSidebar
    
    def build_config(self, config):
        config.setdefaults('twython-configuration', {
            'key': 'key value',
            'secret': 'secret value',
            'token': 'token value',
            'token_secret': 'token secret',
        })
        config.setdefaults('persistence-configuration', {
            'database_path': '~/Documents',
            'graph_path': '~/Documents',
        })
    
    def build_settings(self, settings):
        self.use_kivy_settings = False
        settings.add_json_panel('Twitter API',
                                self.config,
                                data=settings_twitter_json)
        settings.add_json_panel('Data Persistence',
                                self.config,
                                data=settings_persistence_json)
        settings.add_json_panel('Scrape Parameters',
                                self.config,
                                data=settings_persistence_json)

if __name__ == '__main__':
    ScrapetApp().run()

