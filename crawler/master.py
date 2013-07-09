# coding:utf-8
import logging
import os
import logging.config
import threading
from ConfigParser import ConfigParser
from bs4 import BeautifulSoup
import varys


__author__ = 'swarm'


logging.config.fileConfig('logging.conf')
# create logger
logger = logging.getLogger('Crawler')

config_filename = os.path.join('.', 'crawler_config.ini')
config = ConfigParser()
config.read(config_filename)


def get_phone_urls():


def main():
    pass


if __name__ == '__main__':
    main()
