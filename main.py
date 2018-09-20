import json
import time

from InstagramAPI import InstagramAPI

import key


class API:
    def __init__(self, login='', password=''):
        self._login = login if login else None
        self._password = password if password else None
        self._api = InstagramAPI(self._login, self._password) if self._login and self._password else None

    def login(self):
        self._api.login()
        return self._api.LastJson

    def get_feed(self, filtered=True):
        feed = []
        self._api.timelineFeed()
        for item in self._api.LastJson['items']:
            if not ('type' in item) or not filtered:
                feed.append(item)
        return feed

    def get_user_post(self, limit=None, timeout=1, sort=False):
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
        posts = sorted(posts, key=lambda k: k['like_count'], reverse=True) if sort else posts
        return posts[:limit] if limit else posts

    def get_last_activity(self):
        self._api.getRecentActivity()
        return self._api.LastJson

    def get_self_info(self):
        self._api.getSelfUsernameInfo()
        return self._api.LastJson

    def get_self_users_following(self):
        self._api.getSelfUsersFollowing()
        return self._api.LastJson

    def get_user_following(self, id):
        self._api.getUserFollowings(id)
        return self._api.LastJson

    @staticmethod
    def pretty_print(json_dict):
        print(json.dumps(json_dict, indent=2))


insta = API(login=key.login, password=key.password)
insta.login()
