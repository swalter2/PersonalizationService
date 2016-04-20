# -*- coding: utf-8 -*-
import pymysql.cursors
import sys
import operator


class Database:
    connection = ''
    results_alle = {}
    results_personen = {}
    results_ohne_personen = {}

    def __init__(self, host, user, password, db):
        Database.connection = pymysql.connect(host=host,
                             user=user,
                             password=password,
                             db=db,
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)


    @staticmethod
    def getarticlesfromwikipedia(mode, term, limit=0):
        term = term.replace("_"," ")
        switcher = {
            0: " and person=1",
            1: " and person=0",
            2: "",
        }

        if mode == 0 and term in Database.results_alle:
            return Database.results_alle[term]

        if mode == 1 and term in Database.results_personen:
            return Database.results_personen[term]

        if mode == 2 and term in Database.results_ohne_personen:
            return Database.results_ohne_personen[term]

        query = 'SELECT id,  MATCH (body) AGAINST (%s IN NATURAL LANGUAGE MODE) AS score ' \
                'FROM wikipedia WHERE MATCH (body) AGAINST (%s IN NATURAL LANGUAGE MODE)'

        query += switcher.get(mode)
        if limit > 0:
            query += " LIMIT "+str(limit)+";"
        else:
            query += ";"

        results = {}
        try:
            with Database.connection.cursor() as cursor:
                cursor.execute(query,(term, term))
                for row in cursor:
                    results[row.get('id')] = float(row.get('score'))
        except :
            print("Unexpected error:", sys.exc_info()[0])
            raise
        #sorted_results = sorted(results.items(), key=operator.itemgetter(1), reverse=True)
        #print(term, sorted_results)
        if len(results) ==0:
            results['0']=0


        if mode == 0:
            Database.results_alle[term] = results

        if mode == 1:
            Database.results_personen[term] = results

        if mode == 2:
            Database.results_ohne_personen[term] = results

        return results


    #@staticmethod
    #def getuserinterests(person_id):
    #    information = []
    #    query = 'Select distinct interesse from nutzer_interessen where id=%s;'
    #    try:
    #        with Database.connection.cursor() as cursor:
    #            cursor.execute(query, person_id)
    #            for row in cursor:
    #                information.append(row.get('interesse'))
    #    except :
    #        print("Unexpected error:", sys.exc_info()[0])
    #        raise
    #    return information


    @staticmethod
    def getuserids():
        userids = []
        query = 'Select distinct id from nutzer where 1;'
        try:
            with Database.connection.cursor() as cursor:
                cursor.execute(query)
                for row in cursor:
                    userids.append(row.get('id'))
        except :
            print("Unexpected error:", sys.exc_info()[0])
            raise
        return userids

    @staticmethod
    def getarticleids():
        articleids = []
        query = 'Select distinct id from artikel where 1;'
        try:
            with Database.connection.cursor() as cursor:
                cursor.execute(query)
                for row in cursor:
                    articleids.append(row.get('id'))
        except :
            print("Unexpected error:", sys.exc_info()[0])
            raise
        return articleids


    @staticmethod
    def getarticleidsfordate(date):
        articleids = []
        query = 'Select distinct id from artikel where datum=%s;'
        try:
            with Database.connection.cursor() as cursor:
                cursor.execute(query,date)
                for row in cursor:
                    articleids.append(row.get('id'))
        except :
            print("Unexpected error:", sys.exc_info()[0])
            raise
        return articleids

    @staticmethod
    def getarticleidswithoutdate():
        articleids = []
        query = 'Select distinct id from artikel where 1s;'
        try:
            with Database.connection.cursor() as cursor:
                cursor.execute(query)
                for row in cursor:
                    articleids.append(row.get('id'))
        except :
            print("Unexpected error:", sys.exc_info()[0])
            raise
        return articleids


    @staticmethod
    def add_personalization_all_userarticle(userid, articleid, score):
        try:
            with Database.connection.cursor() as cursor:
                sql = "INSERT INTO personalisierung_alle (articleid,userid,score) VALUES (%s,%s,%s);"
                cursor.execute(sql, (articleid, userid, score))
                Database.connection.commit()
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

    @staticmethod
    def add_personalization_person_userarticle(userid, articleid, score):
        try:
            with Database.connection.cursor() as cursor:
                sql = "INSERT INTO personalisierung_personen (articleid,userid,score) VALUES (%s,%s,%s);"
                cursor.execute(sql, (articleid, userid, score))
                Database.connection.commit()
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

    @staticmethod
    def add_personalization_without_persons_userarticle(userid, articleid, score):
        try:
            with Database.connection.cursor() as cursor:
                sql = "INSERT INTO personalisierung_ohne_personen (articleid,userid,score) VALUES (%s,%s,%s);"
                cursor.execute(sql, (articleid, userid, score))
                Database.connection.commit()
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise



    @staticmethod
    def getarticlevector(artikel_id, mode):
        vector = {}
        query = ""
        if mode == 0:
            query = 'Select distinct wikipediaid,score from vector_personen where id=%s;'
        if mode == 1:
            query = 'Select distinct wikipediaid,score from vector_ohne_personen where id=%s;'
        if mode == 2:
            query = 'Select distinct wikipediaid,score from vector_alle where id=%s;'
        try:
            with Database.connection.cursor() as cursor:
                cursor.execute(query,artikel_id)
                for row in cursor:
                    id = row.get('wikipediaid')
                    score = float(row.get('score'))
                    vector[id] = score

        except :
            print("Unexpected error:", sys.exc_info()[0])
            raise
        return vector


    @staticmethod
    def storearticle(article):
        try:
            with Database.connection.cursor() as cursor:
                sql = "INSERT INTO artikel (id,titel,text,tags,datum) VALUES (%s,%s,%s,%s,%s);"
                cursor.execute(sql, (article.id, article.titel, article.text, article.tags, article.datum))
                Database.connection.commit()
                for wikipediaid in article.vector_alle:
                    try:
                        with Database.connection.cursor() as cursor:
                            sql = "INSERT INTO vector_alle (id,wikipediaid,score) VALUES (%s,%s,%s);"
                            cursor.execute(sql, (article.id, wikipediaid, article.vector_alle[wikipediaid]))
                            Database.connection.commit()
                    except:
                        print("Unexpected error:", sys.exc_info()[0])
                        raise

                for wikipediaid in article.vector_personen:
                    try:
                        with Database.connection.cursor() as cursor:
                            sql = "INSERT INTO vector_personen (id,wikipediaid,score) VALUES (%s,%s,%s);"
                            cursor.execute(sql, (article.id, wikipediaid, article.vector_personen[wikipediaid]))
                            Database.connection.commit()
                    except:
                        print("Unexpected error:", sys.exc_info()[0])
                        raise

                for wikipediaid in article.vector_ohne_personen:
                    try:
                        with Database.connection.cursor() as cursor:
                            sql = "INSERT INTO vector_ohne_personen (id,wikipediaid,score) VALUES (%s,%s,%s);"
                            cursor.execute(sql, (article.id, wikipediaid, article.vector_ohne_personen[wikipediaid]))
                            Database.connection.commit()
                    except:
                        print("Unexpected error:", sys.exc_info()[0])
                        raise

        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise


    @staticmethod
    def getpersonalizedarticles(personid):
        results = {}
        try:
            with Database.connection.cursor() as cursor:
                sql = 'SELECT articleid, score, titel, text FROM personalisierung_alle, artikel WHERE userid=%s ' \
                      'and artikel.id=articleid ORDER BY score DESC LIMIT 20;'
                cursor.execute(sql,personid)
                for row in cursor:
                    tmp_hm = {}
                    tmp_hm['id'] = row.get('articleid')
                    tmp_hm['score'] = row.get('score')
                    tmp_hm['titel'] = row.get('titel')
                    tmp_hm['text'] = row.get('text')
                    results[row.get('articleid')] = tmp_hm
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
        return results


    @staticmethod
    def getarticletext(articleid):
        results = []
        try:
            with Database.connection.cursor() as cursor:
                sql = 'SELECT titel, text FROM artikel WHERE id=%s;'
                cursor.execute(sql, articleid)
                for row in cursor:
                    tmp_hm = {}
                    tmp_hm['artikelid'] = articleid
                    tmp_hm['titel'] = row.get('titel')
                    tmp_hm['text'] = row.get('text')

                    results.append(tmp_hm)
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
        return results

    @staticmethod
    def checkanddeletearticleexceptdate(date):
        dates = set()
        try:
            with Database.connection.cursor() as cursor:
                sql = "Select distinct datum from artikel;"
                cursor.execute(sql)
                for row in cursor:
                    dates.add(row.get('datum'))
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

        ids = set()
        if date in dates and len(dates)>1:
            try:
                with Database.connection.cursor() as cursor:
                    sql = 'DELETE FROM `artikel` WHERE datum!=%s;'
                    cursor.execute(sql, date)
                    Database.connection.commit()
            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise

    @staticmethod
    def updatedbwithinterestvector(id,vector, mode):
        print('updatedbwithinterestvector',id,mode)
        sql = ''
        if mode == 0:
            sql = "INSERT INTO interessen_vector_personen (id,wikipediaid,score) VALUES (%s,%s,%s);"
        if mode == 1:
            sql = "INSERT INTO interessen_vector_ohne_personen (id,wikipediaid,score) VALUES (%s,%s,%s);"
        if mode == 2:
            sql = "INSERT INTO interessen_vector_alle (id,wikipediaid,score) VALUES (%s,%s,%s);"

        for wikipediaid in vector:
            try:
                with Database.connection.cursor() as cursor:
                    cursor.execute(sql, (id, wikipediaid, vector[wikipediaid]))
                    Database.connection.commit()
            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise

    # create vector for each three modes for the given interest, then get vector for the given id/mode and update vector "vector" accoring to the score
    @staticmethod
    def createinterestvectorandupdatevector(id, vector, mode, score):
        print('createinterestvectorandupdatevector',id)
        sql = 'SELECT DISTINCT name FROM interessen WHERE id=%s;'

        interest = ""
        try:
            with Database.connection.cursor() as cursor:
                cursor.execute(sql, id)
                for row in cursor:
                    print(row.get('name'))
                    interest = row.get('name')
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
        print
        print
        tmp_vector_0 = Database.getarticlesfromwikipedia(0, interest)
        tmp_vector_1 = Database.getarticlesfromwikipedia(1, interest)
        tmp_vector_2 = Database.getarticlesfromwikipedia(2, interest)
        Database.updatedbwithinterestvector(id, tmp_vector_0, 0)
        Database.updatedbwithinterestvector(id, tmp_vector_1, 1)
        Database.updatedbwithinterestvector(id, tmp_vector_2, 2)
        tmp_vector = {}
        if mode == 0:
            tmp_vector = tmp_vector_0
        if mode == 1:
            tmp_vector = tmp_vector_1
        if mode == 2:
            tmp_vector = tmp_vector_2

        for wikipediaid in tmp_vector:
            if wikipediaid in vector:
                # in the moment only addition of the scores, maybe also try averaging of the scores
                tmp = vector[wikipediaid]
                vector[wikipediaid] = tmp + tmp_vector[wikipediaid]*score
            else:
                vector[wikipediaid] = tmp_vector[wikipediaid]*score
        return vector

    @staticmethod
    def getuserinterests(personid):

        # step1: Get all interest for a user

        sql = 'SELECT DISTINCT nutzer_interessen.interessensid, nutzer_interessen.score, interessen.name FROM nutzer_interessen, interessen WHERE nutzer_interessen.nutzerid=%s and nutzer_interessen.interessensid=interessen.id;'
        interests = {}
        try:
            with Database.connection.cursor() as cursor:
                cursor.execute(sql, personid)
                for row in cursor:
                    tmp = {}
                    tmp['score'] = row.get('score')
                    tmp['name'] = row.get('name')
                    tmp['id'] = row.get('interessensid')
                    interests[row.get('interessensid')] = tmp
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

        return interests




    @staticmethod
    def getuserinterestvector(personid, mode):

        # step1: Get all interest for a user

        sql = 'SELECT DISTINCT interessensid, score FROM nutzer_interessen WHERE nutzerid=%s;'
        interestsids = {}
        try:
            with Database.connection.cursor() as cursor:
                cursor.execute(sql, personid)
                for row in cursor:
                    interestsids[row.get('interessensid')] = 0.0+(row.get('score'))
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

        vector = {}

        # step2: Check, if each interest is represented as a vector, if not, create vector for interest
        # step3: get for each interest, score (defined for ech user) and vector
        for id in interestsids:
            sql = ''
            if mode == 0:
                sql = 'SELECT DISTINCT wikipediaid, score FROM interessen_vector_personen WHERE id=%s;'
            if mode == 1:
                sql = 'SELECT DISTINCT wikipediaid, score FROM interessen_vector_ohne_personen WHERE id=%s'
            if mode == 2:
                sql = 'SELECT DISTINCT wikipediaid, score FROM interessen_vector_alle WHERE id=%s'
            try:
                with Database.connection.cursor() as cursor:
                    cursor.execute(sql, id)
                    counter = 0
                    for row in cursor:
                        wikipediaid = row.get('wikipediaid')
                        score = 0.0+(row.get('score'))
                        # step4: multiply each locacl vector by interest score (defined pers user) and add to global vector.
                        if wikipediaid in vector:
                            tmp = vector[wikipediaid]
                            vector[wikipediaid] = tmp + score*interestsids[id]
                        else:
                            vector[wikipediaid] = score*interestsids[id]
                        counter += 1
                    if counter == 0:
                        vector = Database.createinterestvectorandupdatevector(id, vector, mode, interestsids[id])

            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise
        # step5: return "overall interests vector"
        return vector;