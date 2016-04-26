# -*- coding: utf-8 -*-
from database import Database
from textblob_de.lemmatizers import PatternParserLemmatizer
from sklearn import svm
from general import *
import operator
from itertools import islice
ONLY_PERSONS = 0
WITHOUT_PERSONS = 1
ALL_ARTICLES = 2

class Learning:
    esa = ''
    database = ''
    _lemmatizer = ''
    clf = ''
    date = ''

    def __init__(self, host, user, password, db, date):
        Learning.database = Database(host, user, password, db)
        Learning._lemmatizer = PatternParserLemmatizer()
        Learning.clf = svm.SVC(gamma=0.001, C=100.)
        Learning.article_vector_hm = {}
        Learning.date = date
        # learn model once during initialization
        #Learning.clf.fit(digits.data[:-1], digits.target[:-1])




    # is called when using this class in another function with:
    # with Learning() as learning:
    #   learning.dolearn()
    def __exit__(self, exc_type, exc_value, traceback):
        Learning.connection.close()




    @staticmethod
    def prediction(cos, user_information, artikel_id):

        return cos

    @staticmethod
    def global_learn():
        #Learning.database.deleteuserinterestvector()
        userids = Learning.database.getuserids()
        articleids = Learning.database.getarticleidsfordate(Learning.date)
        for userid in userids:
            print('learning for '+str(userid))
            results = Learning.learn({}, articleids, userid, ONLY_PERSONS)
            for articleid in results:
                score = results[articleid]
                if score > 0.0:
                    Learning.database.add_personalization_person_userarticle(userid, articleid, score)

            results = Learning.learn({}, articleids, userid, WITHOUT_PERSONS)
            for articleid in results:
                score = results[articleid]
                if score > 0.0:
                    Learning.database.add_personalization_without_person_userarticle(userid, articleid, score)

            results = Learning.learn({}, articleids, userid, ALL_ARTICLES)
            for articleid in results:
                score = results[articleid]
                if score > 0.0:
                    Learning.database.add_personalization_all_userarticle(userid, articleid, score)




    @staticmethod
    def relearn(interests, userid):
        list_article_ids = Learning.database.getarticleidswithoutdate()
        Learning.learn(interests, list_article_ids, userid)


    # extend to person ID, load from database such things like age etc
    @staticmethod
    def learn(interests, list_article_ids, userid, mode, updatedscore_hm={}):
        #information = Learning.database.getuserinterests(userid)
        interest_vector_user = Learning.database.getuserinterestvector(userid, mode, updatedscore_hm)

        sorted_interest_vector_user = sorted(interest_vector_user.items(), key=operator.itemgetter(1), reverse=True)
        reduced_sorted_interest_vector = list(islice(sorted_interest_vector_user, 100))
        reduced_sorted_interest_vector_hm = {}
        for x,y in reduced_sorted_interest_vector:
            reduced_sorted_interest_vector_hm[x] = y

        #print('size interestvector for person',userid,len(interest_vector),mode)
        #for i in information:
        #    interests.append(i)

        if len(interests)>0:

            for i in interests:
                interest_input = ""
                for term, tag in Learning._lemmatizer.lemmatize(i):
                    interest_input += " "+term
                interest_input = interest_input.strip()

                tmp_vector = Learning.database.getarticlesfromwikipedia(mode, interest_input)
                for wikipediaid in tmp_vector:
                    if wikipediaid in interest_vector_user:
                        # in the moment only addition of the scores, maybe also try averaging of the scores
                        tmp = interest_vector_user[wikipediaid]
                        interest_vector_user[wikipediaid] = tmp + tmp_vector[wikipediaid]*interests[i]
                    else:
                        interest_vector_user[wikipediaid] = tmp_vector[wikipediaid]*interests[i]

        results = {}
        for article_id in list_article_ids:
            article_vector = {}
            article_vector = Learning.database.getarticlevector(article_id, mode)
            Learning.article_vector_hm[article_id+str(mode)] = article_vector

            sorted_article_vector = sorted(article_vector.items(), key=operator.itemgetter(1),reverse=True)
            reduced_sorted_article_vector = list(islice(sorted_article_vector, 100))
            reduced_sorted_article_vector_hm = {}
            for x, y in reduced_sorted_article_vector:
                reduced_sorted_article_vector_hm[x] = y

            cos = calcualtecos(reduced_sorted_interest_vector_hm, reduced_sorted_article_vector_hm)
            results[article_id] = Learning.prediction(cos, interests, article_id)
        return results