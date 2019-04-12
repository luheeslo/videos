import colander
import deform.widget

from pyramid.view import view_config
import pyramid.httpexceptions as exc

from videos.queries import create_video, get_video, set_video_like


# @view_config(route_name='home', renderer='../templates/mytemplate.jinja2')
# def my_view(request):
#    return {'project': 'videos'}


class VideoPage(colander.MappingSchema):
    title = colander.SchemaNode(colander.String())
    theme = colander.SchemaNode(colander.String())


class VideoViews(object):

    """Docstring for VideoViews. """

    def __init__(self, request):
        self.request = request

    @property
    def video_form(self):
        schema = VideoPage()
        return deform.Form(schema, buttons=('submit',))

    @property
    def reqts(self):
        return self.video_form.get_widget_resources()

    @view_config(route_name='index', renderer='../templates/index.jinja2')
    def index(self):
        cursor = self.request.db['videos'].find({})
        return dict(videos=[video for video in cursor])

    @view_config(route_name='video_create', renderer='../templates/video_create.jinja2')
    def video_create(self):
        form = self.video_form.render()

        if 'submit' in self.request.params:
            controls = self.request.POST.items()
            try:
                appstruct = self.video_form.validate(controls)
            except deform.ValidationFailure as e:
                return dict(form=e.render())

            create_video(self.request.db, title=appstruct['title'],
                         theme=appstruct['theme'])

            url = self.request.route_url('index')
            return exc.HTTPFound(url)

        return dict(form=form)

    @view_config(route_name='like', renderer='json')
    def like(self):
        uid = self.request.json_body['uid']
        if self.request.method == 'POST':
            return {'likes': set_video_like(self.request.db, uid)}
        else:
            raise exc.HTTPForbidden(403)

    @view_config(route_name='dislike', renderer='json')
    def dislike(self):
        uid = self.request.json_body['uid']
        if self.request.method == 'POST':
            return {'dislikes': set_video_like(self.request.db, uid,
                                               dislike=True)}
        else:
            raise exc.HTTPForbidden(403)

    @view_config(route_name='themes', renderer='../templates/themes.jinja2')
    def themes(self):
        cursor = self.request.db['videos'].find({})
        themes = {}
        for v in cursor:
            if not themes.get(v['theme']):
                themes[v['theme']] = {'thumbs_up': 0, 'thumbs_down': 0}
            themes[v['theme']]['thumbs_up'] += v['likes']
            themes[v['theme']]['thumbs_down'] += v['dislikes']
        return dict(themes=sorted(themes.items(),
                                  key=lambda t: t[1]['thumbs_up'] - (t[1]['thumbs_down']/2),
                                  reverse=True))
