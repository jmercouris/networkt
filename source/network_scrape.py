import configparser
import time

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from initialize import Base, Node
from twython import Twython


settings = configparser.ConfigParser()
settings.read('configuration.ini')

APP_KEY = settings.get('twython-configuration', 'key')
APP_SECRET = settings.get('twython-configuration', 'secret')
OAUTH_TOKEN = settings.get('twython-configuration', 'token')
OAUTH_TOKEN_SECRET = settings.get('twython-configuration', 'token_secret')
DATABASE_NAME = settings.get('database-configuration', 'database_name')

twitter = Twython(APP_KEY, APP_SECRET,
                  OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

engine = create_engine(DATABASE_NAME)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# Main Function
def main(root_user='FactoryBerlin'):
    persist_user(root_user)
    # pull_remote_graph(root_user)
    # Show All Objects Referencing root_userp


def persist_user(screen_name):
    root_user_object = session.query(Node).filter_by(screen_name=screen_name).first()
    if (root_user_object is None):
        instance = Node(twitter.lookup_user(screen_name=screen_name)[0])
        session.add(instance)
        session.commit()


def pull_remote_graph(screen_name, scope_limit=1):
    # Collect the Root Object
    root_user_object = session.query(Node).filter_by(screen_name=screen_name).first()

    next_cursor = -1
    while(next_cursor and scope_limit):
        # Limit how many Total Friends we get data for
        scope_limit -= 1

        # Process the next Cursor set of Data
        search = twitter.get_friends_list(screen_name=screen_name,
                                          count=200, cursor=next_cursor)
        for result in search['users']:
            # args = {key: value for key, value in results.items() if key in User.__mapper__.attrs}
            instance = Node(result)
            session.add(instance)
            # Append Relationships
            instance.add_edge(root_user_object)

        # Get Next Cursor, Commit, and Sleep for next iteration
        next_cursor = search["next_cursor"]
        session.commit()
        time.sleep(65)


if __name__ == "__main__":
    main()
