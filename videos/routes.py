def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    # config.add_route('home', '/')
    config.add_route('index', '/')
    config.add_route('video_create', '/create')
    config.add_route('like', '/like')
    config.add_route('dislike', '/dislike')
    config.add_static_view('deform_static', 'deform:static/')
