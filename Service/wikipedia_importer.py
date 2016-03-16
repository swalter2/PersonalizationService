import codecs
import glob
import os
import pymysql.cursors
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
from textblob_de.lemmatizers import PatternParserLemmatizer
from general import *

_lemmatizer = PatternParserLemmatizer()

persons = set()
for line in open('list_german_persons.txt', 'r'):
    line = line.replace('\n', '')
    tmp = line.split('\t')
    for t in tmp:
        persons.add(t)

print(len(persons))


connection = pymysql.connect(host='localhost',
                             user='wikipedia_new',
                             password='1234567',
                             db='wikipedia_new',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)

month = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli',
         'August', 'September', 'Oktober', 'November', 'Dezember']


def workwitharticle(article):
    try:
        tree = ET.fromstring(article)
        w_data = tree.attrib
        id = w_data.get('id')
        title = w_data.get('title')
        url = w_data.get('url')
        # url = 'https://de.wikipedia.org/wiki?curid='+id
        text = str(tree.text)

        if title.startswith('Liste') or '(Begriffsklärung)' in title or title.endswith('v. Chr.') \
                or title.endswith('0er') or title.endswith('Jahrhundert') or '.' in title or title.endswith('n. Chr.')\
                or 'Januar' in title\
                or 'Februar' in title\
                or 'März' in title\
                or 'April' in title\
                or 'Mai' in title\
                or 'Juni' in title\
                or 'Juli' in title\
                or 'August' in title\
                or 'September' in title\
                or 'Oktober' in title\
                or 'November' in title\
                or 'Dezember' in title:
            pass
        elif not title.isdigit():
            text = text[len(title)+1:]
            text = text.replace('\n',' ')
            text = text.replace('( [])',' ')
            person = '0'
            if id in persons:
                person = '1'
            text = combine_noun_adjectives(_lemmatizer.lemmatize(text))
            if len(text) > 10:
                try:
                    with connection.cursor() as cursor:
                        sql = "INSERT INTO wikipedia (id,person,title,body) VALUES (%s,%s,%s,%s);"
                        cursor.execute(sql, (id, person, title, text))
                        connection.commit()
                except:
                    pass

    except:
        pass



# Use Wikiextractor skript to
for foldername in glob.glob(os.path.join('/Users/swalter/Downloads/ESA_Deutsch/extracted/', '*')):
    for filename in glob.glob(os.path.join(foldername+'/', 'wiki_*')):
        article = ''
        for line in codecs.open(filename, 'r', 'utf-8'):
            if line.startswith('</doc>'):
                article += line
                workwitharticle(article)
                article = ''
            else:
                article += line


print('Done')
connection.close()

