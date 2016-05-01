import configparser

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from initialize import Base


settings = configparser.ConfigParser()
settings.read('configuration.ini')

DATABASE_NAME = settings.get('database-configuration', 'database_name')

engine = create_engine(DATABASE_NAME)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# Main Function
def main(root_user='FactoryBerlin'):
    persist_graph(root_user)


def persist_graph(screen_name):
    pass

if __name__ == "__main__":
    main()
