import configparser

settings = configparser.ConfigParser()
settings.read('configuration.ini')

key = settings.get('twython-configuration', 'key')
secret = settings.get('twython-configuration', 'secret')
token = settings.get('twython-configuration', 'token')
token_secret = settings.get('twython-configuration', 'token_secret')


