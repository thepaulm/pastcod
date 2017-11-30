#!/usr/bin/env python

import os
import os.path


class Library(object):
    def __init__(self, path):
        self.path = path
        if not os.path.exists(self.path):
            os.mkdir(self.path)

    def podcast_dir(self, p):
        directory = self.path + '/' + p.title
        if not os.path.exists(directory):
            os.mkdir(directory)
        return directory

    def file_path(self, p, ep):
        return self.path + '/' + p.title + '/' + ep.title + '.mp3'

    def contains(self, p, ep):
        return os.path.exists(self.file_path(p, ep))
