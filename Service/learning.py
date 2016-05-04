# -*- coding: utf-8 -*-
from database import Database
from textblob_de.lemmatizers import PatternParserLemmatizer
from sklearn import svm
from sklearn.feature_extraction import DictVectorizer
from general import *
import operator
from itertools import islice
import pickle
import numpy as np
from feature import *

ONLY_PERSONS = 0
WITHOUT_PERSONS = 1
ALL_ARTICLES = 2
VECTOR_SIZE = 500

class Learning:
    esa = ''
    database = ''
    _lemmatizer = ''
    clf = ''
    date = ''
    ressort_list = ''

    def __init__(self, host, user, password, db, date):
        Learning.database = Database(host, user, password, db)
        Learning._lemmatizer = PatternParserLemmatizer()
        Learning.article_vector_hm = {}
        Learning.date = date
        Learning.ressort_list = Learning.database.get_ressort_list()
        #load data and learn model vor svm
        Learning.clf = svm.SVC(kernel='linear', C=0.1, probability=True)
        training_features = pickle.load(open("resources/training_features.p", "rb"))
        training_annotations = pickle.load(open("resources/training_features_annotations.p", "rb"))
        vec = DictVectorizer()
        feature_vectorized = vec.fit_transform(training_features)
        X = np.array(feature_vectorized.toarray())
        y = np.array(training_annotations)
        Learning.clf.fit(X, y)




    # is called when using this class in another function with:
    # with Learning() as learning:
    #   learning.dolearn()
    def __exit__(self, exc_type, exc_value, traceback):
        Learning.connection.close()

    def close(self):
        try:
            Learning.database.close()
        except:
            pass

    @staticmethod
    def prediction(cos, user, article):
        feature = {}
        feature.update(normalize_article_ressort_to_dict(article[2], Learning.ressort_list))
        feature.update(normalize_pages(article[3]))
        feature.update(user_information_vector(user))
        vec = DictVectorizer()
        value = 0
        try:
            feature_vectorized = vec.fit_transform(feature)
            X = np.array(feature_vectorized.toarray())
            result_prediction = Learning.clf.predict_proba(X)[0]
            #result_prediction[0] probability to be annotated as 0
            # result_prediction[1] probability to be annotated as 1
            value = float(result_prediction[1])
        except:
            print('error in learning')
            value = 0.0
        if value > 0.7 and cos > 0.0:
            return 1.0
        else:
            if cos == 0.0 and value > 0.7:
                return value

        #default
        return cos

    @staticmethod
    def global_learn():
        #Learning.database.deleteuserinterestvector()
        userids = Learning.database.getuserids()
        articleids = Learning.database.getarticleidsfordate(Learning.date)

        user_informations = {}
        for id in userids:
            user_informations[id] = Learning.database.getuserinformations(id)

        article_informations = {}
        for id in articleids:
            article_informations[id] = Learning.database.getarticleinformations(id)


        for userid in userids:
            print('learning for '+str(userid))
            # results = Learning.learn({}, articleids, userid, ONLY_PERSONS, user_informations[userid],article_informations)
            # for articleid in results:
            #     score = results[articleid]
            #     if score > 0.0:
            #         Learning.database.add_personalization_person_userarticle(userid, articleid, score)
            #
            # results = Learning.learn({}, articleids, userid, WITHOUT_PERSONS, user_informations[userid],article_informations)
            # for articleid in results:
            #     score = results[articleid]
            #     if score > 0.0:
            #         Learning.database.add_personalization_without_person_userarticle(userid, articleid, score)

            results = Learning.learn({}, articleids, userid, ALL_ARTICLES, user_informations[userid],article_informations)
            for articleid in results:
                score = results[articleid]
                if score > 0.0:
                    Learning.database.add_personalization_all_userarticle(userid, articleid, score)




    #@staticmethod
    #def relearn(interests, userid):
    #    list_article_ids = Learning.database.getarticleidswithoutdate()
    #    Learning.learn(interests, list_article_ids, userid, ALL_ARTICLES, )


    # extend to person ID, load from database such things like age etc
    @staticmethod
    def learn(interests, list_article_ids, userid, mode, user, articles):
        interest_vector_user = Learning.database.getuserinterestvector(userid, mode)
        if len(interests)>0:

            for i in interests:
                interest_input = ""
                for term, tag in Learning._lemmatizer.lemmatize(i):
                    interest_input += " "+term
                interest_input = interest_input.strip()
                tmp_vector = Learning.database.getinterestvectorforterm(interest_input,mode)
                if len(tmp_vector)==0:
                    tmp_vector = Learning.database.getarticlesfromwikipedia(mode, interest_input)
                    for wikipediaid in tmp_vector:
                        if wikipediaid in interest_vector_user:
                            # in the moment only addition of the scores, maybe also try averaging of the scores
                            tmp = interest_vector_user[wikipediaid]
                            interest_vector_user[wikipediaid] = tmp + tmp_vector[wikipediaid]*float(interests[i])
                        else:
                            if float(interests[i]) > 0.1:
                                interest_vector_user[wikipediaid] = (tmp_vector[wikipediaid]+0.0)*float(interests[i])
                else:
                    for wikipediaid in tmp_vector:
                        if wikipediaid in interest_vector_user:
                            interest_vector_user[wikipediaid] = interest_vector_user[wikipediaid]*float(interests[i])
                        else:
                            interest_vector_user[wikipediaid] = tmp_vector[wikipediaid] * float(interests[i])
        sorted_interest_vector_user = sorted(interest_vector_user.items(), key=operator.itemgetter(1), reverse=True)
        reduced_sorted_interest_vector = list(islice(sorted_interest_vector_user, VECTOR_SIZE))
        reduced_sorted_interest_vector_hm = {}
        for x, y in reduced_sorted_interest_vector:
            reduced_sorted_interest_vector_hm[x] = y

        results = {}
        for article_id in list_article_ids:
            article_vector = {}
            article_vector = Learning.database.getarticlevector(article_id, mode)
            #Learning.article_vector_hm[article_id+str(mode)] = article_vector

            sorted_article_vector = sorted(article_vector.items(), key=operator.itemgetter(1),reverse=True)
            reduced_sorted_article_vector = list(islice(sorted_article_vector, VECTOR_SIZE))
            reduced_sorted_article_vector_hm = {}
            for x, y in reduced_sorted_article_vector:
                reduced_sorted_article_vector_hm[x] = y

            cos = calcualtecos(reduced_sorted_interest_vector_hm, reduced_sorted_article_vector_hm)
            predicted_value =  Learning.prediction(cos, user, articles[article_id])
            if predicted_value > 0.0:
                results[article_id] = predicted_value;
        return results