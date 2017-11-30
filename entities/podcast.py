#!/usr/bin/env python

import sys
import requests


class Episode(object):
    def __init__(self, title, pub_date, url):
        self.title = title
        self.pub_date = pub_date
        self.url = url

    def __str__(self):
        return "{}: {}: {}".format(self.title, self.pub_date, self.url)

    @classmethod
    def from_rss_xml(cls, tree):
        title = tree.find('title').text.rstrip()
        pub_date = tree.find('pubDate').text
        url = None
        enclosure = tree.find('enclosure')
        if enclosure is not None:
            url = enclosure.attrib['url']
        return cls(title, pub_date, url)

    def download(self, path):
        print("download {} to {}".format(self.url, path))
        r = requests.get(self.url, stream=True)
        with open(path, "wb") as f:
            for chunk in r.iter_content(chunk_size=100 * 1024):  # 100k per chunk
                print('.', end='')
                sys.stdout.flush()
                f.write(chunk)
            print("done.")


class Podcast(object):
    def __init__(self, title, description):
        self.title = title
        self.description = description
        self.episodes = []

    def __str__(self):
        return "{}: {}".format(self.title, self.descriptio)

    @classmethod
    def from_rss_xml(cls, tree):

        # Make the podcast object
        channel = tree.find('channel')
        title = channel.find('title').text
        description = channel.find('description').text

        p = cls(title, description)

        # Add all the available episodes
        for item in channel.findall('item'):
            p.episodes.append(Episode.from_rss_xml(item))

        return p

    def sync(self, library):
        library.podcast_dir(self)

        for ep in self.episodes:
            if not library.contains(self, ep):
                path = library.file_path(self, ep)
                ep.download(path)
