""" Used for filtering nodes as to whether they should be expanded or not """


# First Level of Filtering, used to determine whether first degree of nodes will be retrieved
def filter_0(node):
    return logical_time_zone(node)


# Second Degree of Filtering, used to determine whether second degree of nodes will be retrieved
def filter_1(node):
    return False


def logical_distribution():
    return False


def logical_time_zone(node):
    if node.time_zone is None:
        return False
    if 'Berlin' in node.time_zone:
        return True
    else:
        return False

