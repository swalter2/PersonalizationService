import pymysql.cursors
from esa import ESA
from database import Database
import operator
from textblob_de.lemmatizers import PatternParserLemmatizer

class Learning:
    esa = ''
    database = ''
    _lemmatizer = ''

    def __init__(self, host, user, password, db):
        Learning.database = Database(host, user, password, db)
        Learning.esa = ESA()
        Learning._lemmatizer = PatternParserLemmatizer()



    # is called when using this class in another function with:
    # with Learning() as learning:
    #   learning.dolearn()
    def __exit__(self, exc_type, exc_value, traceback):
        Learning.connection.close()




    @staticmethod
    def prediction(cos, user_information, artikel_id):
        return cos

    # extend to person ID, load from database such things like age etc
    @staticmethod
    def learn(interests, artikel_id, person_id):
        information = Learning.database.getuserinformation(person_id)
        interest_vector = {}

        for i in information:
            interests.append(i)

        for i in interests:
            input = ""
            for term, tag in Learning._lemmatizer.lemmatize(i):
                input += " "+term

            tmp_vector = Learning.database.getarticlesfromwikipedia(2, input[1:])
            for title in tmp_vector:
                if title in interest_vector:
                    # in the moment only addition of the scores, maybe also try averaging of the scores
                    tmp = interest_vector[title]
                    interest_vector[title] = tmp + tmp_vector[title]
                else:
                    interest_vector[title] = tmp_vector[title]
                #if title in interest_vector:
                #    # in the moment only addition of the scores, maybe also try averaging of the scores
                #    tmp = interest_vector[title]
                #    interest_vector[title] = tmp.append(tmp_vector[title])
                #else:
                #    interest_vector[title] = [tmp_vector[title]]

        #interest_vector_new = {}
        #for iv in interest_vector:
        #    tmp = interest_vector[iv]
        #    if tmp != None:
        #        value = 0
        #        for t in tmp:
        #            value += t
        #        value = value/len(tmp)
        #        interest_vector_new[iv] = value

        sorted_results = sorted(interest_vector.items(), key=operator.itemgetter(1), reverse=True)
        print(sorted_results[:50])
        print(len(sorted_results))

        cos = Learning.esa.getCos(interests, artikel_id)
        return Learning.prediction(cos, interests, artikel_id)