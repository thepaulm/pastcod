#!/usr/bin/env python


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
