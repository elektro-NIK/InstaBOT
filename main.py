import json

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


if __name__ == '__main__':
    insta = API(login=login, password=password)
    last_activity = insta.login()
    history = last_activity['new_stories'] + last_activity['old_stories']
    db = DB('instaBot.sqlite')
    db.connect()
    create_tables(db)
    insta.logout()

