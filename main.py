#!/usr/bin/env python
import yaml
import requests
import argparse
import xml.etree.ElementTree as ET

from entities.podcast import Podcast
from entities.library import Library
from threading import Thread
from queue import Queue

library_file = './library.yaml'
library_path = './library'


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--num-recent', type=int, help="number of recent podcasts to get")
    parser.add_argument('--num-threads', default=8, type=int, help="number of threads to use for asynchronous downloading")
    return parser.parse_args()


def downloader(ep_queue, library):
    # Multithreaded: download each episode in the queue to the library
    while not ep_queue.empty():
        ep = ep_queue.get()

        ep.download(library)
        ep_queue.task_done()


def main():
    args = get_args()

    library = Library(library_path)
    thread_list = []
    ep_queue = Queue(maxsize=0)

    index = yaml.load(open(library_file))
    for feed in index['podcasts']:
        try:
            feed_xml = requests.get(feed)
        except Exception as e:
            print("Error requesting feed:", e)
        else:
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

            # Create a queue of all of the episodes for the podcast which need to be synced
            podcast.queue_episodes(ep_queue, library, args.num_recent)

    episode_count = ep_queue.qsize()
    print("Downloading {} episodes with {} threads.".format(episode_count, args.num_threads))

    # Launch our thread pool and hand them the queue
    for i in range(0, args.num_threads):
        thread_list.append(Thread(target=downloader, args=(ep_queue, library)))
        thread_list[i].daemon = False
        thread_list[i].start()

    # Hang here until the queue is emptied
    ep_queue.join()

    # Make main thread wait on all threads downloading podcasts
    for t in range(0, len(thread_list)):
        thread_list[t].join()

    print("Finished downloading {} episodes.".format(episode_count))


if __name__ == '__main__':
    main()
