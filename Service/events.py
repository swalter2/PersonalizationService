# -*- coding: utf-8 -*-
import pickle
import string
import xml.etree.ElementTree as ET
import nltk
import wget
from nltk.corpus import stopwords
import datetime
import os


class Event:
    inverted_index = {}
    event_dict = {}

    @staticmethod
    def update_inverted_index(inverted_index, text, text_id):
        tokens = nltk.tokenize.WordPunctTokenizer().tokenize(text.replace('\n',' '))
        for token in tokens:
            token = token.lower()
            #if token not in string.punctuation:
            if token.isalpha() and token not in stopwords.words('german'):
                #print(token)
                if token in inverted_index:
                    #updates the set of the dictionary inverted_index on the position token with the id of the text
                    inverted_index[token].add(text_id)
                else:
                    tmp = set()
                    tmp.add(text_id)
                    inverted_index[token] = tmp

    # Function from Fabian
    def create_dictionary(self, path):
        tree = ET.parse(path)
        root = tree.getroot()

        # ist nachher dict mit {id : {'bezeichnung': <...>, 'beschreibung': <...>, 'beschreibung_lang': <...>},
        #                       id: ..., }
        event_dict = {}
        inverted_index = {}

        for event in root.iter('event'):
            id = event.attrib['id']

            titel = event.find('bezeichnung')
            beschreibung = event.find('beschreibung')
            textsystem = event.find('textsystem')
            bezeichnung_text = ''
            beschreibung_text = ''
            beschreibung_lang_text = ''
            if titel is not None:
                if titel.text is not None:
                    bezeichnung_text = titel.text

            if beschreibung is not None:
                if beschreibung.text is not None:
                    beschreibung_text = beschreibung.text

            if textsystem is not None:
                text = textsystem.find('text')
                if text is not None:
                    fassung = text.find('fassung')
                    if fassung is not None:
                        if fassung.text is not None:
                            beschreibung_lang_text = fassung.text

            if bezeichnung_text != '' and beschreibung_text != '' and beschreibung_lang_text != '':
                event_dict[id] = {}
                event_dict[id]['bezeichnung'] = bezeichnung_text
                event_dict[id]['beschreibung'] = beschreibung_text
                event_dict[id]['beschreibung_lang'] = beschreibung_lang_text
                self.update_inverted_index(inverted_index, beschreibung_text, id)
                self.update_inverted_index(inverted_index, beschreibung_lang_text, id)
        return event_dict, inverted_index

    @staticmethod
    def write_pickle_dictionary(dictionary, path):
        pickle.dump(dictionary, open(path, 'wb'))

    @staticmethod
    def load_pickle_dictionary(path):
        try:
            print('load dictionary '+path)
            return pickle.load(open(path, 'rb'))
        except IOError:
            print('did not find '+path)
            return {}

    @staticmethod
    def load_event_file():
        url = 'http://ftp.forschungsdatenmanagement.org/nw/nw_kognihome.xml'
        filename = wget.download(url)
        return filename

    def __init__(self):
        today = datetime.datetime.now()
        datum = today.strftime("%d%m%Y")
        path_inverted_index = 'resources/event_inverted_index_'+datum+'.p'
        path_event_dict = 'resources/event_dict_'+datum+'.p'

        self.event_dict = self.load_pickle_dictionary(path_event_dict)
        self.inverted_index = self.load_pickle_dictionary(path_inverted_index)
        #checks, if both are empty
        if not self.inverted_index and not self.event_dict:
            print('create new event dictionary and inverted index')
            self.event_dict, self.inverted_index = self.create_dictionary(self.load_event_file())
            self.write_pickle_dictionary(self.event_dict,path_event_dict)
            self.write_pickle_dictionary(self.inverted_index, path_inverted_index)




