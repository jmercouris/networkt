import numpy as np

""" Used for filtering nodes as to whether they should be expanded or not """


# First Level of Filtering, used to determine whether first degree of nodes will be retrieved
def filter_0(node):
    return (logical_time_zone(node) and logical_name(node))


# Second Degree of Filtering, used to determine whether second degree of nodes will be retrieved
def filter_1(node):
    return logical_distribution(node)


def logical_distribution(node):
    print([n.screen_name for n in node.reference_nodes()])
    return False


def logical_time_zone(node):
    if node.time_zone is None:
        return False
    if 'Berlin' in node.time_zone:
        return True
    else:
        return False


def logical_name(node):
    return True
