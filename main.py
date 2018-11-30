import json
import pickle
from datetime import datetime

from db import DB
from key import login, password
from api import API


def pretty_print_json(json_dict):
    print(json.dumps(json_dict, indent=2))


def create_tables(database):
    database.create_table('Text', (
        ('id',         'INTEGER', 'PRIMARY KEY NOT NULL'),
        ('msg',        'TEXT',    'UNIQUE NOT NULL'),
        ('link_start', 'INTEGER', 'NOT NULL'),
        ('link_end',   'INTEGER', 'NOT NULL'),
    ))

    database.create_table('Type', (
        ('id',         'INTEGER', 'PRIMARY KEY NOT NULL'),
        ('text',       'TEXT',    'UNIQUE NOT NULL'),
    ))

    database.create_table('User', (
        ('id',         'INTEGER', 'PRIMARY KEY NOT NULL'),
        ('user_id',    'INTEGER', 'UNIQUE NOT NULL'),
        ('username',   'TEXT',    'NOT NULL'),
        ('userpic',    'TEXT',    'NOT NULL'),
    ))

    database.create_table('Link', (
        ('id',         'INTEGER', 'PRIMARY KEY NOT NULL'),
        ('link_id',    'TEXT',    'UNIQUE NOT NULL'),
        ('type',       'TEXT',    'NOT NULL'),
    ))

    database.create_table('Media', (
        ('id',         'INTEGER', 'PRIMARY KEY NOT NULL'),
        ('url',        'TEXT',    'UNIQUE NOT NULL'),
    ))

    database.create_table('History', (
        ('id',         'INTEGER', 'PRIMARY KEY NOT NULL'),
        ('timestamp',  'REAL',    'NOT NULL'),
        ('text',       'INTEGER', 'REFERENCES Text  ON DELETE CASCADE NOT NULL'),
        ('type',       'INTEGER', 'REFERENCES Type  ON DELETE CASCADE NOT NULL'),
        ('user',       'INTEGER', 'REFERENCES User  ON DELETE CASCADE NOT NULL'),
        ('link',       'INTEGER', 'REFERENCES Link  ON DELETE CASCADE NOT NULL'),
        ('media',      'INTEGER', 'REFERENCES Media ON DELETE CASCADE'),
    ))


def save2file(obj, filename):
    with open(filename, 'wb') as file:
        pickle.dump(obj, file)


def load_from_file(filename):
    with open(filename, 'rb') as file:
        res = pickle.load(file)
    return res


def log(x):
    with open('log.txt', 'a') as f:
        f.write(f'{datetime.now()}: \t {x}')


def simplify_history(hist):
    types = {
        12: 'comment',
        60: 'like',
        66: 'mention',
        101: 'following'
    }
    types_ignoring = {43: 'facebook friend'}
    res = []
    for story in hist:
        try:
            story_type = story['story_type']
        except KeyError:
            log(story)
            continue
        if story_type in types:
            s = {
                'type': types[story_type],
                'timestamp': story['args']['timestamp'],
                'text': {
                    'msg': story['args']['text'],
                    'link_start': story['args']['links'][0]['start'],
                    'link_end': story['args']['links'][0]['end']
                },
                'profile': {
                    'id': story['args']['profile_id'],
                    'name': story['args']['profile_name'],
                    'image': story['args']['profile_image']
                },
                'link': {
                    'id': story['args']['links'][0]['id'],
                    'type': story['args']['links'][0]['type']
                }
            }
            try:
                s['media'] = story['args']['media'][0]['image']
            except KeyError:
                pass
            res.append(s)
        elif story_type in types_ignoring:
            pass
        else:
            log(story)
    return res


def save_history2db(database):
    max_ts = database.get_data('SELECT MAX(timestamp) FROM History')[0][0] or 0.0
    counter = 0
    for i in history:
        if max_ts < i['timestamp']:
            text = database.insert_data(
                'Text',
                ('msg', 'link_start', 'link_end'),
                (i['text']['msg'], i['text']['link_start'], i['text']['link_end'])
            )
            hist_type = database.insert_data('Type', ('text',), (i['type'],))
            user = database.insert_data(
                'User',
                ('user_id', 'username', 'userpic'),
                (i['profile']['id'], i['profile']['name'], i['profile']['image'])
            )
            link = database.insert_data('Link', ('link_id', 'type'), (i['link']['id'], i['link']['type']))
            try:
                media = database.insert_data('Media', ('url',), (i['media'],))
            except KeyError:
                media = None
            database.insert_data(
                'History',
                ('timestamp', 'text', 'type', 'user', 'link', 'media'),
                (i['timestamp'], text, hist_type, user, link, media)
            )
            counter += 1
    return counter


if __name__ == '__main__':
    insta = API(login=login, password=password)
    last_activity = insta.login()
    history = simplify_history(last_activity['new_stories'] + last_activity['old_stories'])
    db = DB('instaBot.sqlite')
    db.connect()
    create_tables(db)
    count = save_history2db(db)
    print(f'Added {count} lines to DB.')
    db.close_connection()
    insta.logout()
