"""
+ Ego Centric Graph of Every Transantional

  Create gml files for every transnational

"""
import configparser
from graph.data_model import Tag

import networkx
from neomodel import config
from copy import deepcopy
import re


########################################
settings = configparser.ConfigParser()
settings.read('scrapet.ini')
# Database parameters ##################
config.DATABASE_URL = settings.get('database-configuration', 'url')
########################################

# regex to strip non alpha characters
regex = re.compile('[^a-zA-Z]')


def sanitize_dict(input_dict):
    output_dict = {}
    
    for key in input_dict:
        output_dict[regex.sub('', key)] = input_dict[key]
    
    # set of keys to be removed
    sanitize_keys = ['friends', 'followers', 'statuses', 'tags',
                     'createdat', 'description']
    for key in sanitize_keys:
        output_dict.pop(key)
    
    # clean values that cannot be represented as a string
    for key in output_dict:
        if output_dict[key] is None:
            output_dict[key] = str(output_dict[key])
    
    return output_dict


# get transnational users
tag = Tag.nodes.get(name=Tag.FILTER_1)

for node in tag.users:
    graph = networkx.DiGraph()
    graph.add_node(node.screen_name, sanitize_dict(vars(node)))
    
    for follower in node.followers:
        graph.add_node(follower.screen_name, sanitize_dict(vars(follower)))
        graph.add_edge(node.screen_name, follower.screen_name)
    
    for friend in node.friends:
        graph.add_node(friend.screen_name, sanitize_dict(vars(friend)))
        graph.add_edge(friend.screen_name, node.screen_name)
    
    networkx.write_gml(graph, 'usr_{}_graph.gml'.format(node.screen_name))
