import os
from wordcloud import WordCloud
from configparser import ConfigParser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from graph.initialize import Base, Status

# Word Cloud for All Tweets


def create_session():
    config = ConfigParser()
    config.read(os.path.expanduser('~/.config/networkt/cluster.ini'))
    DATABASE_NAME = 'sqlite:///{}/data_store.db'.format(config.get('persistence-configuration', 'database_path'))
    engine = create_engine(DATABASE_NAME)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session


if __name__ == "__main__":
    session = create_session()
    statuses = session.query(Status).all()

    documents = [i.text for i in statuses]
    text = ' '.join(documents)
    print('Documents Gathered')

    # Generate a word cloud image
    wordcloud = WordCloud().generate(text)

    # Display the generated image:
    # the matplotlib way:
    import matplotlib.pyplot as plt
    plt.imshow(wordcloud)
    plt.axis("off")
    
    # lower max_font_size
    wordcloud = WordCloud(width=2000, height=2000).generate(text)
    plt.figure(figsize=(20, 20), facecolor='k')
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.savefig('{}.png'.format('plotname'))
