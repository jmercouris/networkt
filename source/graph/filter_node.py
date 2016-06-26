from collections import Counter
import difflib

""" Used for filtering nodes as to whether they should be expanded or not """


# First Level of Filtering, used to determine whether first degree of nodes will be retrieved
def filter_0(node, name_list):
    return (logical_time_zone(node) and logical_name(node, name_list))


# Second Degree of Filtering, used to determine whether second degree of nodes will be retrieved
def filter_1(node):
    return logical_distribution(node)


# Third Degree of Filtering, determine whether their tweets are of any value, or they are a spambot etc
def filter_2(node):
    # Return true for verified users
    if (verified(node)):
        return True
    # Ratio of friends to followers is insufficient
    if (not valid_follower_ratio(node)):
        return False
    # Return false for users with insufficient content
    if (not valid_content_length(node)):
        return False
    # Too much repetition in the user's content
    if (not valid_content_repetition(node)):
        return False
    return True


def valid_content_repetition(node):
    for status_a in node.statuses:
        # Start at -1 because the algorithm will count the original tweet as matching
        repetition_count = -1
        for status_b in node.statuses:
            seq = difflib.SequenceMatcher(a=status_a.text.lower(), b=status_b.text.lower())
            if (seq.ratio() > .75):
                repetition_count = repetition_count + 1
        # If any tweet is repeated more than 50% of the user's tweets, too much repetition
        if (repetition_count > len(node.statuses) * .5):
            return False
    return True


def valid_follower_ratio(node):
    if (node.friends_count <= 0):
        return False
    if (node.followers_count / node.friends_count > 0.1):
        return True
    else:
        return False


def valid_content_length(node):
    if (len(node.statuses) > 50):
        return True
    else:
        return False


def verified(node):
    if (node.verified):
        return True
    else:
        return False


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

