from collections import Counter

""" Used for filtering nodes as to whether they should be expanded or not """


# First Level of Filtering, used to determine whether first degree of nodes will be retrieved
def filter_0(node, name_list):
    return (logical_time_zone(node) and logical_name(node, name_list))


# Second Degree of Filtering, used to determine whether second degree of nodes will be retrieved
def filter_1(node):
    return logical_distribution(node)


def logical_distribution(node):
    time_zone_list = []
    for time_zone in [n.time_zone for n in node.reference_nodes()]:
        if (time_zone is not None):
            time_zone_list.append(time_zone)
    
    # If they dont have any reference nodes with time zones, they cannot be quantified
    if(len(time_zone_list) < 1):
        return 0
    
    counts = Counter(time_zone_list).most_common(2)
    inclusive_count = 0
    for key in counts:
        inclusive_count = inclusive_count + key[1]
        
    try:
        return ((inclusive_count > len(time_zone_list) * .50) and
                (abs(counts[0][1] - counts[1][1]) / counts[0][1] < .8))
    except:
        return 0


def logical_time_zone(node):
    if node.time_zone is None:
        return False
    if 'Berlin' in node.time_zone:
        return True
    else:
        return False


def logical_name(node, name_list):
    return any(i in node.name.upper() for i in name_list)


def load_name_list_into_memory(location='static/census-derived-all-first.txt'):
    output_array = []
    with open(location) as f:
        content = f.readlines()
        for line in content:
            output_array.append(line.split(' ', 1)[0])
    return output_array

