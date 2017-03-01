"""Network Graph, Size of Nodes = Population from Location.

Show a simple graph showing how many people are coming from each
country, each node's relative size indicates how many individuals are
coming from that country, output for rendering by Gephi

"""
from collections import defaultdict
from neomodel import config
from graph.data_model import Node
import configparser

########################################
settings = configparser.ConfigParser()
settings.read('scrapet.ini')
# Database parameters ##################
config.DATABASE_URL = settings.get('database-configuration', 'url')
########################################

# get root user
root_user = Node.nodes.get(screen_name='FactoryBerlin')

# get list of time zones
time_zones = [node.time_zone for node in root_user.followers]
print(len(time_zones))

# count via dictionary
time_zone_dictionary = defaultdict(int)

for time_zone in time_zones:
    time_zone_dictionary[time_zone] = time_zone_dictionary[time_zone] + 1

# output data to appropriate formats
for time_zone, count in time_zone_dictionary.items():
    print('{}: {}'.format(time_zone, count))
