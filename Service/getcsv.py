import codecs
import glob
import os
from gensim import models
from nltk import word_tokenize

import sys
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET



def workwitharticle(article):
    try:
        tree = ET.fromstring(article)
        w_data = tree.attrib
        id = w_data.get('id')
        title = w_data.get('title')
        url = w_data.get('url')
        # url = 'https://de.wikipedia.org/wiki?curid='+id
        text = str(tree.text)
        return text;
    except:
        return("")


counter = 0;
articles = [];
for foldername in glob.glob(os.path.join('/Users/swalter/Downloads/ESA_Deutsch/extracted/', '*')):
    for filename in glob.glob(os.path.join(foldername+'/', 'wiki_*')):
        article = ''
        for line in codecs.open(filename, 'r', 'utf-8'):
                if line.startswith('</doc>'):
                    article += line
                    result = workwitharticle(article)
                    if len(result)> 100:
                        articles.append(result)
                    article = ''
                    counter += 1
                else:
                    article += line


print('Done')
print(len(articles))




arglist = sys.argv

file_name = "embedings.txt"

class ArticleSentences():
    def __init__(self,article_full_texts):
        self.article_full_texts = article_full_texts

    def __iter__(self):     #iterator über die wörter im text
        for full_text in self.article_full_texts:
            yield word_tokenize(full_text)

print("Trainiere Word-Embeddings...")
articleSentences = ArticleSentences(articles)
model = models.Word2Vec(articleSentences, min_count=1, workers=2)       #arbeitet zum trainieren auf iterator, hier kann man auch noch weitere Parameter festlegen
print("Speichere trainiertes modell in %s" % file_name)
model.save(file_name)

