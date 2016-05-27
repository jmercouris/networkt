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

  
