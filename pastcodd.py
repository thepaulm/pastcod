#!/usr/bin/env python

import logging

logger = logging.getLogger(__name__)
loglevel = logging.DEBUG


def init_logging():
    base_log_path = '/var/log/'
    logging.basicConfig(level=loglevel, filename=base_log_path + 'pastcodd.log',
                        format='%(asctime)s %(message)s')


init_logging()


def main():
    logging.info("Did this go?")


if __name__ == '__main__':
    main()
