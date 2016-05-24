from sklearn import svm
from sklearn.feature_extraction import DictVectorizer
from sklearn import metrics
from sklearn import cross_validation
import numpy as np
from database import Database
from general import *
from textblob_de.lemmatizers import PatternParserLemmatizer
import operator
from itertools import islice
import pickle
import sys
from feature import *

from feature_extraction import *
_lemmatizer = PatternParserLemmatizer()
host = 'localhost'
user = 'wikipedia_new'
password = '1234567'
db = 'wikipedia_new'
database = Database(host, user, password, db)
ONLY_PERSONS = 0
WITHOUT_PERSONS = 1
ALL_ARTICLES = 2
VALUE = 200
stopwords = set()
for line in open('resources/germanST.txt'):
    line = line.replace('\n','')
    stopwords.add(line)


train(database)

