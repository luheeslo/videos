import os
from pprint import pprint

import unittest
try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

from pyramid import testing
from pymongo import MongoClient

from .views.default import VideoViews
from .queries import create_video, get_video


'''class ViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_my_view(self):
        from .views.default import my_view
        request = testing.DummyRequest()
        info = my_view(request)
        self.assertEqual(info['project'], 'videos')


class FunctionalTests(unittest.TestCase):
    def setUp(self):
        from videos import main
        app = main({})
        from webtest import TestApp
        self.testapp = TestApp(app)

    def test_root(self):
        res = self.testapp.get('/', status=200)
        self.assertTrue(b'Pyramid' in res.body)
'''


class VideoViewTest(unittest.TestCase):

    """Test case docstring."""

    def setUp(self):
        self.database_uri = os.environ.get('DATABASE_URI_TEST')
        self.config = testing.setUp()

        db_url = urlparse(self.database_uri)

        self.db = MongoClient(
            host=db_url.hostname,
            port=db_url.port
        )['videos']

        self.v1 = {'title': 'Radiohead Lucky Live', 'theme': 'Music',
                   'likes': 2, 'dislikes': 0}
        self.v2 = {'title': 'Video1', 'theme': 'Music', 'likes': 6, 
                   'dislikes': 10}
        self.v3 = {'title': 'Video3', 'theme': 'Anime', 'likes': 0,
                   'dislikes': 0}
        self.v4 = {'title': 'Video2', 'theme': 'Entretairment',
                   'likes': 5, 'dislikes': 5}

    def request(self, post=None):
        r = testing.DummyRequest(post=post) if post else testing.DummyRequest()
        r.db = self.db
        return r

    def tearDown(self):
        self.db.drop_collection('videos')
        testing.tearDown()

    def test_index(self):
        create_video(self.db, title=self.v1['title'], theme=self.v1['theme'])
        create_video(self.db, title=self.v2['title'], theme=self.v2['theme'])
        response = VideoViews(self.request()).index()
        self.assertEqual(len(response['videos']), 2)
        for v in zip(response['videos'], [self.v1, self.v2]):
            self.assertEqual(v[0]['title'], v[1]['title'])
            self.assertEqual(v[0]['theme'], v[1]['theme'])

    def test_video_create(self):
        from videos import main
        app = main({}, mongo_uri=self.database_uri)
        from webtest import TestApp
        self.testapp = TestApp(app)
        self.v1['submit'] = True
        r = self.testapp.post('/create', params=self.v1)
        r = r.follow()
        self.assertEqual(r.status_code, 200)
        self.assertTrue(bool(get_video(self.db, title=self.v1['title'])))

    def test_themes_list_score(self):
        videos = self.db['videos']
        expected = ['Music', 'Entretairment', 'Anime']
        for v in [self.v1, self.v2, self.v3, self.v4]:
            create_video(self.db, title=v['title'], theme=v['theme'])
            v_doc = get_video(self.db, title=v['title'])
            videos.update_one({'uid': v_doc['uid']},
                              {'$set': {k: v for k, v in v.items() if k == 'likes' or k == 'dislikes'}})
        response = VideoViews(self.request()).themes()
        self.assertEqual(expected, [t for t, _ in response['themes']])
