#!/usr/bin/env python

import os
import os.path
import requests.utils

def escape(s):
    return requests.utils.quote(s, safe=' #:')


class Library(object):
    def __init__(self, path):
        self.path = path
        if not os.path.exists(self.path):
            os.mkdir(self.path)

    def podcast_dir(self, p):
        directory = self.path + '/' + escape(p.title)
        if not os.path.exists(directory):
            os.mkdir(directory)
        return directory

    def file_path(self, ep):
        return self.path + '/' + escape(ep.podcast_title) + '/' + escape(ep.title) + '.mp3'

    def contains(self, p, ep):
        return os.path.exists(self.file_path(ep))
