import logging

from wok_hooks.misc import Configuration as _Configuration

import lastfm
from datetime import datetime
from StringIO import StringIO


class Document(object):

    def __init__(self, slug, title, time, content):
        self.slug = slug
        self.title = title
        self.time = time
        self.content = content

    def save(self, content_dir):
        path = '%s%s.md' % (content_dir, self.slug)
        logging.debug('save %s' % path)
        with open(path, 'w+') as fd:
            def writeline(text):
                try:
                    fd.write(text.encode('utf8') + '\n')
                except Exception as ex:
                    logging.error(ex)
            writeline('title: %s' % self.title)
            writeline('slug: %s' % self.slug)
            writeline('type: base')
            writeline('datetime: %s' % self.time.isoformat(' '))
            writeline('---')
            writeline(self.content)


class Configuration(_Configuration):
    DEFAULTS = {'account': {'user_id': None}, 'api_key': None}

    def __init__(self, path, **kwargs):
        _Configuration.__init__(self, path, **kwargs)

        for key, value in self.DEFAULTS.items():
            if key not in self:
                self[key] = value
                self.save()


def update_lastfm_toplist(options, content_dir='./content/'):
    config = Configuration('lastfm.config')

    api = lastfm.Api(config['api_key'])
    user = api.get_user(config['account']['user_id'])

    doc = Document('last-fm-toplist', 'LastFM Toplist', datetime.now(), '')
    doc_buffer = StringIO()

    print >> doc_buffer, "\n# Artists"

    print >> doc_buffer, "\n## Top 10 of the last month\n"
    for artist in user.get_top_artists('1month')[:10]:
        print >> doc_buffer, "%s. [%s](%s) (%s playcounts)" % (artist.stats.rank, artist.name, artist.url, artist.stats.playcount)

    print >> doc_buffer, "\n## Top 10 of the last quarter\n"
    for artist in user.get_top_artists('3month')[:10]:
        print >> doc_buffer, "%s. [%s](%s) (%s playcounts)" % (artist.stats.rank, artist.name, artist.url, artist.stats.playcount)

    print >> doc_buffer, "\n## Top 10 of the last year\n"
    for artist in user.get_top_artists('12month')[:10]:
        print >> doc_buffer, "%s. [%s](%s) (%s playcounts)" % (artist.stats.rank, artist.name, artist.url, artist.stats.playcount)

    print >> doc_buffer, "\n# Albums"

    print >> doc_buffer, "\n## Top 10 of the last month\n"
    for album in user.get_top_albums('1month')[:10]:
        print >> doc_buffer, "%s. [%s](%s) - [%s](%s) (%s playcounts)" % (album.stats.rank, album.name, album.url, album.artist.name, album.artist.url, album.stats.playcount)

    print >> doc_buffer, "\n## Top 10 of the last quarter\n"
    for album in user.get_top_albums('3month')[:10]:
        print >> doc_buffer, "%s. [%s](%s) - [%s](%s) (%s playcounts)" % (album.stats.rank, album.name, album.url, album.artist.name, album.artist.url, album.stats.playcount)

    print >> doc_buffer, "\n## Top 10 of the last year\n"
    for album in user.get_top_albums('12month')[:10]:
        print >> doc_buffer, "%s. [%s](%s) - [%s](%s) (%s playcounts)" % (album.stats.rank, album.name, album.url, album.artist.name, album.artist.url, album.stats.playcount)

    doc_buffer.seek(0)
    doc.content = doc_buffer.read()
    doc.save(content_dir)

if __name__ == '__main__':
    import os
    logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s:%(message)s', level=logging.DEBUG)
    os.chdir('..')
    update_lastfm_toplist({}, '/tmp/')