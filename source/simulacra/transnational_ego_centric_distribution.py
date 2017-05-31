"""
+ Ego Centric Graph of Every Transantional

+ Show a simple graph showing how many people are coming from each
  country, each node's relative size indicates how many individuals
  are coming from that country, output for rendering by Gephi

  Create gml files for every transnational

"""
import configparser
from graph.data_model import Tag

import networkx
from neomodel import config
from collections import defaultdict

########################################
settings = configparser.ConfigParser()
settings.read('scrapet.ini')
# Database parameters ##################
config.DATABASE_URL = settings.get('database-configuration', 'url')
########################################


# get transnational users
tag = Tag.nodes.get(name=Tag.FILTER_1)

for node in tag.users:
    # get list of time zones from root_user's followers
    time_zones_follow = [node.time_zone for node in node.followers]
    time_zones_friend = [node.time_zone for node in node.friends]
    
    # count via dictionary
    time_zone_dictionary_follow = defaultdict(int)
    time_zone_dictionary_friend = defaultdict(int)
    
    # count how many members are in each time zone
    for time_zone in time_zones_follow:
        time_zone_dictionary_follow[time_zone] = time_zone_dictionary_follow[time_zone] + 1
    
    # count how many members are in each time zone
    for time_zone in time_zones_friend:
        time_zone_dictionary_friend[time_zone] = time_zone_dictionary_follow[time_zone] + 1
    
    # output to graph ####################################################
    graph = networkx.Graph()
    graph.add_node(node.screen_name)

    for time_zone, count in time_zone_dictionary_follow.items():
        if time_zone and count:
            graph.add_node(time_zone, {'count': count})
            graph.add_edge(node.screen_name, time_zone)
    
    for time_zone, count in time_zone_dictionary_friend.items():
        if time_zone and count:
            graph.add_node(time_zone, {'count': count})
            graph.add_edge(time_zone, node.screen_name)
    
    networkx.write_gml(graph, '{}_user_distribution.gml'.format(node.screen_name))
