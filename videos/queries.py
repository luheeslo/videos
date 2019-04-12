from uuid import uuid4, UUID

import videos.exceptions as exc


def create_video(db, title, theme):
    videos = db['videos']

    inserted_id = videos.insert_one({
        'uid': uuid4(),
        'title': title,
        'theme': theme,
        'likes': 0,
        'dislikes': 0,
    }).inserted_id

    return videos.find_one({'_id': inserted_id})


def get_video(db, uid=None, title=None, theme=None):
    videos = db['videos']
    video = None

    if uid:
        video = videos.find_one({'uid': UUID(uid)})
    elif title:
        video = videos.find_one({'title': title})
    elif theme:
        video = videos.find_one({'theme': theme})

    if not video:
        raise exc.VideoNotFound()

    return video


def set_video_like(db, uid, dislike=False):
    videos = db['videos']
    key = 'dislikes' if dislike else 'likes'
    v = get_video(db, uid=uid)
    result = videos.update_one({'uid': UUID(uid)},
                               {'$set': {key: v[key] + 1}})
    if not result.modified_count:
        raise exc.VideoNotFound()

    return v[key] + 1
