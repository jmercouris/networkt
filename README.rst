Networkt - Temporal Network Analysis
================================================================================
Networkt is a project that aims to do temporal network analysis on
digital networks. Temporal network analysis is concerned with the
content and time of messages as they traverse the network.  This type
of analysis allows answering questions about how information flows
through networks, and which are the key individuals responsible for
diffusing information (particularly innovation).  Conversely,
traditional network analysis attempts to answer similar questions, but
instead by analysis strongly concerned with the relationships between
the nodes in a network.

What's the context of this project?
--------------------------------------------------------------------------------
The context of this project is Transnational Entrepreneurship. There
is a business theory that states there are a set of individuals named
Transnational Entrepreneurs who are responsible for the diffusion of
information and innovation across national borders. An example of what
a Transnational Entrepreneur may be is an individual with two or more
distinct networks in two or more countries. That is, imagine an
individual who has a set of friends in country A and a set of friends
in country B. It is said that this individual is responsible for
spreading ideas and innovations between these countries.

What's the question you're trying to answer?
--------------------------------------------------------------------------------
A simplified explanation for what we are trying to prove is the
following: Is the "diversity" of an entrepreneur's network a moderator
for how frequently they diffusion innovation and information across
networks and borders.

To find out more please check out the /report directory where you can
find out more information about this research project and how it was
conducted.

How does your software work? What's your general approach?
--------------------------------------------------------------------------------
Our software is written in Python and designed to be easily executable
so that you can use it for tests and information gathering of your
own. Below, briefly described are the tools we use, and the process of
of our software / analysis.

Information about our setup
********************************************************************************
- We use the twitter API to gather all of our data about a network
- We use Neo4j for our network persistence to disk
- We use scikit learn for all of our network analysis and content clustering

Information about our process
********************************************************************************
#. Select a startup incubator/workspace/hotspot in a city we are
   interested in studying, find their twitter username.
#. Collect a set of followers following that startup incubator, living
   in the same city.
#. For each collected follower (F) following the startup
   incubator/workspace/hotspot, collect a sample of their network.
#. Check the sample network of (F) to see whether it qualifies them as
   a Transnational (the details qualifying a network can be found in
   the report).
#. If the follower (F) qualifies, collect a larger version of their
   network for analysis. This entails getting a larger set of their
   friends and followers.
#. Collect the last 200 tweets of every individual in the
   follower's (F) egocentric network.
#. Run content clustering on tweets within (F)'s network to determine
   how similar two tweets are. If they are similar within some
   threshold (defined in the report), label them as being about the
   same topic.
#. Finally, determine how many instances occur of a tweet traversing
   the network in such a way that the information traveled through
   our Transnational entrepreneur. That is, how often is the
   Transnational entrepreneur (F) responsible for spreading information
   between the distinct networks (networks delineated by country) they
   are part of. To do this, we see if a tweet was tweeted by the
   friend of our Transnational entrepreneur, then by the Transnational
   entrepreneur, then by a follower of the Transnational
   entrepreneur. It is important that the friend and follower tweeting
   are from two distinct networks (this helps ensure to some degree
   that the Transnational entrepreneur's follower received the
   information from the Transnational themselves. If the above was
   confusing, the diagram below may help clarify the interaction we
   are looking for.


::

   +---------------+	  +---------------+	+-----------------+
   | Person A      |   	  | Transnational |    	| Person B        |
   | Country A 	   |	  | Entrepreneur  |    	| Country B       |
   | Tweet Topic 1 +------> Tweet Topic 1 +-----> Tweet Topic 1   |
   |               |	  | Network A, B  |   	|                 |
   |               |	  |               |   	|                 |
   +---------------+	  +---------------+    	+-----------------+


How can I run your software?
--------------------------------------------------------------------------------
Please check the readme in the /source folder for all details,
including installation, execution, and how you can recreate this
project yourself.

What's the origin of the name?
--------------------------------------------------------------------------------
The name derives from 'network' + 'time (t)' - hence, networkt.
