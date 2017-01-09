Scrapet: Twitter Network Scraper Tool
================================================================================
This tool is used to gather all of the network data necessary to
perform the network analysis. The tool functions as described in the
readme in the root of this project. Additionally, a few filters are
used throughout the scraping process to guide future scraping. Their
position in the process, and roles are described below.


Filter 0
--------------------------------------------------------------------------------
This filter  involves determining whether we would like to
consider a candidate for analysis.

#. Select a startup incubator/workspace/hotspot in a city we are
   interested in studying, find their twitter username.
#. Collect a set of followers following that startup incubator, living
   in the same city.

From that set of followers, we select the ones based on:
********************************************************************************
- User is from desired city
- User has a valid friend/follower ratio without too great a disparity


Filter 1
--------------------------------------------------------------------------------
This filter involves an assessment of whether a user is a
Transnational entrepreneur.

#. For each collected follower (F) following the startup
   incubator/workspace/hotspot, collect a sample of their network.
#. Check the sample network of (F) to see whether it qualifies them as
   a Transnational (the details qualifying a network can be found in
   the report).
#. If the follower (F) qualifies, collect a larger version of their
   network for analysis. This entails getting a larger set of their
   friends and followers.

From our now smaller set of followers, we select based on:
********************************************************************************
- User is considered Transnational Entrepreneur
- User has correct distribution of Friends

Filter 2
--------------------------------------------------------------------------------
This filter concerns itself if we are interested in the content of
someone's tweets.  After the following steps we evaluate a set of
criteria.

#. Collect the last 200 tweets of every individual in the
   follower's (F) egocentric network.

From our networks, we consider which user's tweets are interesting based on:
********************************************************************************
- If they are a verified user (automatically labeled as filter 2)
- If they tweet frequently enough (accounts with less than 50 total
  tweets are not considered)
- If they have a valid follower to friend ratio
- If they avoid repeating themselves over 50% of the time
