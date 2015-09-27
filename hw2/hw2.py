__author__ = 'lizaku55'

import urllib.request as urlr
import re

codes = [line.strip() for line in open('codes.txt', encoding='utf8')]

#wiki_url = 'https://dumps.wikimedia.org/backup-index.html'
#page = urlr.urlopen(wiki_url)
#text = page.read().decode('utf-8')

#links = [re.findall('<a[^>]*>(.*)</a>', x, flags=re.DOTALL) for x in re.findall('<li>(.*?)</li>', text, flags=re.DOTALL)]
#codes = [x[0][:-4] for x in links if (x != [] and x[0].endswith('wiki'))]
#print(codes)

query = input('What language are you looking for? ')
if query in codes:
    dump_url = 'https://dumps.wikimedia.org/%swiki/latest/%swiki-latest-pages-articles.xml.bz2' % (query, query)
    urlr.urlretrieve(dump_url, dump_url.split('/')[-1])
    #print(dump_url)
else:
    print('Your language code is not valid.')
