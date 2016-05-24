# -*- coding: utf-8 -*-
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
from textblob_de.lemmatizers import PatternParserLemmatizer
from general import *

ONLY_PERSONS = 0
WITHOUT_PERSONS = 1
ALL_ARTICLES = 2

class XMLImporter:
    _lemmatizer = ''
    database = ''
    text_hm = set()

    def __init__(self, database):
        XMLImporter._lemmatizer = PatternParserLemmatizer()
        XMLImporter.database = database
        XMLImporter.text_hm = set()

    @staticmethod
    def read_xml_file(file):

        #results = []
        processed_pdf = set()
        tree = ET.parse(file)
        for artikel in tree.iter(tag='artikel'):
            artikel_id = ""
            artikel_text = ""
            artikel_lieferant_id = ""
            artikel_quelle_id = ""
            artikel_name = ""
            artikel_datum = ""
            artikel_seite_start = ""
            artikel_abbildung = set()
            artikel_rubrik = ""
            artikel_ressort = ""
            artikel_titel = ""

            for elem in artikel:
                for e in elem:
                    if e.tag == "artikel-pdf":
                        artikel_id = str(e.text)

                    if e.tag == "text":
                        for text in e:
                            if text.tag == "absatz":
                                artikel_text = " "+str(text.text)
                            if text.tag == "abbildung":
                                artikel_abbildung.add(str(text.text))

                    if e.tag == "titel-liste":
                        for titelliste in e:
                            if titelliste.tag == "titel":
                                artikel_titel = str(titelliste.text)
                            if titelliste.tag == "rubrik":
                                artikel_rubrik = str(titelliste.text)
                            if titelliste.tag == "ressort":
                                artikel_ressort = str(titelliste.text)
                                if artikel_ressort == 'Politik / Politik':
                                    artikel_ressort = 'Politik'

                    if e.tag == "quelle":
                        for quelle in e:
                            if quelle.tag == "lieferant_id":
                                artikel_lieferant_id = str(quelle.text)
                            if quelle.tag == "quelle-id":
                                artikel_quelle_id = str(quelle.text)
                            if quelle.tag == "name":
                                artikel_name = str(quelle.text)
                            if quelle.tag == "datum":
                                artikel_datum = str(quelle.text)
                            if quelle.tag == "seite-start":
                                artikel_seite_start = str(quelle.text)

            if artikel_id not in processed_pdf \
                    and len(artikel_titel) > 10 \
                    and 'Familienchronik' not in artikel_titel \
                    and 'SO GEHT’S WEITER' not in artikel_titel \
                    and 'WOHIN HEUTE' not in artikel_titel \
                    and 'TERMINKALENDER' not in artikel_titel\
                    and 'TERMIN-KALENDER' not in artikel_titel \
                    and 'Öffnungszeiten' not in artikel_titel\
                    and 'TERMIN- KALENDER' not in artikel_titel\
                    and artikel_text not in XMLImporter.text_hm:

                tags = combine_noun_adjectives(XMLImporter._lemmatizer.lemmatize(artikel_text))
                tags = tags.strip()
                #ignore articles without noun/adjective content
                if len(tags) > 2 and " " in tags:
                    # new_article = Artikel(artikel_id, artikel_text,
                    #                   tags,
                    #                   artikel_lieferant_id, artikel_quelle_id, artikel_name, artikel_datum,
                    #                   artikel_seite_start, artikel_abbildung, artikel_rubrik,
                    #                   artikel_ressort, artikel_titel, XMLImporter.getvector(tags, ALL_ARTICLES),
                    #                       XMLImporter.getvector(tags, ONLY_PERSONS),
                    #                       XMLImporter.getvector(tags, WITHOUT_PERSONS),
                    #                       len(artikel_text.split(" ")))
                    new_article = Artikel(artikel_id, artikel_text,
                                          tags,
                                          artikel_lieferant_id, artikel_quelle_id, artikel_name, artikel_datum,
                                          artikel_seite_start, artikel_abbildung, artikel_rubrik,
                                          artikel_ressort, artikel_titel, XMLImporter.getvector(tags, ALL_ARTICLES),
                                          {},
                                          {},
                                          len(artikel_text.split(" ")))
                    XMLImporter.database.storearticle(new_article)
                    XMLImporter.text_hm.add(artikel_text)
                    print("stored: "+new_article.titel)
                    #results.append(new_article)
                    processed_pdf.add(artikel_id)

        #return results


    @staticmethod
    def getvector(tags, mode):
        list_tags = tags.split(" ")
        hm_tags = {}

        # make sure each term in a text is called only once, if it occours multiple times,
        # simply multiply by the frequency
        for t in list_tags:
            if t in hm_tags:
                value = hm_tags[t]
                hm_tags[t] = value + 1
            else:
                hm_tags[t] = 1

        article_vector = {}
        for input in hm_tags:
            tmp_vector = XMLImporter.database.getarticlesfromwikipedia(mode, input, 25)
            for title in tmp_vector:
                if title in article_vector:
                    # in the moment only addition of the scores, maybe also try averaging of the scores
                    tmp = article_vector[title]
                    article_vector[title] = tmp + tmp_vector[title]*hm_tags[input]
                else:
                    article_vector[title] = tmp_vector[title]*hm_tags[input]
        #sorted_results = sorted(article_vector.items(), key=operator.itemgetter(1), reverse=True)
        #print(len(article_vector))
        return article_vector


class Artikel:

    def __init__(self, artikel_id, artikel_text,tags, artikel_lieferant_id, artikel_quelle_id, artikel_name, artikel_datum,
                 artikel_seite_start, artikel_abbildung, artikel_rubrik, artikel_ressort,
                 artikel_titel, artikel_vector_alle, artikel_vector_personen, artikel_vector_ohne_personen,artikel_anzahl_woerter):
        self.id = artikel_id.replace('article_pdf_', '').replace('.pdf', '')
        self.text = artikel_text
        self.tags = tags
        self.lieferanten_id = artikel_lieferant_id
        self.quellen_id = artikel_quelle_id
        self.name = artikel_name
        self.datum = artikel_datum
        self.seite = artikel_seite_start
        self.abbildung = artikel_abbildung
        self.rubrik = artikel_rubrik
        self.ressort = artikel_ressort
        self.titel = artikel_titel
        self.vector_alle = artikel_vector_alle
        self.vector_personen = artikel_vector_personen
        self.vector_ohne_personen = artikel_vector_ohne_personen
        self.anzahl_woerter = artikel_anzahl_woerter



