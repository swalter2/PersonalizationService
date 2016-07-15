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
    list_featurenames = set()

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
        for  s in training_features:
            for key in s:
                Learning.list_featurenames.add(key)
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

        normalized_article_ressort = ressort_mapping(article[2])

        #ressort-prior-feature
        normalized_ressort_dict_article = normalize_article_ressort_to_dict(normalized_article_ressort)

        feature.update(normalized_ressort_dict_article)
        #page prior feature
        feature.update(normalize_pages(article[3]))
        #prior-infos about user
        feature.update(user_information_vector(user))
        #user-spezific comparison of interests with text and title
        user_interest_list = []
        for interest_id in user[8].keys(): #erstelle Liste der User-Interessen für den Vergleich mit Text
            user_interest_list.append(user[8][interest_id]['name'])
        feature.update(compare_string_to_interests(article[0] + " " + article[1], user_interest_list, mode='user_specific_titel_and_text'))
        #cross-feature with ressort and normalized page
        cf_age_ressort,cf_sex_ressort,cf_edu_ressort,cf_age_page,cf_sex_page,cf_edu_page\
            = compute_cross_features(user[0],user[1],user[2],article[3],article[3])

        feature.update(cf_age_ressort)
        feature.update(cf_sex_ressort)
        feature.update(cf_edu_ressort)
        feature.update(cf_age_page)
        feature.update(cf_sex_page)
        feature.update(cf_edu_page)




        normalized_ressort_dict_user = normalize_user_ressort_ratings_to_dict(user)

        ##User X findet Ressort Y gut und Artikel Z ist aus Ressort Y (5 binaere features)
        ressort_specific_dict = user_specific_ressort_ratings(normalized_ressort_dict_user, normalized_article_ressort)
        feature.update(ressort_specific_dict)

        #User X findet Ressort Y mit Wertung Z gut und Artikel ist aus Ressort Y (25 binaere features, davon eins = 1)
        ressort_specific_dict_with_ratings = user_specific_ressort_explicit_ratings(normalized_ressort_dict_user, normalized_article_ressort)
        feature.update(ressort_specific_dict_with_ratings)

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
            tmp_list_featurenames = set()
            for s in feature:
                tmp_list_featurenames.add(s)
            print(list(Learning.list_featurenames-tmp_list_featurenames))
            print(list(tmp_list_featurenames-Learning.list_featurenames))
            print(len(Learning.list_featurenames))
            print(len(tmp_list_featurenames))
            print("Unexpected error:", sys.exc_info()[0])
            raise
            value = 0.0
        if value > 0.95 and cos > 0.0:
            return 1.0
        else:
            if cos == 0.0 and value > 0.90:
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
            user_informations[id] = Learning.database.getuserinformations(id) #die userinformations die von der DB kommen sind eine Liste
            user_informations[id].append(Learning.database.getuserinterests(id)) #die interessen sind als dict gespeichert

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

            cos_similarity = calculatesimilarity(reduced_sorted_interest_vector_hm, reduced_sorted_article_vector_hm)
            #cos = calculatesimilarity(reduced_sorted_interest_vector_hm, reduced_sorted_article_vector_hm)
            predicted_value =  Learning.prediction(cos_similarity, user, articles[article_id])
            if predicted_value > 0.0:
                results[article_id] = predicted_value;
        return results