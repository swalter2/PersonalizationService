# -*- coding: utf-8 -*-

from gensim import models
from nltk import word_tokenize

import sys

model_new = models.Word2Vec.load("/Users/swalter/Downloads/embedings.txt")
model_new.most_similar(positive=['wort1','wort2'], negative=['wort3','wort4']) #addiert bzw subtrahiert wörter und macht dann kosinus-ähnlichkeit

