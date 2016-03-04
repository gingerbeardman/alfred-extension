# -*- coding: utf-8 -*-
#
# Jaemok Jeong, 2013. 3. 27.

import itertools
import json
import re
import urllib
import alfred
import os

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

url = 'http://itunes.apple.com/search'

ALBUM_ICON = True
MAX_RESULT = 15
COUNTRY = u'GB'
CURRENCY_SYMBOL = u'£'

searchTerm = sys.argv[1:]

params = urllib.urlencode({
    'term' : searchTerm,
    'country' : COUNTRY,
    'media': u'music',
    'entity': u'album',
    'app': u'itunes',
    'uo': u'4',
    'limit' : MAX_RESULT,})

data = urllib.urlopen(url, params).read()
resultData = json.loads(data)['results']

results = []

results.append(alfred.Item(title=u"Search iTunes for albums matching \"%s\"" % "".join(searchTerm),
                           subtitle=u"Search iTunes",
                           attributes= {'uid':alfred.uid(0),
                                        'arg':u"itms://itunes.apple.com/WebObjects/MZStore.woa/wa/search?term=%s"% searchTerm[0] },
                           icon=u"icon.png"
                           ))

for (idx,e) in enumerate(itertools.islice(resultData, MAX_RESULT)):
    if ALBUM_ICON:
        imageurl = e['artworkUrl60']
        filepath = os.path.join(alfred.work(True), str(e['collectionId'])+".png")
        if not os.path.exists(filepath):
            urllib.urlretrieve(e['artworkUrl60'], filepath)
        imageurl = filepath
    else:
        imageurl = u"icon.png"

    try:
        collectionPrice = e['collectionPrice']
        if collectionPrice < 0:
            collectionPrice = u'Album Only'
        else:
            collectionPrice = CURRENCY_SYMBOL + str(e['collectionPrice'])
    except KeyError:
        collectionPrice = u'?'

    itmsLink = e['collectionViewUrl'].replace('https://','itms://') + u'&app=itunes'

    # subtitle = "%s • %s" % (e['artistName'], formatKind)
    subtitle = "%s • %s • %s" % (e['artistName'], e['collectionType'], collectionPrice)
    results.append(alfred.Item(title=e['collectionName'],subtitle=subtitle,
                               attributes={'arg':itmsLink},
                               icon=imageurl))

alfred.write(alfred.xml(results,maxresults=None))
