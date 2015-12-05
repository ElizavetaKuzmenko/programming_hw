__author__ = 'lizaku55'

# links = [re.findall('<a[^>]*>(.*)</a>', x, flags=re.DOTALL) for x in re.findall('<li>(.*?)</li>',
# text, flags=re.DOTALL)]
# codes = [x[0][:-4] for x in links if (x != [] and x[0].endswith('wiki'))]


def load_dump():
    query = input('What language are you looking for? ')
    if query in codes:
        dump_url = 'https://dumps.wikimedia.org/%swiki/latest/%swiki-latest-pages-articles.xml.bz2' % (query, query)
        dump = urlr.urlopen(dump_url)
        size = int(re_size.findall(dump.info().as_string())[0].split()[-1])
        if size > 50000000:
            answer = input('The download size is %s MB. Do you want to download it (yes/no)? ' % str(size/1000000))
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
        # dump = open('%swiki-latest-pages-articles.xml' % query, 'r', encoding='utf-8')
        for line in dump:
            line = str(line, encoding='utf-8')
            if '<title>' in line and ':' not in line:
                article = re_title.findall(line)[0].replace('&quot;', '"')
                articles.append(article)
    for art in sorted(articles):
        articles_list.write(art + '\n')
    articles_list.close()


def read_articles():
    query = input('What language are you looking for? ')
    if query in codes:
        freq_dic = {}
        d = open('freq_dic.json', 'a')
        wiki_table = open('%s_wiki_table.csv' % query, 'w')
        wiki_table.write('Название статьи\tСколько в ней ссылок\tКоличество слов\n')
        dump = bz2.BZ2File('%swiki-latest-pages-articles.xml.bz2' % query, 'r')
        # dump = open('%swiki-latest-pages-articles.xml' % query, 'r', encoding='utf-8')
        article = ''
        for line in dump:
            line = str(line, encoding='utf-8')
            article += line
            if '</page>' in line:
                title = re_title.findall(article)[0].replace('&quot;', '"')
                if ':' not in title:
                    links = re_links.findall(article)
                    text = re_clean1.sub('', re_text.findall(article)[0]).replace("''", '')
                    text = re_clean2.sub('', text)
                    text = re_clean3.sub('', text).replace('#REDIRECT', '').replace('#Redirect', '').replace("'''", '')
                    text = re_clean4.sub('', text)
                    text = re_clean5.sub('', text)
                    text = stop_symb.sub('', text)
                    words = [word for word in text.split() if not (word == '|-' or word == '-|' or word == '|' or
                                                                   '#' in word or '|' in word or '-' in word or
                                                                   word == ':' or word == '/' or word == '—')]
                    for word in words:
                        try:
                            freq_dic[word] += 1
                        except:
                            freq_dic[word] = 1
                        if len(freq_dic) == 10000:
                            d.write(json.dumps(freq_dic, ensure_ascii=False) + '\n')
                            freq_dic = {}
                    wiki_table.write(title + '\t' + str(len(links)) + '\t' + str(len(words)) + '\n')
                article = ''
        wiki_table.close()
        d.close()
        res_freq = {}
        for line in open('freq_dic.json', 'r'):
            line = json.loads(line.strip())
            for word in line:
                if word in res_freq:
                    res_freq[word] += line[word]
                else:
                    res_freq[word] = line[word]
        fr = open('frequency_list.csv', 'w', encoding='utf8')
        for k in sorted(res_freq, key=lambda w: -res_freq[w]):
            fr.write(k + '\t' + str(res_freq[k]) + '\n')
        fr.close()

    else:
        print('Your language code is not valid.')


def read_articles_db():
    query = input('What language are you looking for? ')
    if query in codes:
        base = sqlite3.connect('%s_frequency.db' % query)
        c = base.cursor()
        c.execute('''CREATE TABLE frequency_list (word, frequency)''')
        # c.execute('''CREATE TABLE wikipedia (title, links, words)''')
        dump = bz2.BZ2File('%swiki-latest-pages-articles.xml.bz2' % query, 'r')
        # dump = open('%swiki-latest-pages-articles.xml' % query, 'r', encoding='utf-8')
        article = ''
        for line in dump:
            line = str(line, encoding='utf-8')
            article += line
            if '</page>' in line:
                title = re_title.findall(article)[0].replace('&quot;', '"')
                if ':' not in title:
                    links = re_links.findall(article)
                    text = re_clean1.sub('', re_text.findall(article)[0]).replace("''", '')
                    text = re_clean2.sub('', text)
                    text = re_clean3.sub('', text).replace('#REDIRECT', '').replace('#Redirect', '').replace("'''", '')
                    text = re_clean4.sub('', text)
                    text = re_clean5.sub('', text)
                    text = stop_symb.sub('', text)
                    words = [word for word in text.split() if not (word == '|-' or word == '-|' or word == '|' or
                                                                   '#' in word or '|' in word or '-' in word or
                                                                   word == ':' or word == '/' or word == '—')]
                    for word in words:
                        word = word.lower()
                        c.execute('SELECT frequency FROM frequency_list WHERE word=?', (word,))
                        freq = c.fetchone()
                        if freq is None:
                            c.execute('INSERT INTO frequency_list VALUES (?,?)', (word, 1))
                        else:
                            c.execute('UPDATE frequency_list SET frequency = ? WHERE word = ?', (freq[0] + 1, word))
                            # c.execute('SELECT * FROM frequency_list WHERE word=?', (word,))
                            # print(c.fetchone())
                    # data = (title, len(links), len(words))
                    # print(data)
                    # base.execute('INSERT INTO wikipedia VALUES (?,?,?)', data)
                article = ''
        base.commit()
        base.close()
    else:
        print('Your language code is not valid.')

if __name__ == '__main__':
    read_articles_db()