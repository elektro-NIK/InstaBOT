import json
import pickle

from db import DB
from key import login, password
from api import API


def pretty_print_json(json_dict):
    print(json.dumps(json_dict, indent=2))


def create_tables(db):
    db.create_table('User', (
        ('id',        'INTEGER', 'PRIMARY KEY NOT NULL'),
        ('user_id',   'INTEGER', 'UNIQUE NOT NULL'),
        ('username',  'TEXT',    'NOT NULL'),
        ('private',   'INTEGER', 'NOT NULL'),
        ('following', 'INTEGER', 'NOT NULL'),
        ('userpic',   'TEXT',    'NOT NULL'),
    ))

    db.create_table('Media', (
        ('id',        'INTEGER', 'PRIMARY KEY NOT NULL'),
        ('media_id',  'TEXT',    'UNIQUE NOT NULL'),
        ('url',       'TEXT',    'UNIQUE NOT NULL'),
    ))

    db.create_table('Link', (
        ('id',        'INTEGER', 'PRIMARY KEY NOT NULL'),
        ('link_id',   'TEXT',    'UNIQUE NOT NULL'),
        ('text',      'TEXT',    'NOT NULL'),
    ))

    db.create_table('Type', (
        ('id',        'INTEGER', 'PRIMARY KEY NOT NULL'),
        ('name',      'TEXT',    'UNIQUE NOT NULL'),
    ))

    db.create_table('History', (
        ('id',        'INTEGER', 'PRIMARY KEY NOT NULL'),
        ('type',      'INTEGER', 'REFERENCES Type'),
        ('timestamp', 'REAL',    'NOT NULL'),
        ('text',      'TEXT',    'NOT NULL'),
        ('link',      'INTEGER', 'REFERENCES Link'),
        ('user',      'INTEGER', 'REFERENCES User'),
        ('media',     'INTEGER', 'REFERENCES Media'),
    ))


def save2file(obj, filename):
    with open(filename, 'wb') as file:
        pickle.dump(obj, file)


def load_from_file(filename):
    with open(filename, 'rb') as file:
        res = pickle.load(file)
    return res


def log(x):
    pass    # Fixme!


def simplify_history(history):
    types = {12: 'comment', 60: 'like', 101: 'following'}
    types_ignoring = {43: 'facebook friend'}
    res = []
    for story in history:
        try:
            type = story['story_type']
        except KeyError:
            log(story)
            continue
        if type in types:
            s = {
                'type': types[type],
                'text': story['args']['text'],
                'timestamp': story['args']['timestamp'],
                'profile': {
                    'id': story['args']['profile_id'],
                    'name': story['args']['profile_name'],
                    'image': story['args']['profile_image']
                },
                'link': {
                    'id': story['args']['links'][0]['id'],
                    'type': story['args']['links'][0]['type'],
                    'start': story['args']['links'][0]['start'],
                    'end': story['args']['links'][0]['end']
                }
            }
            try:
                s['media'] = story['args']['media'][0]['image']
            except KeyError:
                pass
            res.append(s)
        elif type in types_ignoring:
            pass
        else:
            log(story)
    return res


if __name__ == '__main__':
    insta = API(login=login, password=password)
    last_activity = insta.login()
    history = last_activity['new_stories'] + last_activity['old_stories']
    save2file(history, 'save_002')
    db = DB('instaBot.sqlite')
    db.connect()
    create_tables(db)
    insta.logout()

