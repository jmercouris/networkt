"""
+ Create a "network graph" featuring only transnational entrepreneuers
  within this graph show relative populations, eg. how many are from
  France, Berlin, etc

"""
import configparser
import csv
from collections import defaultdict

from graph.data_model import Node
from graph.data_model import Tag

import networkx
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

# output to graph ####################################################
graph = networkx.Graph()
graph.add_node(root_user.screen_name)

for time_zone, count in time_zone_dictionary.items():
    if time_zone and count:
        graph.add_node(time_zone, {'count': count})
        graph.add_edge(root_user.screen_name, time_zone)

networkx.write_gml(graph, 'transnational_user_distribution.gml')

# output to csv ######################################################
with open('transnational_user_distribution.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    for time_zone, count in time_zone_dictionary.items():
        if time_zone and count:
            writer.writerow([time_zone, count])
