import json

settings_twitter_json = json.dumps([
    {'type': 'string',
     'title': 'Key',
     'desc': 'Twitter Key',
     'section': 'twython-configuration',
     'key': 'key'},
    
    {'type': 'string',
     'title': 'Secret',
     'desc': 'Twitter Secret',
     'section': 'twython-configuration',
     'key': 'secret'},
    
    {'type': 'string',
     'title': 'Token',
     'desc': 'String description text',
     'section': 'twython-configuration',
     'key': 'token'},
    
    {'type': 'string',
     'title': 'Token Secret',
     'desc': 'Twitter token secret',
     'section': 'twython-configuration',
     'key': 'token_secret'},
    ])

settings_persistence_json = json.dumps([
    {'type': 'path',
     'title': 'Database Directory',
     'desc': 'Directory where your database will be created',
     'section': 'persistence-configuration',
     'key': 'database_path'},
    
    {'type': 'path',
     'title': 'Graph Directory',
     'desc': 'Directory where your graphs will be stored',
     'section': 'persistence-configuration',
     'key': 'graph_path'},
    
    {'type': 'path',
     'title': 'Valid Names',
     'desc': 'File containing list of valid names',
     'section': 'scrape-configuration',
     'key': 'name_list_path'},
    
    ])


settings_scrape_json = json.dumps([
    {'type': 'string',
     'title': 'Root User',
     'desc': 'Root user/hub of network to scrape (FactoryBerlin)',
     'section': 'scrape-configuration',
     'key': 'root_user'},
    
    {'type': 'numeric',
     'title': 'Root User Follower Count',
     'desc': 'FactoryBerlin -> (How many Followers)',
     'section': 'scrape-configuration',
     'key': 'root_user_follower_limit'},
    
    {'type': 'numeric',
     'title': 'Root User Filter Follower Follower Count',
     'desc': 'FactoryBerlin -> Follower -> (How many Followers)',
     'section': 'scrape-configuration',
     'key': 'filter_graph_follower_limit'},
    
    {'type': 'numeric',
     'title': 'Root User Follower  Follower Follower Count',
     'desc': 'FactoryBerlin -> Filtered Follower -> (How many Followers) (How many Friends)',
     'section': 'scrape-configuration',
     'key': 'extended_graph_follower_limit'},
    
    ])
