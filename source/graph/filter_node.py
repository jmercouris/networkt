from collections import Counter
from graph.data_model import Tag
import difflib
import itertools
import neomodel
from math import ceil as ceiling
from scipy.stats import chisquare

""" Used for filtering nodes as to whether they should be expanded or not """


class Filter(object):
    """Documentation for Filter
    
    """
    def __init__(self):
        try:
            self.tag_0 = Tag(name=Tag.FILTER_0).save()
        except neomodel.exception.UniqueProperty:
            self.tag_0 = Tag.nodes.get(name=Tag.FILTER_0)
        
        try:
            self.tag_1 = Tag(name=Tag.FILTER_1).save()
        except neomodel.exception.UniqueProperty:
            self.tag_1 = Tag.nodes.get(name=Tag.FILTER_1)
        
        try:
            self.tag_2 = Tag(name=Tag.FILTER_2).save()
        except neomodel.exception.UniqueProperty:
            self.tag_2 = Tag.nodes.get(name=Tag.FILTER_2)
    
    def filter_0(self, user, time_zone, disparity_tolerance):
        """Create a Tag (StructuredNode) which we will connect with Nodes that
        meet the criteria of the first filter. The first filter
        describes any nodes that are interesting to us, which nodes we
        will draw a sample network from for analysis.
        
        :param root_user: The root_user of the network to be analyzed
        :param time_zone: The time_zone we will filter against :param
        disparity_tolerance: The percent difference between
            friends/followers tolerated
        :returns: None :rtype: None
        
        """
        for follower in user.followers:
            if (logical_time_zone(follower, time_zone) and
               valid_follower_friend_ratio(follower, disparity_tolerance)):
                self.tag_0.users.connect(follower)
    
    def filter_1(self, user):
        """Create a Tag (StructuredNode) which we will connect with Nodes that
        meet the criteria of the second filter. The scond filter
        describes any nodes that appear to have transnational networks.
        
        :param user: The user whose network to test
        :returns: None
        :rtype: None
        
        """
        if transnational_distribution(user):
            self.tag_1.users.connect(user)
    
    def filter_2(self, user):
        """Only include nodes that are valid.
        
        :param node: The node network to test
        :returns: None
        :rtype: None
        
        """
        for node in itertools.chain(user.followers, user.friends):
            if (verified(node) or (valid_follower_friend_ratio(node, 0.75) and
               valid_content_length(node) and valid_content_repetition(node, 25, 0.50))):
                node.tags.connect(self.tag_2)


def valid_content_repetition(node, max_sample_size, repetition_threshold):
    """This function takes a sample of node's tweets and sees if they are
    repeated over 50% of the time.
    
    :param node: The node to test
    :returns: Is the tested node
        repeating the same content over 50% of the time?
    :rtype: Boolean
    
    """
    # Collect max_sample_size of the first statuses
    statuses = node.statuses[:max_sample_size]
    
    # Iterate until we could not have enough nodes untested to have 50%+ repitition
    for index, status_a in enumerate(
            statuses[ceiling(max_sample_size * repetition_threshold):]):
        repetition_count = 0
        
        for status_b in statuses[index:]:
            seq = difflib.SequenceMatcher(a=status_a.text.lower(), b=status_b.text.lower())
            # If status_a and status_b are over 75% similar
            if (seq.ratio() > 0.75):
                repetition_count += 1
        
        # If any tweet is repeated more than 50% of the user's tweets, too much repetition
        if (repetition_count > len(node.statuses) * repetition_threshold):
            return False
    return True


def valid_follower_friend_ratio(node, disparity_tolerance):
    """Verify that there is a percent difference no grater than
    :disparity_tolerance: between the friends_count and the
    followers_count of a node
    
    :param node: The node to check for disparity :param
    disparity_tolerance: The tolerance for disparity expressed as a
        float between 0 and 1
    :returns: Whether the Node is within the
        tolerance for disparity
    :rtype: Boolean
    
    """
    
    if (node.friends_count == 0):
        return False
    if (node.followers_count == 0):
        return False
    
    difference = abs(node.friends_count - node.followers_count)
    average = (node.friends_count + node.followers_count) / 2
    
    if average <= 0:
        return False
    
    if (difference / average) > disparity_tolerance:
        return False
    else:
        return True


def valid_content_length(node):
    if (node.statuses_count > 50):
        return True
    else:
        return False


def verified(node):
    """Check if the Node is verified
    
    :param node: The node to test
    :returns: If the node is verified
    :rtype: boolean
    
    """
    return node.verified


def transnational_distribution(node):
    """Check the graph distribution of the node in question to make sure
    that it qualifies as transantional, we don't want it too heavily
    skewed towards one other time_zone/country
    
    :param node: The node to test to see if it's graph is transnational
    :returns: If the node has a transnationally distributed graph
    :rtype: boolean
    
    """
    time_zone_list = []
    for time_zone in [n.time_zone for n in node.friends]:
        if (time_zone is not None):
            time_zone_list.append(time_zone)
    
    # if they dont have any friends with time zones, they cannot be quantified
    if(len(time_zone_list) < 1):
        return False
    
    # collect the top 3 time_zones in their network
    counts = [c[1] for c in Counter(time_zone_list).most_common(3)]
    # cs returns tuple(Power_divergenceResult, pvalue)
    cs = chisquare(counts)
    if (cs[0] < 5 and cs[1] > 0.25):
        return True
    else:
        return False


def logical_time_zone(node, time_zone):
    """Make sure that the node in question is in a time_zone that we are
    interested in
    
    :param node: The node to test
    :param time_zone: The time_zone we want the node to be in
    :returns: If the node is within the time_zone
    :rtype: boolean
    
    """
    if node.time_zone is None:
        return False
    if time_zone in node.time_zone:
        return True
    else:
        return False
