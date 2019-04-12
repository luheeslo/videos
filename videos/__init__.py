import os

from pyramid.config import Configurator
try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

from pymongo import MongoClient


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    with Configurator(settings=settings) as config:
        print(urlparse(os.path.expandvars(settings['mongo_uri'])))
        db_url = urlparse(os.path.expandvars(settings['mongo_uri']))
        config.registry.db = MongoClient(
            host=db_url.hostname,
            port=db_url.port
        )

        def add_db(request):
            db = config.registry.db[db_url.path[1:]]
            if db_url.username and db_url.password:
                db.authenticate(db_url.username, db_url.password)
            return db

        config.add_request_method(add_db, 'db', reify=True)

        config.include('pyramid_jinja2')
        config.include('.routes')
        config.scan()
    return config.make_wsgi_app()
