# -*- coding: utf-8 -*-

from textblob_de.lemmatizers import PatternParserLemmatizer
lemmatizer = PatternParserLemmatizer()

beispielsatz = "Bei der Wahl des Jahres 2012 besiegte Obama seinen republikanischen Herausforderer Mitt Romney und wurde so für eine zweite Amtszeit bestätigt."

tags = lemmatizer.lemmatize(beispielsatz)

for term, tag in tags:
    print(term,tag)