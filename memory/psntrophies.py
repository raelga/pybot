#!/usr/bin/env python
"""
 psnthropies.py List PSN trohpies information from a PSN ID.
 Author:        Rael Garcia <self@rael.io>
 Date:          01/2017
 Tested on:     Python 3 / OS X 10.11.5
"""

from urllib import request as r
import json, re, sys

def psntrophies(psnid):
    
    url = "https://io.playstation.com/playstation/psn/public/trophies/?onlineId="
    headers = {"Referer" : "https://www.playstation.com/en-us/my/compare-game-trophies",
    "User-Agent" : "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)" }

    req = r.Request(url + psnid, None, headers)
    resp = r.urlopen(req)
    body = resp.read()
    encoding = resp.info().get_content_charset('utf-8')
    data = json.loads(body.decode(encoding))

    games = len(data['list'])
    platinum = 0
    completed = 0
    info = "Recent games played\n"

    for g in range(games):
      if g <= 5: info += "👾  " + data['list'][g]['title'] + " (" + repr(data['list'][g]['progress']) + "%)\n"
      if (data['list'][g]['progress'] == 100): completed += 1
      if (data['list'][g]['trophies']['platinum'] == 1): platinum += 1

    summary = psnid + "\n"  + repr(platinum) + " platinums (" + repr(completed) + " 100%s)"

    return (summary + "\n\n" + info)

def hear(words):
    data = re.search( r'(^|.*)trophies ([A-Za-z0-9_-]+).*', words, re.I|re.M)
    if data: return psntrophies(data.groups()[1])

    data = re.search( r'^perfil ([A-Za-z0-9_-]+).*', words, re.I|re.M)
    if data: return psntrophies(data.groups()[0])

def main(argv):
    if len(sys.argv)>1:
        print(hear(' '.join(sys.argv)))
    else:
        print('I heard nothing.')

if __name__ == "__main__":
    main(sys.argv)
