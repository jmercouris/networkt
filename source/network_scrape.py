from twython import Twython
import configparser
import initialize

settings = configparser.ConfigParser()
settings.read('configuration.ini')

APP_KEY = settings.get('twython-configuration', 'key')
APP_SECRET = settings.get('twython-configuration', 'secret')
OAUTH_TOKEN = settings.get('twython-configuration', 'token')
OAUTH_TOKEN_SECRET = settings.get('twython-configuration', 'token_secret')
DATABASE_NAME = settings.get('database-configuration', 'database_name')


def main():
    # twitter = Twython(APP_KEY, APP_SECRET,
    #                   OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    # print(twitter.get_home_timeline())
    initialize.create_database(DATABASE_NAME)


if __name__ == "__main__":
    main()
