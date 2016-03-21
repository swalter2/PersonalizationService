from database import Database
import operator
from textblob_de.lemmatizers import PatternParserLemmatizer
from sklearn import svm
from general import *

class Learning:
    esa = ''
    database = ''
    _lemmatizer = ''
    clf = ''
    article_vector_hm = ''
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
        userids = Learning.database.getuserids()
        articleids = Learning.database.getarticleidsfordate(Learning.date)
        for userid in userids:
            print('learning for userid:'+str(userid))
            results = Learning.learn([], articleids, userid)
            for articleid in results:
                score = results[articleid]
                if score > 0.0:
                    Learning.database.adduserarticlescore(userid, articleid, score)



    # extend to person ID, load from database such things like age etc
    @staticmethod
    def learn(interests, list_article_ids, person_id):
        mode = 2
        information = Learning.database.getuserinterests(person_id)
        interest_vector = {}

        for i in information:
            interests.append(i)

        for i in interests:
            input = ""
            for term, tag in Learning._lemmatizer.lemmatize(i):
                input += " "+term

            tmp_vector = Learning.database.getarticlesfromwikipedia(mode, input[1:])
            for wikipediaid in tmp_vector:
                if wikipediaid in interest_vector:
                    # in the moment only addition of the scores, maybe also try averaging of the scores
                    tmp = interest_vector[wikipediaid]
                    interest_vector[wikipediaid] = tmp + tmp_vector[wikipediaid]
                else:
                    interest_vector[wikipediaid] = tmp_vector[wikipediaid]
        results = {}
        for article_id in list_article_ids:
            article_vector = {}
            if article_id+str(mode) in Learning.article_vector_hm:
                article_vector = Learning.article_vector_hm[article_id+str(mode)]
            else:
                article_vector = Learning.database.getarticlevector(article_id, mode)
                Learning.article_vector_hm[article_id+str(mode)] = article_vector

            #sorted_results = sorted(interest_vector.items(), key=operator.itemgetter(1), reverse=True)

            cos = calcualtecos(interest_vector, article_vector)
            results[article_id] = Learning.prediction(cos, interests, article_id)
        return results