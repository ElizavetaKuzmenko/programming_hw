__author__ = 'lizaku55'

import urllib.request as urlr
import re, bz2

codes = [line.strip() for line in open('codes.txt', encoding='utf8')]
re_title = re.compile('<title>([^<]*)</title>')
re_size = re.compile('Content-Length:.*')

#wiki_url = 'https://dumps.wikimedia.org/backup-index.html'
#page = urlr.urlopen(wiki_url)
#text = page.read().decode('utf-8')

#links = [re.findall('<a[^>]*>(.*)</a>', x, flags=re.DOTALL) for x in re.findall('<li>(.*?)</li>', text, flags=re.DOTALL)]
#codes = [x[0][:-4] for x in links if (x != [] and x[0].endswith('wiki'))]

def load_dump():
    query = input('What language are you looking for? ')
    if query in codes:
        dump_url = 'https://dumps.wikimedia.org/%swiki/latest/%swiki-latest-pages-articles.xml.bz2' % (query, query)
        dump = urlr.urlopen(dump_url)
        size = int(re_size.findall(dump.info().as_string())[0].split()[-1])
        if size > 50000000:
            answer = input('The download size is %s MB. Are you sure you want to download it (yes/no)? ' % str(size/1000000))
            if answer == 'yes':
                urlr.urlretrieve(dump_url, dump_url.split('/')[-1])
                print('Dump is downloaded!')
        else:
            urlr.urlretrieve(dump_url, dump_url.split('/')[-1])
            print('Dump is downloaded!')
    else:
        print('Your language code is not valid.')

def find_articles():
    articles = []
    articles_list = open('article_names.txt', 'w', encoding='utf-8')
    query = input('What language are you looking for? ')
    if query in codes:
        dump = bz2.BZ2File('%swiki-latest-pages-articles.xml.bz2' % query, 'r')
        #dump = open('%swiki-latest-pages-articles.xml' % query, 'r', encoding='utf-8')
        for line in dump:
            line = str(line, encoding='utf-8')
            if '<title>' in line and ':' not in line:
                article = re_title.findall(line)[0].replace('&quot;', '"')
                articles.append(article)
    for art in sorted(articles):
        articles_list.write(art + '\n')
    articles_list.close()
