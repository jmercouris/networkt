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
    ])


settings_scrape_json = json.dumps([
    {'type': 'string',
     'title': 'Root User',
     'desc': 'Root user/ hub of network to scrape',
     'section': 'scrape-configuration',
     'key': 'root_user'},
    
    {'type': 'numeric',
     'title': 'Root User Follower Count',
     'desc': 'How many followers from the root user to pull',
     'section': 'scrape-configuration',
     'key': 'root_user_follower_limit'},

    {'type': 'path',
     'title': 'Valid Names',
     'desc': 'File containing list of valid names',
     'section': 'scrape-configuration',
     'key': 'name_list_path'},
    
    # {'type': 'numeric',
    #  'title': 'Transnational Threshold',
    #  'desc': 'What percentage of this user follower network have to be transnational',
    #  'section': 'scrape-configuration',
    #  'key': 'transnational_percentage'},
    
    # {'type': 'numeric',
    #  'title': 'Transnational Friends',
    #  'desc': 'How many transnational friends friends',
    #  'section': 'scrape-configuration',
    #  'key': 'transnational_friend_count'},
    
    ])


settings_json = json.dumps([
    {'type': 'title',
     'title': 'example title'},
    {'type': 'bool',
     'title': 'A boolean setting',
     'desc': 'Boolean description text',
     'section': 'example',
     'key': 'boolexample'},
    {'type': 'numeric',
     'title': 'A numeric setting',
     'desc': 'Numeric description text',
     'section': 'example',
     'key': 'numericexample'},
    {'type': 'options',
     'title': 'An options setting',
     'desc': 'Options description text',
     'section': 'example',
     'key': 'optionsexample',
     'options': ['option1', 'option2', 'option3']},
    {'type': 'string',
     'title': 'A string setting',
     'desc': 'String description text',
     'section': 'example',
     'key': 'stringexample'},
    {'type': 'path',
     'title': 'A path setting',
     'desc': 'Path description text',
     'section': 'example',
     'key': 'pathexample'}])

  
