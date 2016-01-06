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
appStoreUrl='itms://itunes.apple.com/app/id%s?mt=8'

ALBUTM_ICON = True
MAX_RESULT = 15

searchTerm = sys.argv[1:]

params = urllib.urlencode({
    'term' : searchTerm,
    'country' : u"US",
    'entity': u"software",
    'limit' : MAX_RESULT,})

data = urllib.urlopen(url, params).read()
resultData = json.loads(data)['results']

results = []

results.append(alfred.Item(title=u"Search apps with keyword \"%s\"" % "".join(searchTerm),
                           subtitle=u"Search AppStore",
                           attributes= {'uid':alfred.uid(0),
                                        'arg':u"itms://itunes.apple.com/WebObjects/MZStore.woa/wa/search?mt=8&term=%s"% searchTerm[0] },
                           icon=u"icon.png"
                           ))

for (idx,e) in enumerate(itertools.islice(resultData, MAX_RESULT)):
    if ALBUTM_ICON:
        imageurl = e['artworkUrl60']
        filepath = os.path.join(alfred.work(True), str(e['trackId'])+".png")
        if not os.path.exists(filepath):
            urllib.urlretrieve(e['artworkUrl60'], filepath)
        imageurl = filepath
    else:
        imageurl = u"icon.png"

    try:
        averageUserRating = e['averageUserRating']
    except KeyError:
        averageUserRating = u"no data"
        
    subtitle = "%s • Price: %s • Rating: %s" % (e['artistName'], e['formattedPrice'], averageUserRating)
    results.append(alfred.Item(title=e['trackName'],subtitle=subtitle,
                               attributes={'arg':appStoreUrl%e['trackId']},
                               icon=imageurl))

alfred.write(alfred.xml(results,maxresults=None))
