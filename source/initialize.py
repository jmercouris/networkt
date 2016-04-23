""" Initialize the database tables, columns, etc
"""
from sqlalchemy import Column, Integer, Float, Date, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    symbol = Column(Text)


def create_database(database_name='sqlite:///data/data_store.db'):
    # Create an engine that stores data in the local directory's
    # 'sqlite:///data/data_store.db' file.
    engine = create_engine(database_name)
 
    # Create all tables in the engine. This is equivalent to "Create Table"
    # statements in raw SQL.
    Base.metadata.create_all(engine)
    print('Database {} Initialized'.format(database_name))


if __name__ == "__main__":
    create_database()


