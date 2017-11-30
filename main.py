#!/usr/bin/env python
import yaml
import requests
import xml.etree.ElementTree as ET

from entities.podcast import Podcast
from entities.library import Library


library_file = './library.yaml'
library_path = './library'


def main():
    library = Library(library_path)

    index = yaml.load(open(library_file))
    for feed in index['podcasts']:
        feed_xml = requests.get(feed)
        tree = ET.fromstring(feed_xml.text)

        podcast = Podcast.from_rss_xml(tree)
        print("Title:\n", podcast.title)
        print()

        print("Description:\n", podcast.description)
        print()

        for i, ep in enumerate(podcast.episodes):
            print("{}: {}".format(i, ep.title))
            print("Date: ", ep.pub_date)
            print("Url: ", ep.url)

        print()

        podcast.sync(library)


if __name__ == '__main__':
    main()
