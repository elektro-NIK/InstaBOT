import json
import time
from InstagramAPI import InstagramAPI
from . import key


class API:
    def __init__(self, login='', password=''):
        self._login = login if login else None
        self._password = password if password else None
        self._api = InstagramAPI(self._login, self._password) if self._login and self._password else None

    def login(self):
        self._api.login()

    def get_feed(self, filtered=True):
        feed = []
        self._api.timelineFeed()
        for item in self._api.LastJson['items']:
            if not ('type' in item) or not filtered:
                feed.append(item)
        return feed

    def get_user_post(self, limit=None, timeout=1):
        posts = []
        has_more_posts = True
        max_id = ""
        while has_more_posts and not limit:
            self._api.getSelfUserFeed(maxid=max_id)
            has_more_posts = self._api.LastJson['more_available']
            max_id = self._api.LastJson.get('next_max_id', '')
            posts.extend(self._api.LastJson['items'])
            if limit and len(posts) >= limit:
                break
            time.sleep(timeout)
        return posts[:limit] if limit else posts

    @staticmethod
    def pretty_print(json_dict):
        print(json.dumps(json_dict, indent=2))


insta = API(login=key.login, password=key.password)
insta.login()
