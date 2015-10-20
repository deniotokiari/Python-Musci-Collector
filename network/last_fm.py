# -*- coding: utf-8 -*-

import requests
from colorama import Fore

LAST_FM_API_ROOT = "http://ws.audioscrobbler.com/2.0/"
LAST_FM_LOVED_TRACKS = LAST_FM_API_ROOT + "?method=user.getLovedTracks" \
                                          "&api_key=%s" \
                                          "&limit=%d" \
                                          "&page=%d" \
                                          "&format=json" \
                                          "&user=%s"
LAST_FM_LOVED_TRACKS_URL = "http://www.last.fm/user/%s/loved?page=%d"


class LastFm:
    def __init__(self, user, api_key):
        self.user = user
        self.api_key = api_key

    def get_tracks(self, limit, page):
        url = LAST_FM_LOVED_TRACKS % (self.api_key, limit, page, self.user)

        print(Fore.YELLOW + "\tFetching %s" % url)

        request = requests.get(url)

        return request.json()

    def get_all_tracks(self, result=None, page=1):
        if not result:
            result = []

        response = self.get_tracks(50, page)
        items = response["lovedtracks"]["track"]

        if len(items) > 0:
            return self.get_all_tracks(result + items, page + 1)
        else:
            return result


''' just plain page parsing
    def get_all_tracks(self, page, items):
        soup = BeautifulSoup(requests.get(LAST_FM_LOVED_TRACKS_URL % (self.user, page), "html5lib").text)

        pages = soup.find("li", {"class": "pages"}).string.split()
        current = pages[1]
        total = pages[3]

        tracks = soup.findAll("td", {"class": "chartlist-name"})

        if current == total:
            return items + tracks
        else:
            return self.get_all_tracks(page + 1, items + tracks)
'''
