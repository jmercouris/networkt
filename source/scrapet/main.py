from kivy.app import App
from kivy.uix.settings import SettingsWithSidebar
from scrapet.settings_panel import settings_twitter_json


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
    
    def build_settings(self, settings):
        self.use_kivy_settings = False
        settings.add_json_panel('Twitter',
                                self.config,
                                data=settings_twitter_json)
        # settings.add_json_panel('Panel Two',
        #                         self.config,
        #                         data=settings_json)

if __name__ == '__main__':
    ScrapetApp().run()

# ***REMOVED***
# ***REMOVED***
# ***REMOVED***
# ***REMOVED***
# ***REMOVED***

# ***REMOVED***
# ***REMOVED***
