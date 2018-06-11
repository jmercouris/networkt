"""
+ Create a "network graph" featuring only transnational entrepreneuers
  within this graph show relative populations, eg. how many are from
  France, Berlin, etc

"""
from scipy.stats import skew
import configparser
from collections import defaultdict

from graph.data_model import Node, Tag

from neomodel import config


########################################
settings = configparser.ConfigParser()
settings.read('scrapet.ini')
# Database parameters ##################
config.DATABASE_URL = settings.get('database-configuration', 'url')
########################################

# get root user
root_user = Node.nodes.get(screen_name='FactoryBerlin')

# get transnational users
tag = Tag.nodes.get(name=Tag.FILTER_1)

# get list of time zones from root_user's followers
time_zones = [node.time_zone for node in tag.users]

# count via dictionary
time_zone_dictionary = defaultdict(int)

# count how many members are in each time zone
for time_zone in time_zones:
    time_zone_dictionary[time_zone] = time_zone_dictionary[time_zone] + 1

time_zone_histogram_data = []

for time_zone, count in time_zone_dictionary.items():
    time_zone_histogram_data.append(count)

# create a single dimensional array with each timezone acting as a histogram bucket
print(time_zone_histogram_data)

# calculate skewness
print(skew(time_zone_histogram_data))
