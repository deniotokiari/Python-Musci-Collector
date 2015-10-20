# -*- coding: utf-8 -*-

import time

from colorama import init
from colorama import Fore

from utils import downloader
from network.vkontakte import Vkontakte
from network.last_fm import LastFm
from network.google_music import GoogleMusic
from utils.app_config import Config
from utils.collector import *
from utils.html import print_logs
from utils.teseract import process

config = Config()


def process_vk(collector):
    print("\n============================================")
    print("Vk user tracks processing:\n")

    start = time.time()
    vk = Vkontakte(config.config["vk"]["email"], config.config["vk"]["password"], config.config["vk"]["app_id"])
    vk.init()
    items = vk.get_all_tracks()

    print(Fore.RESET + "\nFetched %d tracks" % len(items))
    print("Collecting tracks...")

    collector.vk(items)

    print(Fore.CYAN + "Done in %d seconds" % (time.time() - start))


def process_last_fm(collector):
    print(Fore.RESET + "\n============================================")
    print("LastFm loved tracks processing:\n")

    start = time.time()
    last_fm = LastFm(config.config["lm"]["name"], config.config["lm"]["token"])
    items = last_fm.get_all_tracks()

    print(Fore.RESET + "\nFetched %d tracks" % len(items))
    print("Collecting tracks...")

    collector.last_fm(items)

    print(Fore.CYAN + "Done in %d seconds" % (time.time() - start))


def process_google_music(collector):
    print(Fore.RESET + "\n============================================")
    print("Google Music promoted tracks processing")

    start = time.time()
    google_music = GoogleMusic(config.config["gm"]["email"], config.config["gm"]["password"])
    google_music.init()
    items = google_music.get_all_tracks()
    # google_music.logout()

    print(Fore.RESET + "\nFetched %d tracks" % len(items))
    print("Collecting tracks...")

    collector.play_google(items)

    print(Fore.CYAN + "Done in %d seconds" % (time.time() - start))


init()

print("Starting...")

s = time.time()
storage = Collector()

process_vk(storage)
process_last_fm(storage)
process_google_music(storage)

process(storage.storage)

dl = downloader.Downloader()
dl.download_all(storage.storage)

print_logs(storage.storage, dl.tracks_without_url)

print(Fore.RESET + "\n--------------------------------------------")
print("Total tracks: %s" % len(storage.storage))
print(Fore.GREEN + "Done in %s seconds" % (time.time() - s))
