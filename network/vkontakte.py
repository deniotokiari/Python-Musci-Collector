# -*- coding: utf-8 -*-

from selenium import webdriver
from colorama import Fore
import requests

from utils.app_config import Config

VK_AUTH_URL = "http://api.vkontakte.ru/oauth/authorize" \
              "?client_id=%s" \
              "&scope=audio,offline" \
              "&redirect_uri=http://api.vk.com/blank.html" \
              "&display=page" \
              "&v=%s" \
              "&response_type=token"
VK_AUDIO = "https://api.vkontakte.ru/method/audio.get" \
           "?owner_id=%s" \
           "&need_user=0" \
           "&count=%d" \
           "&offset=%d" \
           "&access_token=%s"
VK_AUDIO_SEARCH = "https://api.vkontakte.ru/method/audio.search" \
                  "?q=%s" \
                  "&sort=2" \
                  "&auto_complete=1" \
                  "&access_token=%s"

VK_CONF_FILE = "vk_conf"


def validate_vk_conf():
    return Config().config["vk"]["token"]


class Vkontakte:
    token = ""
    user_id = ""

    def __init__(self, user, password, client_id):
        self.user = user
        self.password = password
        self.client_id = client_id

    def init(self):
        if validate_vk_conf():
            config = Config()

            self.token = config.config["vk"]["token"]
            self.user_id = config.config["vk"]["user_id"]
        else:
            driver = webdriver.Firefox()
            driver.get(VK_AUTH_URL % (self.client_id, "5.37"))

            user_input = driver.find_element_by_name("email")
            password_input = driver.find_element_by_name("pass")

            user_input.send_keys(self.user)
            password_input.send_keys(self.password)

            submit = driver.find_element_by_id("install_allow")
            submit.click()

            submit = driver.find_element_by_id("install_allow")
            submit.click()

            current = driver.current_url
            access_list = (current.split("#"))[1].split("&")

            access_token = (access_list[0].split("="))[1]
            expires_in = (access_list[1].split("="))[1]
            user_id = (access_list[2].split("="))[1]

            driver.close()

            print("VK: \n\ttoken = %s \n\texpires = %s \n\tuser = %s" % (access_token, expires_in, user_id))

            self.token = access_token
            self.user_id = user_id

            vk_conf = open(VK_CONF_FILE, "w")
            vk_conf.write("%s,%s" % (access_token, user_id))
            vk_conf.close()

    def search_track(self, q):
        request = requests.get(VK_AUDIO_SEARCH % (q, self.token))
        json = request.json()

        if "response" in json:
            return json["response"][1:]
        else:
            print(Fore.RED + "\tError when search url" + Fore.RESET)
            return None

    def get_tracks(self, limit, offset):
        url = VK_AUDIO % (self.user_id, limit, offset, self.token)

        print(Fore.YELLOW + "\tFetching %s" % url)

        request = requests.get(url)

        return request.json()

    def get_all_tracks(self, result=None):
        if not result:
            result = []

        response = self.get_tracks(100, len(result))
        items = response["response"][1:]

        if len(items) > 0:
            return self.get_all_tracks(result + items)
        else:
            return result
