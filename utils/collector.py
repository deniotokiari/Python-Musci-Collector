# -*- coding: utf-8 -*-


class Item:
    def __init__(self, artist, title, network, url, track_id=None, tracks=None):
        if not tracks:
            tracks = []

        self.artist = artist
        self.title = title
        self.network = network
        self.url = url
        self.track_id = track_id
        self.tracks = tracks


class Collector:
    def __init__(self):
        pass

    storage = []

    def vk(self, items):
        for item in items:
            self.storage.append(Item(item["artist"], item["title"], "vk", item["url"]))

    def last_fm(self, items):
        for item in items:
            self.storage.append(Item(item["artist"]["name"], item["name"], "last fm", None))
        '''
        for item in items:
            a = item.findAll("a")
            self.storage.append(Item(a[0].string, a[1].string, "lfm", None))
            '''

    def play_google(self, items):
        for item in items:
            self.storage.append(Item(item["artist"], item["title"], "gm", None, item["storeId"]))
