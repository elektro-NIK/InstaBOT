from operator import itemgetter

import tz
from datetime import datetime

import django
from django.conf import settings
from django.template.loader import get_template

from db import DB


def timestamp2datetime(ts):
    return datetime.fromtimestamp(ts)


def get_text(text_id):

    return text_id


def get_type(type_id):
    return type_id


def get_user(user_id):
    return user_id


def get_link(link_id):
    return link_id


def get_media(media_id):
    return media_id


if __name__ == '__main__':
    db = DB('instaBot.sqlite')
    db.connect()
    settings.configure(
        TEMPLATES=[{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': ['.'],
            'APP_DIRS': False,
        }]
    )
    django.setup()
    t = get_template('statistic.html')
    history = db.get_data('History', ['*'])
    activities = []
    for i in history:
        user = db.get_data('User', ['*'], f"id={i[4]}")[0]
        activities.append({
            'id': i[0],
            'time': timestamp2datetime(i[1]),
            'text': db.get_data('Text', ['*'], f"id={i[2]}")[0][1],
            'type': db.get_data('Type', ['*'], f"id={i[3]}")[0][1],
            'user': {
                'username': user[2],
                'userpic': user[3]
            },
            'link': db.get_data('Link', ['*'], f"id={i[5]}")[0][1],
            'media': db.get_data('Media', ['*'], f"id={i[6]}")[0][1] if i[6] != 'None' else None,
        })
    with open('1.html', 'w') as f:
        activities = sorted(activities, key=itemgetter('time'), reverse=True)
        f.write(t.render({'activities': activities}))
    db.close_connection()
