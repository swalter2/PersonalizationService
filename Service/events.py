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
    stemmer = nltk.stem.snowball.GermanStemmer()

    def update_inverted_index(self, inverted_index, text, text_id):
        tokens = nltk.tokenize.WordPunctTokenizer().tokenize(text.replace('\n',' '))
        for token in tokens:
            token = token.lower()
            #if token not in string.punctuation:
            if token.isalpha() and token not in stopwords.words('german'):
                #print(token)
                stemmed_token = self.stemmer.stem(token)
                if stemmed_token in inverted_index:
                    #updates the set of the dictionary inverted_index on the position token with the id of the text
                    inverted_index[stemmed_token].add(text_id)
                else:
                    tmp = set()
                    tmp.add(text_id)
                    inverted_index[stemmed_token] = tmp

    # Function from Fabian
    def create_dictionary(self, filename):
        tree = ET.parse(filename)
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
        os.remove(filename)
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

    def get_events(self,interests):
        hm = {}
        for interest in interests:
            stemmed_interest = self.stemmer.stem(interest.lower())
            if stemmed_interest in self.inverted_index:
                for eventid in self.inverted_index[stemmed_interest]:
                    hm['event_id_'+eventid] = self.event_dict[eventid]
        return hm

    def get_raw_events(self):
        d = {}
        for eventid in list(self.event_dict):
            self.event_dict[eventid]['id'] = 'event_id_' + eventid
            d['event_id_' + eventid] = self.event_dict[eventid]
        return d

    def get_events_ids_scores(self, interests_with_scores):
        """
        :param interests_with_scores: dict with {id: {'score':<score>, 'id':<id>, 'name':<name>},...}
        :return:
        """
        d = {}

        for interest_id in interests_with_scores:
            interest = interests_with_scores[interest_id]['name']
            score = interests_with_scores[interest_id]['score']
            stemmed_interest = self.stemmer.stem(interest.lower())
            if stemmed_interest in list(self.inverted_index):
                for eventid in self.inverted_index[stemmed_interest]:
                    d['event_id_'+eventid] = {'score': (score / 5), 'id': ('event_id_'+eventid)}

        return d


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




