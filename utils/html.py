# -*- coding: utf-8 -*-

FILE_NAME = "log.html"
HTML_TEMPLATE = "<html>" \
                "<head>" \
                "<title>Logs</title>" \
                "<link rel='stylesheet' href='style.css'>" \
                "</head>" \
                "<body>"
HTML_ITEM_TEMPLATE = "<tr><td class='counter'></td><td>%s</td><td>%s</td><td><a href='%s' target='_blank'>%s</a></td></tr>"


def print_logs(items, items_without_url):
    file_log = file(FILE_NAME, "w")
    file_log.write(HTML_TEMPLATE)
    file_log.write("<table>")

    for item in items:
        if item.tracks:
            file_log.write("<tr><td colspan='4'><hr align='center'></td></tr>")

            for i in item.tracks:
                file_log.write((HTML_ITEM_TEMPLATE %
                                (i.artist, i.title, [i.url, "#"][i.url is None], i.network)).encode('UTF-8'))
        else:
            file_log.write((HTML_ITEM_TEMPLATE %
                            (item.artist, item.title, [item.url, "#"][item.url is None], item.network)).encode('UTF-8'))

    if len(items_without_url) > 0:
        file_log.write("<tr><td colspan='4'><hr align='center'></td></tr>")
        file_log.write("<tr><td colspan='4'><h2 align='center'>Tracks without url...</h2></td></tr>")

        for item in items_without_url:
            file_log.write((HTML_ITEM_TEMPLATE %
                            (item.artist, item.title, [item.url, "#"][item.url is None], item.network)).encode('UTF-8'))

    file_log.write("</table>")
    file_log.write("</body></html>")
    file_log.close()
