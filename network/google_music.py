# -*- coding: utf-8 -*-

from gmusicapi import Mobileclient


class GoogleMusic:
    api = None

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def init(self):
        api = Mobileclient()
        api.login(self.email, self.password, Mobileclient.FROM_MAC_ADDRESS)

        self.api = api

    def get_all_tracks(self):
        tracks = self.api.get_promoted_songs()

        '''for track in tracks:
            try:
                song_id = track["storeId"]
                self.api.get_stream_url(song_id)
                track["url"] = song_id
            except Exception:
                track["url"] = None'''

        return tracks

    def logout(self):
        if self.api is not None:
            self.api.logout()
