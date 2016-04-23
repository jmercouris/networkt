import configparser
import time
from initialize import Base, User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from twython import Twython


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


def pull_remote_graph(scope_limit=100, screen_name='FactoryBerlin'):
    twitter = Twython(APP_KEY, APP_SECRET,
                      OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    next_cursor = -1
    while(next_cursor and scope_limit):
        # Limit how many Total Friends we get data for
        scope_limit -= 1
        
        # Process the next Cursor set of Data
        search = twitter.get_friends_list(screen_name=screen_name, count=200, cursor=next_cursor)
        for result in search['users']:
            # Check to see if Parameters Exist
            # args = {key: value for key, value in results.items() if key in User.__mapper__.attrs}
            instance = User(result)
            session.add(instance)
            
        # Get Next Cursor, Commit, and Sleep for next iteration
        next_cursor = search["next_cursor"]
        session.commit()
        time.sleep(65)

    # instance = User(symbol='tst_usr')
    # session.add(instance)
    # # Commit Changes to the Database
    # session.commit()


if __name__ == "__main__":
    pull_remote_graph()
