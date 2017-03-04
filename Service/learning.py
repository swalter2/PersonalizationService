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
import matplotlib.pyplot as plt
import os
from datetime import datetime

DEBUG = False
ESA_SCORES = []
SVM_SCORES = []
RELEVANCES = []

GENERAL_SCORE = []

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
    def prediction(cos, user_informations, article, alpha = 0.25, beta = 0.25, z_norm=True):
        feature = {}

        personalization_level = user_informations[8]
        if personalization_level == 'low':
            alpha = beta = 1.5
        elif personalization_level == 'medium':
            alpha = beta = 2.5
        elif personalization_level == 'high':
            alpha = beta = 3.5

        normalized_article_ressort = ressort_mapping(article[2])

        #ressort-prior-feature
        normalized_ressort_dict_article = normalize_article_ressort_to_dict(normalized_article_ressort)

        feature.update(normalized_ressort_dict_article)
        #page prior feature
        page = article[3]
        feature.update(normalize_pages(page))
        #prior-infos about user
        feature.update(user_information_vector(user_informations))
        #user-spezific comparison of interests with text and title
        user_interest_list = []
        for interest_id in user_informations[9].keys(): #erstelle Liste der User-Interessen für den Vergleich mit Text
            user_interest_list.append(user_informations[9][interest_id]['name'])
        feature.update(compare_string_to_interests(article[0] + " " + article[1], user_interest_list, mode='user_specific_titel_and_text'))
        #cross-feature with ressort and normalized page
        cf_age_ressort,cf_sex_ressort,cf_edu_ressort,cf_age_page,cf_sex_page,cf_edu_page\
            = compute_cross_features(user_informations[0], user_informations[1], user_informations[2], article[3], article[3])

        feature.update(cf_age_ressort)
        feature.update(cf_sex_ressort)
        feature.update(cf_edu_ressort)
        feature.update(cf_age_page)
        feature.update(cf_sex_page)
        feature.update(cf_edu_page)




        normalized_ressort_dict_user = normalize_user_ressort_ratings_to_dict(user_informations)

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

        relevance = 1 / float(page)         #inverse of the page
        esa_score = cos
        svm_score = value

        if z_norm:
            #normalize the scores
            normalized_relevance = z_normalization(relevance, mean = 0.16947266884534248, var = 0.07322013147086222)            #these values were precomputed
            normalized_esa_score = z_normalization(esa_score, mean = 0.0009855744806407337, var = 7.961933559635215e-05)
            normalized_svm_score = z_normalization(svm_score, mean = 0.5833671193911723, var = 0.05558054791068003)

            score = (1 - alpha - beta) * normalized_relevance + alpha * normalized_esa_score + beta * normalized_svm_score
        else:
            score = (1 - alpha - beta) * relevance + alpha * esa_score + beta * svm_score

        return score, normalized_relevance, normalized_esa_score, normalized_svm_score


    @staticmethod
    def global_learn():
        print("Starting global_learn")
        #Learning.database.deleteuserinterestvector()
        userids = Learning.database.getuserids()
        #if DEBUG:
         #   articleids = Learning.database.getarticleidsfordate(datetime.strptime("09052016", "%d%m%Y"))
        #else:
        articleids = Learning.database.getarticleidsfordate(Learning.date)

        article_informations = {}
        if DEBUG: print("list_article_ids = {} for date {}".format(articleids,Learning.date))

        for id in articleids:
            article_informations[id] = Learning.database.getarticleinformations(id)

        user_informations = {}
        for userid in userids:
            print("Learning for User {}".format(userid))
            user_informations[userid] = Learning.database.getuserinformations(userid) #die userinformations die von der DB kommen sind eine Liste
            user_informations[userid].append(Learning.database.getuserinterests(userid)) #die interessen sind als dict gespeichert

            results = Learning.learn({}, articleids, userid, ALL_ARTICLES, user_informations[userid], article_informations)
            for articleid in results:
                score = results[articleid]
                try:
                    if score > 0.000001:
                        # print("L\tInserting {}:{}:{} into DB...".format(userid,articleid,score))
                        Learning.database.add_personalization_all_userarticle(userid, articleid, score)
                except:
                    pass
                    #happens only if none value is given.
        # analyze_score_distribution(ESA_SCORES, "ESA_SCORES")
        # analyze_score_distribution(SVM_SCORES, "SVM_SCORES")
        # analyze_score_distribution(RELEVANCES, "RELEVANCES")
        # analyze_score_distribution(GENERAL_SCORE, "GENERAL")


        # for userid in userids:
        #     print('learning for '+str(userid))
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



    @staticmethod
    def single_learn(userid):
        #rticleids = Learning.database.getarticleidsfordate(Learning.date)
        articleids = Learning.database.getarticleidswithoutdate()


        user_informations = {}
        user_informations[userid] = Learning.database.getuserinformations(userid)  # die userinformations die von der DB kommen sind eine Liste
        user_informations[userid].append(Learning.database.getuserinterests(userid))  # die interessen sind als dict gespeichert

        article_informations = {}
        for id in articleids:
            article_informations[id] = Learning.database.getarticleinformations(id)


        print('learning for ' + str(userid))
        results = Learning.learn({}, articleids, userid, ALL_ARTICLES, user_informations[userid],article_informations)
        for articleid in results:
            score = results[articleid]
            Learning.database.add_personalization_all_userarticle(userid, articleid, score)


    # extend to person ID, load from database such things like age etc
    @staticmethod
    def learn(interests, list_article_ids, userid, mode, user_informations, articles):
        interest_vector_user = Learning.database.getuserinterestvector(userid, mode)        #get all interests for a user
        if len(interests)>0:

            for i in interests:     #iterate over interests
                interest_input = ""
                for term, tag in Learning._lemmatizer.lemmatize(i):     #concatenate interests
                    interest_input += " "+term
                interest_input = interest_input.strip()
                tmp_vector = Learning.database.getinterestvectorforterm(interest_input,mode)    #get presaved esa_vec for concatenated interests
                if len(tmp_vector)==0:      #if no wikipediaarticles were saved for given interests
                    tmp_vector = Learning.database.getarticlesfromwikipedia(mode, interest_input)   #get new esa_vec
                    for wikipediaid in tmp_vector:
                        if wikipediaid in interest_vector_user:     #if wiki_id already in the interest_vector of the user
                            # in the moment only addition of the scores, maybe also try averaging of the scores
                            tmp = interest_vector_user[wikipediaid]
                            interest_vector_user[wikipediaid] = tmp + tmp_vector[wikipediaid]*float(interests[i])     #add new score to the old score
                        else:       #if wiki_id not in user_vector
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
            predicted_value, relevance, esa_score, svm_score =  Learning.prediction(cos_similarity, user_informations, articles[article_id])
            results[article_id] = predicted_value;
            if DEBUG: print(predicted_value, relevance, esa_score, svm_score)
            # ESA_SCORES.append(esa_score)
            # SVM_SCORES.append(svm_score)
            # RELEVANCES.append(relevance)
            # GENERAL_SCORE.append(predicted_value)

        # print(ESA_SCORES[0:100])
        # print(SVM_SCORES[0:100])
        # print(RELEVANCES[0:100])
        # print(GENERAL_SCORE[0:100])
        # quit()
        return results

def analyze_score_distribution(arr, filename):
    print("Plotting histogram for {}".format(filename))
    if not "plots" in os.listdir("."):
        os.mkdir("./" + "plots")
    mean = np.mean(arr)
    var = np.var(arr)
    plt.clf()
    plt.title("mean = {}, var = {}".format(mean,var))
    plt.hist(arr, bins=50)
    plt.savefig("plots/" + filename + ".png")
   # print(arr)
    #print("{}:\tMean = {}\tVar = {}".format(filename,np.mean(arr),np.var(arr)))

def z_normalization(x, mean, var):
    z = (x - mean) / var
    return z