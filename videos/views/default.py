import colander
import deform.widget

from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
import pyramid.httpexceptions as exc


videos = [
        {'title': 'Radiohead Lucky Live', 'theme': 'Music', 'uid': 100,
         'likes': 0, 'dislikes': 0},
        {'title': 'DOIS ANOS DE METEORO #meteoro.doc ', 
         'theme': 'Entertainment', 'uid': 101, 'likes': 0, 'dislikes': 0},
        {'title': 'Example ', 'theme': 'Example', 'uid': 102, 
         'likes': 0, 'dislikes': 0},
]


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
        return dict(videos=videos)

    @view_config(route_name='video_create', renderer='../templates/video_create.jinja2')
    def video_create(self):
        form = self.video_form.render()

        if 'submit' in self.request.params:
            controls = self.request.POST.items()
            try:
                appstruct = self.video_form.validate(controls)
            except deform.ValidationFailure as e:
                return dict(form=e.render())

            last_uid = int(sorted(videos, key=lambda i: i['uid'])[-1]['uid'])
            new_uid = str(last_uid + 1)
            videos.append(dict(
                uid=new_uid, title=appstruct['title'],
                theme=appstruct['theme'], likes=0, deslikes=0,
            ))

            url = self.request.route_url('index')
            return HTTPFound(url)

        return dict(form=form)

    @view_config(route_name='like', renderer='json')
    def like(self):
        if self.request.method == 'POST':
            v = next(video for video in videos if video['uid'] == self.request.json_body['uid'])
            v['likes'] += 1
            return {'likes': v['likes']}
        else:
            raise exc.HTTPForbidden(403)

    @view_config(route_name='dislike', renderer='json')
    def dislike(self):
        if self.request.method == 'POST':
            v = next(video for video in videos if video['uid'] == self.request.json_body['uid'])
            v['dislikes'] += 1
            return {'dislikes': v['dislikes']}
        else:
            raise exc.HTTPForbidden(403)
