'''
Created on 21.06.2013

@author: steffen
'''

import logging
from misc import Configuration as _Configuration

DEFAULTS = {'pod': '',
            'user': ''}

from activitystreams import PostActivity, NoteObject
from activitystreams.atom import make_activities_from_feed
import urllib2
import xml.etree.ElementTree
import re

import os

from timeline import Post as TimelineUpdate

class Configuration(_Configuration):

    def __init__(self, path, **kwargs):
        _Configuration.__init__(self, path, **kwargs)

        for key, value in DEFAULTS.items():
            if key not in self:
                self[key] = value
                self.save()


class DiasporaNote(TimelineUpdate):

    TITLE_CHAR_BLACKLIST = ['[', '!', '*', ':']

    def __init__(self, base_object, time, pod, user):
        assert isinstance(base_object, NoteObject)
        slug = base_object.id.replace('https://%s/' % pod, pod + '-').replace('/', '-').replace('_', '-').replace('.', '-')
        title = base_object.name
        for char in DiasporaNote.TITLE_CHAR_BLACKLIST:
            title = title.replace(char, '')
        url = base_object.url
        content = base_object.content

        # fix awful mix of html and markdown
        content = re.sub(r'<.*?>', '', content)

        TimelineUpdate.__init__(self, slug, title, url, time, content)

        self.actions.append(('show diaspora', url))


def add_diaspora_posts_to_microblog(content_dir = './content/timeline/'):
    config = Configuration('diaspora.config')
    url = '%spublic/%s.atom' % ('https://%s/' % (config['pod']), config['user'])
    response = urllib2.urlopen(url)
    contents = response.read()
    xml_tree = xml.etree.ElementTree.fromstring(contents)
    xml_tree.getroot = lambda: xml_tree
    activities = make_activities_from_feed(xml_tree)
    for activity in activities:
        try:
            if isinstance(activity, PostActivity):
                if isinstance(activity.object, NoteObject):
                    note = DiasporaNote(activity.object, activity.time, config['pod'], config['user'])
                    note.save(content_dir)
                else:
                    logging.info('unexpected post object')
            else:
                logging.info('unknwon diaspora activity verb %s' % activity.verb)
        except Exception as ex:
            print ex

if __name__ == '__main__':
    logging.basicConfig(format = '%(asctime)s %(levelname)s %(name)s:%(message)s', level = logging.DEBUG)
    add_diaspora_posts_to_microblog('/tmp/')
