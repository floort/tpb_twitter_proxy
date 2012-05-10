#!/usr/bin/env python

###############################################################################
# Copyright (c) 2012, Floor Terra <floort@gmail.com>
# 
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
# 
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
############################################################################### 

import random
import urlparse
import urllib
import urllib2
import twitter
import sys
import time

ACCOUNT_NAME = "@floorter" # Twitter user
CONSUMER_KEY = ""
CONSUMER_SECRET = ""
ACCESS_TOKEN_KEY = ""
ACCESS_TOKEN_SECRET = ""



def shorten_magnet(m):
    if not m.startswith("magnet:?"):
        return False
    param = m[8:]
    q = "magnet:?"
    keep = []
    keepone = []
    for p in urlparse.parse_qsl(param):
        if p[0] == "tr":
            keepone.append(p)
        elif p[0] == "dn":
            keep.append(("dn", "short"))
        elif p[0] == "xt":
            q += p[0] + "=" + p[1] + "&"
        else:
            keep.append(p)
    keep.append(random.choice(keepone))
    q += urllib.urlencode(keep)
    return q


def search(q):
    url = "http://thepiratebay.se/search/%s/0/7/0" % urllib.quote(q)
    page = urllib.urlopen(url).read()
    start = page.find("magnet:")
    end = page.find("\"", start)
    return page[start:end]




api = twitter.Api(
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
    access_token_key=ACCESS_TOKEN_KEY,
    access_token_secret=ACCESS_TOKEN_SECRET
)


while True:
    f = open("last.id")
    last = int(f.read())
    f.close()
    mentions = api.GetMentions(since_id=last)
    for m in mentions:
        magnet = search(m.text.replace("@zoekpiraat", ""))
        update_str = "@%s %s" % (m.user.screen_name, shorten_magnet(magnet))
        update = api.PostUpdate(update_str, in_reply_to_status_id=m.id)
        f = open("last.id", "w")
        f.write("%d\n" % (m.id,))
        f.close()
        print update.text
    time.sleep(30)



