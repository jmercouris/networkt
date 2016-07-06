from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.settings import SettingsWithSidebar
from scrapet.settings_panel import settings_twitter_json, settings_persistence_json, settings_scrape_json
from scrapet.runner import main as main_execution
from scrapet.logger import Logger
from kivy.clock import mainthread
import _thread
import os


class LoggerGraphical(Logger):
    """Documentation for LoggerConsole
    
    """
    def __init__(self, progress_bar, text_input):
        super(LoggerGraphical, self).__init__()
        self.progress_bar = progress_bar
        self.text_input = text_input
        self.log_text = ''
    
    @mainthread
    def update_progress(self, percent_complete):
        self.progress_bar.value = percent_complete * 100
    
    # Importance is a number from 0-1
    def log_event(self, importance, text):
        self.log_text = self.log_text + '\n' + text
        self.text_input.text = self.log_text


class RootWidget(BoxLayout):
    def run(self, *args):
        self.config = App.get_running_app().config
        # Network Scrape Parameters
        APP_KEY = self.config.get('twython-configuration', 'key')
        APP_SECRET = self.config.get('twython-configuration', 'secret')
        OAUTH_TOKEN = self.config.get('twython-configuration', 'token')
        OAUTH_TOKEN_SECRET = self.config.get('twython-configuration', 'token_secret')
        DATABASE_NAME = 'sqlite:///{}/data_store.db'.format(
            self.config.get('persistence-configuration', 'database_path'))
        graph_path = self.config.get('persistence-configuration', 'graph_path')
        # Scrape Specific Configuration Details
        root_user = self.config.get('scrape-configuration', 'root_user')
        name_list_path = self.config.get('scrape-configuration', 'name_list_path')
        root_user_follower_limit = int(self.config.get('scrape-configuration', 'root_user_follower_limit'))
        filter_graph_follower_limit = int(self.config.get('scrape-configuration', 'filter_graph_follower_limit'))
        extended_graph_follower_limit = int(self.config.get('scrape-configuration', 'extended_graph_follower_limit'))
        
        parameters = (APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET, DATABASE_NAME,
                      LoggerGraphical(self.ids.progress_bar, self.ids.text_input))
        kwargs = {'root_user': root_user,
                  'root_user_follower_limit': root_user_follower_limit,
                  'extended_graph_follower_limit': extended_graph_follower_limit,
                  'filter_graph_follower_limit': filter_graph_follower_limit,
                  'name_list_path': name_list_path,
                  'graph_path': graph_path}
        
        _thread.start_new_thread(main_execution, parameters, kwargs)


class ScrapetApp(App):
    
    def get_application_config(self):
        filename = os.path.expanduser("{}/{}".format('~/.config/networkt/', 'scrapet.ini'))
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        return super(ScrapetApp, self).get_application_config(filename)
    
    def build(self):
        self.settings_cls = SettingsWithSidebar
        return RootWidget()
    
    def build_config(self, config):
        config.setdefaults('twython-configuration', {
            'key': 'key value',
            'secret': 'secret value',
            'token': 'token value',
            'token_secret': 'token secret',
        })
        config.setdefaults('persistence-configuration', {
            'database_path': '',
            'graph_path': '',
        })
        config.setdefaults('scrape-configuration', {
            'root_user': 'Root User',
            'root_user_follower_limit': '200',
            'name_list_path': '',
            'extended_graph_follower_limit': '200',
            'filter_graph_follower_limit': 200,
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
                                data=settings_scrape_json)

if __name__ == '__main__':
    ScrapetApp().run()

