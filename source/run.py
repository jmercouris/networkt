from graph.network_scrape import persist_user
from graph.initialize import create_database_session
from graph.initialize import Node


def main(root_user='FactoryBerlin'):
    persist_user(root_user)
    session = create_database_session()
    root_user_object = session.query(Node).filter_by(screen_name=root_user).first()
    print(root_user_object.screen_name, root_user_object.description)


if __name__ == "__main__":
    main()
