"""
+ Show a simple graph showing how many people are coming from each
  country, each node's relative size indicates how many individuals
  are coming from that country, output for rendering by Gephi

+ Show a simple bar graph that shows how many people are coming from
  each country

"""
import configparser
import csv
from collections import defaultdict

from graph.data_model import Node

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

# get list of time zones from root_user's followers
time_zones = [node.time_zone for node in root_user.followers]

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

networkx.write_gml(graph, 'root_user_distribution.gml')

# output to csv ######################################################
with open('root_user_distribution.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    for time_zone, count in time_zone_dictionary.items():
        if time_zone and count:
            writer.writerow([time_zone, count])
