Networkt - Source
================================================================================
Networkt is a project that aims to do temporal network analysis on
digital networks.

Requirements
--------------------------------------------------------------------------------
You will need to have the following to run this software:

- Python 3.4+
- Neo4j: https://neo4j.com/

Python Dependencies
********************************************************************************
This software requires the following to be installed:

- Twython: https://github.com/ryanmcgrath/twython
- Neomodel: https://github.com/robinedwards/neomodel
- Scikit Learn: http://scikit-learn.org/stable/
- NTLK: http://www.nltk.org/

Running The Code
--------------------------------------------------------------------------------
- Get a Twitter API Key that you can use: https://apps.twitter.com/.

- Create a configuration file in the root source directory (the
  directory that also contains this readme) named
  ``scrapet.ini``. This is where you will put your configuration of
  the scraper. An example of the configuration is outlined below:

::

  [twython-configuration]
  secret = <twitter secret goes here>
  key = <twitter key goes here>
  token_secret = <twitter token secret goes here>
  token = <twitter token goes here>

  [persistence-configuration]
  graph_path = <path to save output graph files goes here>

  [scrape-configuration]
  root_user = <twitter username of startup incubator goes here>
  root_user_follower_limit = <how many root user followers to collect>
  filter_graph_sample_limit = <sample size to test users for transnational networks>
  extended_graph_limit = <how many friends/followers to collect for individual network analysis>


- Start a Neo4j instance on your local machine or on a server, and
  then connect it with the following instructions:
  http://neomodel.readthedocs.io/en/latest/configuration.html. In
  short, this involves executing the following before executing the
  script:

::

   from neomodel import config
   config.DATABASE_URL = 'bolt://neo4j:neo4j@localhost:7687`

- Collect your data by running the following command from the root of
  this source directory: ``python -m scrapet.runner``. This enables you
  to run all of the source code as a module without adding things to
  your python path or attempting to install this software via pip.
- The scripts ``standard out`` will update you as it collects the data.
- After the collection script has executed, you can run any analysis
  you wish on the data. It is available via the Neo4j database in a
  set of relationships defined in graph/data_model.py.
- To run the standard analysis as intended for this project run the
  following command from the root of this source directory:
  ``python -m cluster.db_scan``
