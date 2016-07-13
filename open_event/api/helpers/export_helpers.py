import json
import os
import shutil
from flask_restplus import marshal

from ..events import DAO as EventDAO, EVENT, \
    LinkDAO as SocialLinkDAO, SOCIAL_LINK
from ..microlocations import DAO as MicrolocationDAO, MICROLOCATION
from ..sessions import DAO as SessionDAO, SESSION, \
    TypeDAO as SessionTypeDAO, SESSION_TYPE
from ..speakers import DAO as SpeakerDAO, SPEAKER
from ..sponsors import DAO as SponsorDAO, SPONSOR
from ..tracks import DAO as TrackDAO, TRACK
from .non_apis import CustomFormDAO, CUSTOM_FORM


EXPORTS = [
    ('event', EventDAO, EVENT),
    ('microlocations', MicrolocationDAO, MICROLOCATION),
    ('sessions', SessionDAO, SESSION),
    ('speakers', SpeakerDAO, SPEAKER),
    ('sponsors', SponsorDAO, SPONSOR),
    ('tracks', TrackDAO, TRACK),
    ('session_types', SessionTypeDAO, SESSION_TYPE),
    ('social_links', SocialLinkDAO, SOCIAL_LINK),
    ('custom_forms', CustomFormDAO, CUSTOM_FORM)
]

# keep sync with storage.UPLOAD_PATHS
DOWNLOAD_FIEDLS = {
    'sessions': {
        'video': '/videos/session_%d',
        'audio': '/audios/session_%d',
        'slides': '/slides/session_%d'
    },
    'speakers': {
        'photo': '/images/speakers/photo_%d'
    },
    'event': {
        'logo': '/images/logo',
        'background_url': '/images/background'
    },
    'sponsors': {
        'logo': '/images/sponsors/logo_%d'
    },
    'tracks': {
        'track_image_url': '/images/tracks/image_%d'
    }
}


def export_event_json(event_id):
    """
    Exports the event as a zip on the server and return its path
    """
    # make directory
    dir_path = 'static/exports/event%d' % event_id
    if os.path.isdir(dir_path):
        shutil.rmtree(dir_path, ignore_errors=True)
    os.mkdir(dir_path)
    # save to directory
    for e in EXPORTS:
        if e[0] == 'event':
            data = marshal(e[1].get(event_id), e[2])
        else:
            data = marshal(e[1].list(event_id), e[2])
        data_str = json.dumps(data, sort_keys=True, indent=4)
        fp = open(dir_path + '/' + e[0] + '.json', 'w')
        fp.write(data_str)
        fp.close()
    # make zip
    shutil.make_archive(dir_path, 'zip', dir_path)
    return os.path.realpath('.') + '/' + dir_path + '.zip'
