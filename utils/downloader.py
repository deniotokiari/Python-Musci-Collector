# -*- coding: utf-8 -*-

import urllib2
import os
import time
import random

from colorama import Fore
from network.google_music import GoogleMusic
from network.vkontakte import Vkontakte
from teseract import compare

FILE_TEMPLATE = "%s - %s.mp3"
FILE_MUSIC = "music"
ILLEGAL_CHARACTERS = '<>:"/\|?*'


def get_candidate(items):
    # vk => gm => last fm
    for item in items:
        if item.network is "vk":
            return item

    for item in items:
        if item.network is "gm":
            return item

    return items[0]


def normalize_name(name):
    return "".join(x for x in name if x not in ILLEGAL_CHARACTERS)


def to_file(url, name):
    try:
        response = urllib2.urlopen(url)
        output = open(name, "wb")
        output.write(response.read())
        output.close()
    except Exception:
        print((Fore.RED + "\tError when downloading %s" + Fore.RESET) % name)
        i = random.randint(3, 10)

        print((Fore.CYAN + "\tDownloader: sleep in %d seconds" + Fore.RESET) % i)

        time.sleep(i)


class Downloader:
    gm = None
    vk = None
    tracks_without_url = []

    def __init__(self):
        pass

    def get_gm_url(self, item):
        try:
            return self.gm.api.get_stream_url(item.track_id)
        except Exception:
            return None

    def get_vk_url(self, item):
        if self.vk is None:
            from utils.app_config import Config
            config = Config()

            self.vk = Vkontakte(config.config["vk"]["email"], config.config["vk"]["password"],
                                config.config["vk"]["app_id"])
            self.vk.init()

        search_items = self.vk.search_track("%s-%s" % (item.artist, item.title))
        url = None

        if search_items is not None:
            for search_item in search_items:
                artist = search_item["artist"]
                title = search_item["title"]

                artist_cmp_factor = compare(artist, item.artist)
                title_cmp_factor = compare(title, item.title)

                if artist_cmp_factor > 80 and title_cmp_factor > 80:
                    url = search_item["url"]

                    break

        if not url:
            i = random.randint(3, 10)

            print((Fore.CYAN + "\tVk resolver: sleep in %d seconds" + Fore.RESET) % i)

            time.sleep(i)

        return url

    def find_url(self, item):
        url = item.url

        if url:
            return url
        else:
            network = item.network

            if network is "gm":
                if self.gm is None:
                    from utils.app_config import Config
                    config = Config()

                    self.gm = GoogleMusic(config.config["gm"]["email"], config.config["gm"]["password"])
                    self.gm.init()

                url = self.get_gm_url(item)

                if url:
                    return url
                else:
                    return self.get_vk_url(item)
            elif network == "last fm":
                return self.get_vk_url(item)

    def handle_item(self, items, item):
        name = FILE_TEMPLATE % (item.artist, item.title)

        if os.path.isfile(FILE_MUSIC + os.path.sep + normalize_name(name)):
            print(Fore.GREEN + "\tFile %s exist" % name.encode('ascii', 'ignore'))

            return

        url = self.find_url(item)

        if url:
            print(Fore.YELLOW + "\t[%d/%d] Download %s - %s" % (
                items.index(item) + 1 if item in items else 0,
                len(items),
                item.artist.encode('ascii', 'ignore'),
                item.title.encode('ascii', 'ignore')))

            to_file(url, FILE_MUSIC + os.path.sep + normalize_name(name))
        else:
            self.tracks_without_url.append(item)

            print(Fore.RED + "\tUrl for %s - %s not found" % (
                item.artist.encode('ascii', 'ignore'),
                item.title.encode('ascii', 'ignore')))

    def download_all(self, items):
        print(Fore.RESET + "\n============================================")
        print("Download tracks...\n")

        if not os.path.isdir(FILE_MUSIC):
            os.makedirs(FILE_MUSIC)

        for item in items:
            if item.tracks:
                self.handle_item(items, get_candidate(item.tracks))
            else:
                self.handle_item(items, item)
