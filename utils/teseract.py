# -*- coding: utf-8 -*-

from colorama import Fore

from utils.collector import Item


def canonize(source):
    stop_symbols = '.,!?:;-\n\r()\''
    stop_words = (u"the",)

    return [x for x in [y.strip(stop_symbols) for y in source.lower().split()] if x and (x not in stop_words)]


def genshingle(source):
    import binascii
    shingle_len = 1
    out = []

    for i in range(len(source) - (shingle_len - 1)):
        out.append(binascii.crc32(' '.join([x for x in source[i:i + shingle_len]]).encode('utf-8')))

    return out


def compare(source_1, source_2):
    source1 = genshingle(canonize(source_1))
    source2 = genshingle(canonize(source_2))
    same = 0

    for i in range(len(source1)):
        if source1[i] in source2:
            same += 1

    return same * 2 / float(len(source1) + len(source2)) * 100


def filter_tracks(items):
    from utils.app_config import Config

    tacks = Config().config["filter"]
    to_delete = []

    for i in range(len(items)):
        for f in tacks:
            if items[i].artist.find(f) != -1:
                to_delete.append(i)

                continue

    for index in range(len(to_delete) - 1, -1, -1):
        del items[to_delete[index]]


def filter_equals(items, equals_items):
    items_to_delete = []

    for equals in equals_items:
        items_to_append = []

        for i in equals:
            items_to_append.append(items[i])
            items_to_delete.append(i)

        items.append(Item(None, None, None, None, None, items_to_append))

    items_to_delete.sort()

    result = list(set(items_to_delete))
    result.sort(reverse=True)

    for index in result:
        del items[index]


def process(items):
    filter_tracks(items)

    print(Fore.RESET + "\n============================================")
    print("Finding similar tracks...\n")

    equals_items = []

    for i in range(0, len(items)):
        item = items[i]
        to_append = [i]

        for j in range(i + 1, len(items) - 1):
            another_item = items[j]
            title_cmp_factor = compare(item.title, another_item.title)

            if title_cmp_factor == 100:
                artist_cmp_factor = compare(item.artist, another_item.artist)

                if 80 < artist_cmp_factor <= 100:
                    txt = "\tEquals: %s - %s <%d:%s=%d:%s> %s - %s = %d%%" % (
                        item.artist,
                        item.title,
                        i,
                        item.network,
                        j,
                        another_item.network,
                        another_item.artist,
                        another_item.title,
                        title_cmp_factor
                    )

                    to_append.append(j)

                    print(txt.encode('ascii', 'ignore'))

        if len(to_append) > 1:
            equals_items.append(to_append)

    filter_equals(items, equals_items)
