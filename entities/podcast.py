#!/usr/bin/env python

import sys
import requests
import threading

from entities.shared import locked_print
from threading import Thread

class Episode(object):
    def __init__(self, title, pub_date, url):
        self.title = title
        self.pub_date = pub_date
        self.url = url
        self.podcast_title = None

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

    def download(self, library):
        # Careful- this guy is multithreaded ...
        
        try:
            r = requests.get(self.url, stream=True)
        except Exception as e:
            locked_print("Error accessing URL: {}. Error: {}".format(self.url, e))
        
        path = library.file_path(self)
        locked_print("Downloading {} to {}".format(self.url, path))

        try:
            with open(path, "wb") as f:
                for chunk in r.iter_content(chunk_size=100 * 1024):  # 100k per chunk
                    f.write(chunk)

                locked_print("Finished downloading", self.url)
        except Exception as e:
            locked_print("Error writing podcast episode: {}. Error: {}".format(self.url, e)) 

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
            episode = Episode.from_rss_xml(item)
            episode.podcast_title = title
            p.episodes.append(episode)

        return p

    def sync(self, library, num_recent=None):
        library.podcast_dir(self)

        for i, ep in enumerate(self.episodes):

            if num_recent is not None and i >= num_recent:
                break

            #if not library.contains(self, ep):
                #path = library.file_path(self, ep)
                #ep.download(path)
    
    def queue_episodes(self, ep_queue, library, num_recent=None):
        library.podcast_dir(self)

        for i, ep in enumerate(self.episodes):

            if num_recent is not None and i >= num_recent:
                break

            # Add only the episodes not already in the library to the queue
            if not library.contains(self, ep):
                ep_queue.put(ep)

