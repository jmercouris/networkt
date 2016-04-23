from twython import Twython
import configparser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from initialize import Base, User

settings = configparser.ConfigParser()
settings.read('configuration.ini')

APP_KEY = settings.get('twython-configuration', 'key')
APP_SECRET = settings.get('twython-configuration', 'secret')
OAUTH_TOKEN = settings.get('twython-configuration', 'token')
OAUTH_TOKEN_SECRET = settings.get('twython-configuration', 'token_secret')
DATABASE_NAME = settings.get('database-configuration', 'database_name')

engine = create_engine(DATABASE_NAME)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


def main():
    twitter = Twython(APP_KEY, APP_SECRET,
                      OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    twitter.get_home_timeline()

    instance = User(symbol='tst_usr')
    session.add(instance)
        
    # Commit Changes to the Database
    session.commit()


if __name__ == "__main__":
    main()
