from twython import Twython
import configparser

settings = configparser.ConfigParser()
settings.read('configuration.ini')

APP_KEY = settings.get('twython-configuration', 'key')
APP_SECRET = settings.get('twython-configuration', 'secret')
OAUTH_TOKEN = settings.get('twython-configuration', 'token')
OAUTH_TOKEN_SECRET = settings.get('twython-configuration', 'token_secret')


def main():
    twitter = Twython(APP_KEY, APP_SECRET,
                      OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    print(twitter.get_home_timeline())


if __name__ == "__main__":
    main()
