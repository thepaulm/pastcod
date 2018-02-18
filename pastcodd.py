#!/usr/bin/env python3

import logging
import time

logger = logging.getLogger(__name__)
loglevel = logging.DEBUG


def init_logging():
    base_log_path = '/var/log/'
    logging.basicConfig(level=loglevel, filename=base_log_path + 'pastcodd.log',
                        format='%(asctime)s %(message)s')


init_logging()


def main():
    while True:
        logging.info("Did this go?")
        time.sleep(1)


if __name__ == '__main__':
    main()
