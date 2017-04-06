# -*- coding: utf-8 -*-
import pymysql
import sys
from textblob_de.lemmatizers import PatternParserLemmatizer
from events import Event
from rezepte import Rezept

ONLY_PERSONS = 0
WITHOUT_PERSONS = 1
ALL_ARTICLES = 2
VECTOR_SIZE = 500

class Database:
    connection = ''
    results_alle = {}
    results_personen = {}
    results_ohne_personen = {}
    _lemmatizer = ''
    event = Event()
    rezept = Rezept()


    def __init__(self, host, user, password, db):
        # print("Connecting to Database...")
        Database.connection = pymysql.connect(
                             host=host,
                             user=user,
                             password=password,
                             db=db,
                             charset='utf8mb4',
                             # port=8889,     # comment this and the next line before pushing
                             # unix_socket="/Applications/MAMP/tmp/mysql/mysql.sock",
                             cursorclass=pymysql.cursors.DictCursor)

        Database._lemmatizer = PatternParserLemmatizer()
        # print("Done")

    def close(self):
        #this line thros an error....
        #self.connection.close()
        pass

    @staticmethod
    def getarticlesfromwikipedia(mode, term, limit=0):
        term = term.replace("_"," ")

        if mode == ALL_ARTICLES and term in Database.results_alle:
            return Database.results_alle[term]

        if mode == ONLY_PERSONS and term in Database.results_personen:
            return Database.results_personen[term]

        if mode == WITHOUT_PERSONS and term in Database.results_ohne_personen:
            return Database.results_ohne_personen[term]

        query = 'SELECT id,  MATCH (body) AGAINST (%s IN NATURAL LANGUAGE MODE) AS score ' \
                'FROM wikipedia WHERE MATCH (body) AGAINST (%s IN NATURAL LANGUAGE MODE)'

        if mode == ALL_ARTICLES:
            query += ''

        if mode == ONLY_PERSONS:
            query += ' and person=1'

        if mode == WITHOUT_PERSONS:
            query += ' and person=0'

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
        #sollte das bei Interessen stehen?
        #if len(results) ==0:
        #    results['0']=0


        if mode == ALL_ARTICLES:
            Database.results_alle[term] = results

        if mode == ONLY_PERSONS:
            Database.results_personen[term] = results

        if mode == WITHOUT_PERSONS:
            Database.results_ohne_personen[term] = results

        return results



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
        query = 'Select distinct id from artikel;'
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
        #print('called add_personalization_all_userarticle')
        # print("DB\tInserting {}:{}:{} into DB...".format(userid,articleid,score))
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
    def add_personalization_without_person_userarticle(userid, articleid, score):
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
        if mode == ONLY_PERSONS:
            query = 'Select distinct wikipediaid,score from vector_personen where id=%s;'
        if mode == WITHOUT_PERSONS:
            query = 'Select distinct wikipediaid,score from vector_ohne_personen where id=%s;'
        if mode == ALL_ARTICLES:
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
                sql = "INSERT INTO artikel (id,titel,text,tags,datum, ressort, seite, anzahl_woerter) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);"
                cursor.execute(sql, (article.id, article.titel, article.text, article.tags, article.datum, article.ressort, article.seite, article.anzahl_woerter))
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
                      'and artikel.id=articleid ORDER BY score DESC LIMIT 20;'              #LIMIT in this SQL-Query sets the amount of articles that are returned. Could be turned into a function parameter
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
    def getpersonalizedarticles_justids(personId, date):
        results = {}
        print(date)
        try:
            with Database.connection.cursor() as cursor:
                sql = 'SELECT articleid, score FROM personalisierung_alle, artikel WHERE userid=%s AND datum= %s ' \
                      'and artikel.id=articleid ORDER BY score DESC;'              #LIMIT in this SQL-Query sets the amount of articles that are returned. Could be turned into a function parameter
                cursor.execute(sql,(personId, date))
                for row in cursor:
                    tmp_hm = {}
                    tmp_hm['articleid'] = row.get('articleid')
                    tmp_hm['score'] = row.get('score')
                    results[row.get('articleid')] = tmp_hm
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
        return results

    @staticmethod
    def getarticlesfordate(date,number_articles=500):
        print(date)
        results = {}
        try:
            with Database.connection.cursor() as cursor:
                sql = 'SELECT id, titel, text, seite FROM artikel WHERE datum= %s LIMIT %s;'          #LIMIT in this SQL-Query sets the amount of articles that are returned. Could be turned into a function parameter
                cursor.execute(sql,(date,number_articles))
                for row in cursor:
                    tmp_hm = {}
                    tmp_hm['id'] = row.get('id')
                    tmp_hm['titel'] = row.get('titel')
                    tmp_hm['text'] = row.get('text')
                    tmp_hm['seite'] = row.get('seite')
                    results[row.get('id')] = tmp_hm
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
    def getannotatedarticleinformations(articleid):
        results = []
        try:
            with Database.connection.cursor() as cursor:
                sql = 'SELECT titel, text, ressort, seite, anzahl_woerter FROM annotierte_artikel WHERE id=%s;'
                cursor.execute(sql, articleid)
                for row in cursor:
                    results.append(row.get('titel'))
                    results.append(row.get('text'))
                    results.append(row.get('ressort'))
                    results.append(row.get('seite'))
                    results.append(row.get('anzahl_woerter'))
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
        return results

    @staticmethod
    def getarticleinformations(articleid):
        results = []
        try:
            with Database.connection.cursor() as cursor:
                sql = 'SELECT titel, text, ressort, seite, anzahl_woerter FROM artikel WHERE id=%s;'
                cursor.execute(sql, articleid)
                for row in cursor:
                    results.append(row.get('titel'))
                    results.append(row.get('text'))
                    results.append(row.get('ressort'))
                    results.append(row.get('seite'))
                    results.append(row.get('anzahl_woerter'))
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
        return results

    @staticmethod
    def checkfordateindb(date):
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

        current_date_in_db = dates.pop()
        if date == current_date_in_db:
            return True, current_date_in_db
        else:
            return False, current_date_in_db

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
        if mode == ONLY_PERSONS:
            sql = "INSERT INTO interessen_vector_personen (id,wikipediaid,score) VALUES (%s,%s,%s);"
        if mode == WITHOUT_PERSONS:
            sql = "INSERT INTO interessen_vector_ohne_personen (id,wikipediaid,score) VALUES (%s,%s,%s);"
        if mode == ALL_ARTICLES:
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

        tmp_vector_0 = Database.getarticlesfromwikipedia(ONLY_PERSONS, interest,100)
        tmp_vector_1 = Database.getarticlesfromwikipedia(WITHOUT_PERSONS, interest,100)
        tmp_vector_2 = Database.getarticlesfromwikipedia(ALL_ARTICLES, interest,100)
        # sometimes, through spelling errors, no interest vector can be found. in order to reduce computaion time, set those interest to 0
        if len(tmp_vector_0) == 0:
            tmp_vector_0['0'] = 0
        if len(tmp_vector_1) == 0:
            tmp_vector_1['0'] = 0
        if len(tmp_vector_2) == 0:
            tmp_vector_2['0'] = 0
        Database.updatedbwithinterestvector(id, tmp_vector_0, ONLY_PERSONS)
        Database.updatedbwithinterestvector(id, tmp_vector_1, WITHOUT_PERSONS)
        Database.updatedbwithinterestvector(id, tmp_vector_2, ALL_ARTICLES)

        tmp_vector = {}
        if mode == ONLY_PERSONS:
            tmp_vector = tmp_vector_0
        if mode == WITHOUT_PERSONS:
            tmp_vector = tmp_vector_1
        if mode == ALL_ARTICLES:
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
    def getinterestvectorforterm(term, mode):

        sql = 'SELECT DISTINCT id FROM interessen WHERE name=%s;'
        ids = set()
        try:
            with Database.connection.cursor() as cursor:
                cursor.execute(sql, term)
                for row in cursor:
                    ids.add(row.get('id'))
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

        vector = {}

        for id in ids:
            sql = ''
            if mode == ONLY_PERSONS:
                sql = 'SELECT DISTINCT wikipediaid, score FROM interessen_vector_personen WHERE id=%s;'
            if mode == WITHOUT_PERSONS:
                sql = 'SELECT DISTINCT wikipediaid, score FROM interessen_vector_ohne_personen WHERE id=%s'
            if mode == ALL_ARTICLES:
                sql = 'SELECT DISTINCT wikipediaid, score FROM interessen_vector_alle WHERE id=%s'
            try:
                with Database.connection.cursor() as cursor:
                    cursor.execute(sql, id)
                    counter = 0
                    for row in cursor:
                        wikipediaid = row.get('wikipediaid')
                        score = 0.0 + (row.get('score'))
                        # step4: multiply each locacl vector by interest score (defined pers user) and add to global vector.
                        if wikipediaid in vector:
                            tmp = vector[wikipediaid]
                            vector[wikipediaid] = tmp + score
                        else:
                            vector[wikipediaid] = score

            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise
        return vector;

    @staticmethod
    def getinterestvectorforid(interestid, mode):

        sql = 'SELECT DISTINCT id FROM interessen WHERE id=%s;'
        ids = set()
        try:
            with Database.connection.cursor() as cursor:
                cursor.execute(sql, interestid)
                for row in cursor:
                    ids.add(row.get('id'))
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

        vector = {}

        for id in ids:
            sql = ''
            if mode == ONLY_PERSONS:
                sql = 'SELECT DISTINCT wikipediaid, score FROM interessen_vector_personen WHERE id=%s;'
            if mode == WITHOUT_PERSONS:
                sql = 'SELECT DISTINCT wikipediaid, score FROM interessen_vector_ohne_personen WHERE id=%s'
            if mode == ALL_ARTICLES:
                sql = 'SELECT DISTINCT wikipediaid, score FROM interessen_vector_alle WHERE id=%s'
            try:
                with Database.connection.cursor() as cursor:
                    cursor.execute(sql, id)
                    counter = 0
                    for row in cursor:
                        wikipediaid = row.get('wikipediaid')
                        score = 0.0 + (row.get('score'))
                        # step4: multiply each locacl vector by interest score (defined pers user) and add to global vector.
                        if wikipediaid in vector:
                            tmp = vector[wikipediaid]
                            vector[wikipediaid] = tmp + score
                        else:
                            vector[wikipediaid] = score

            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise
        return vector;



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

        for id in interestsids:
            sql = ''
            if mode == ONLY_PERSONS:
                sql = 'SELECT DISTINCT wikipediaid, score FROM interessen_vector_personen WHERE id=%s;'
            if mode == WITHOUT_PERSONS:
                sql = 'SELECT DISTINCT wikipediaid, score FROM interessen_vector_ohne_personen WHERE id=%s'
            if mode == ALL_ARTICLES:
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

    @staticmethod
    def deleteuserinterestvector(userid):
        try:
            with Database.connection.cursor() as cursor:
                sql = "DELETE FROM personalisierung_alle WHERE userid=%s;"
                cursor.execute(sql,userid)
                Database.connection.commit()
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

        try:
            with Database.connection.cursor() as cursor:
                sql = "DELETE FROM personalisierung_personen WHERE userid=%s;"
                cursor.execute(sql, userid)
                Database.connection.commit()
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

        try:
            with Database.connection.cursor() as cursor:
                sql = "DELETE FROM  personalisierung_ohne_personen WHERE userid=%s;"
                cursor.execute(sql, userid)
                Database.connection.commit()
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

    @staticmethod
    def deleteuser(userid):
        try:
            with Database.connection.cursor() as cursor:
                sql = "DELETE FROM nutzer WHERE id=%s;"
                cursor.execute(sql, userid)
                Database.connection.commit()
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise


    @staticmethod
    def _tmp_add_interesse(userid, interesse, score):
        interessen = {}
        query = 'Select distinct id, name  from interessen;'
        try:
            with Database.connection.cursor() as cursor:
                cursor.execute(query)
                for row in cursor:
                    interessen[row.get('name')] = row.get('id')
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
        tags = Database._lemmatizer.lemmatize(interesse)
        interesse = ""
        for term, tag in tags:
            interesse += " "+term
        interesse = interesse.strip()

        interessensid = 0
        if interesse in interessen:
            interessensid = interessen[interesse]
        else:
            number = 0
            try:
                with Database.connection.cursor() as cursor:
                    cursor.execute('SELECT MAX(id) as tmp from interessen;')
                    for row in cursor:
                        number = int(row.get('tmp'))
            except:
                print("Unexpected error:", sys.exc_info()[0])
                number = 0
                raise
            interessensid = number+1
            sql = "INSERT INTO interessen (id,name) VALUES (%s,%s);"
            try:
                with Database.connection.cursor() as cursor:
                    cursor.execute(sql,(interessensid,interesse))
                    Database.connection.commit()
            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise
        #add interesse zu nutzer_interesse, wenn nicht bereits vorhanden
        results = set()
        try:
            with Database.connection.cursor() as cursor:
                cursor.execute('SELECT nutzerid from nutzer_interessen WHERE nutzerid=%s and interessensid=%s;',(userid,interessensid))
                for row in cursor:
                    results.add(row.get('nutzerid'))
        except:
            print("Unexpected error:", sys.exc_info()[0])
            number = 0
            raise
        if len(results) == 0:
            sql = "INSERT INTO nutzer_interessen (nutzerid,interessensid,score) VALUES (%s,%s,%s);"
            try:
                with Database.connection.cursor() as cursor:
                    cursor.execute(sql, (userid, interessensid, score))
                    Database.connection.commit()
            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise
            if len(Database.getinterestvectorforid(interessensid, ALL_ARTICLES)) == 0:
                tmp_vector_0 = Database.getarticlesfromwikipedia(ALL_ARTICLES, interesse, 100)
                if len(tmp_vector_0) == 0:
                    tmp_vector_0['0'] = 0
                Database.updatedbwithinterestvector(interessensid, tmp_vector_0, ALL_ARTICLES)
            #also create vector for interests, if interest does not exist as vector..
            #if len(Database.getinterestvectorforid(interessensid,ONLY_PERSONS))==0:
            #    tmp_vector_0 = Database.getarticlesfromwikipedia(ONLY_PERSONS, interesse, 100)
            #    if len(tmp_vector_0) == 0:
            #        tmp_vector_0['0'] = 0
            #    Database.updatedbwithinterestvector(interessensid, tmp_vector_0, WITHOUT_PERSONS)
            #if len(Database.getinterestvectorforid(interessensid,WITHOUT_PERSONS))==0:
            #    tmp_vector_0 = Database.getarticlesfromwikipedia(WITHOUT_PERSONS, interesse, 100)
            #    if len(tmp_vector_0) == 0:
            #        tmp_vector_0['0'] = 0
            #    Database.updatedbwithinterestvector(interessensid, tmp_vector_0, WITHOUT_PERSONS)





    @staticmethod
    def getannotations():
        annotations = []
        sql = 'SELECT nutzerid, artikelid, bewertung FROM annotationen;'
        try:
            with Database.connection.cursor() as cursor:
                cursor.execute(sql)
                for row in cursor:
                    annotations.append([row.get('nutzerid'),row.get('artikelid'),row.get('bewertung')])
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

        return annotations

    @staticmethod
    def getuserinformations(userid):
        informations = []
        sql = 'SELECT age, geschlecht, abschluss, personalisierungs_level, interessen_kultur, interessen_lokales, interessen_lokalsport, interessen_politik, interessen_sport FROM nutzer where id=%s;'
        try:
            with Database.connection.cursor() as cursor:
                cursor.execute(sql,userid)
                for row in cursor:
                    informations.append(row.get('age'))     #0
                    informations.append(row.get('geschlecht')) #1
                    informations.append(row.get('abschluss'))   #2
                    informations.append(row.get('interessen_kultur')) #3
                    informations.append(row.get('interessen_lokales')) #4
                    informations.append(row.get('interessen_lokalsport')) #5
                    informations.append(row.get('interessen_politik')) #6
                    informations.append(row.get('interessen_sport')) #7
                    informations.append(row.get('personalisierungs_level')) #8
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

        return informations

    @staticmethod
    def get_ressort_list():
        ressorts = set()
        sql = 'SELECT DISTINCT ressort FROM artikel;'
        try:
            with Database.connection.cursor() as cursor:
                cursor.execute(sql)
                for row in cursor:
                    ressorts.add(row.get('ressort'))
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
        sql = 'SELECT DISTINCT ressort FROM annotierte_artikel;'
        try:
            with Database.connection.cursor() as cursor:
                cursor.execute(sql)
                for row in cursor:
                    ressorts.add(row.get('ressort'))
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

        return ressorts

    @staticmethod
    def get_age_list():
        ages = set()
        sql = 'SELECT DISTINCT age FROM nutzer;'
        try:
            with Database.connection.cursor() as cursor:
                cursor.execute(sql)
                for row in cursor:
                    ages.add(row.get('age'))
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

        return ages

    @staticmethod
    def getpersonalizedevents(personid):
        interests_raw = Database.getuserinterests(personid)
        interests = []
        for interest_id in interests_raw:
            interest = interests_raw[interest_id]
            score = interest['score']
            # for old users, make sure score is not below 1
            if score < 1:
                score = round(score*10.0)
            if score >= 3:
                interests.append(interest['name'])
        return Database.event.get_events(interests)

    @staticmethod
    def getraweventdata():
        return Database.event.get_raw_events()

    @staticmethod
    def getpersonalizedevents_justscores(personid):
        interests_with_scores = Database.getuserinterests(personid)
        return Database.event.get_events_ids_scores(interests_with_scores)

    @staticmethod
    def getallrecipes():
        return Database.rezept.get_all_recipes()

    @staticmethod
    def getpersonalizedrecipes(personid):
        return Database.rezept.get_rezept()

    @staticmethod
    def getpersonalizedrecipes_justscores(personid):
        return Database.rezept.get_personalized_recipes(personid)

    @staticmethod
    def add_user(json_input, person_id = ''):

        translations = {}
        translations["electro"] = "Electro"
        translations["hiphop"] = "Hip Hop"
        translations["jazz"] = "Jazz"
        translations["metal"] = "Metal"
        translations["other_music"] = "Musik"
        translations["pop"] = "Pop"
        translations["rock"] = "Rock"
        translations["basketball"] = "Basketball"
        translations["cycling"] = "Fahhrad fahren"
        translations["golf"] = "Golf"
        translations["handball"] = "Handball"
        translations["others_sport"] = "Sport"
        translations["riding"] = "Reiten"
        translations["soccer"] = "Fußball"
        translations["swimming"] = "Schwimmen"
        translations["tennis"] = "Tennis"
        translations["wintersport"] = "Wintersport"


        try:
            if person_id == '':
                person_ids = Database.getuserids()
                person_id = max(person_ids)+1
            else:
                pass

            # "personalizationlevel":"medium",
            personalization_level = json_input['personalizationlevel']

            interest_rating = json_input['interestratings'] # this is a list in in the list is a dictionary....
            interest_rating = interest_rating[0]

            interessen_sport_list = interest_rating['interest_sports']
            interessen_sport_hm = interessen_sport_list[0]
            interessen_sport = 0
            for sport in interessen_sport_hm:
                interessen_sport += int(interessen_sport_hm[sport])
            interessen_sport = round(interessen_sport/(len(interessen_sport_hm)+0.0))

            interessen_lokales = int(interest_rating['localnews'])

            interessen_politik = int(interest_rating['politics'])

            geschlecht = "m"
            if json_input['sex'] == 'Weiblich':
                geschlecht = 'w'

            abschluss = json_input['educationlevel']

            if abschluss == 'Hochschulreife':
                abschluss = 'Abitur'
            abschluss = abschluss.strip()



            #interessen_kultur fehlt
            #interessen_lokalsport fehlt

            interessen_vector = {}
            for sport in interessen_sport_hm:
                interessen_vector[translations[sport]] = interessen_sport_hm[sport]

            interessen_musik_list = interest_rating['interest_musics']
            interessen_musik_hm = interessen_musik_list[0]
            for musik in interessen_musik_hm:
                interessen_vector[translations[musik]] = int(interessen_musik_hm[musik])
            try:

                with Database.connection.cursor() as cursor:
                    sql = "INSERT INTO nutzer (id,age,geschlecht,personalisierungs_level,abschluss,interessen_kultur,interessen_lokales," \
                          "interessen_lokalsport,interessen_politik,interessen_sport,interessanteste_rubrik,plz) " \
                          "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
                    cursor.execute(sql, (person_id,json_input['age'],geschlecht,personalization_level,abschluss,"3",interessen_lokales,"3",interessen_politik,interessen_sport,"none","0"))
                    Database.connection.commit()

                for interesse in interessen_vector:
                    Database._tmp_add_interesse(person_id, interesse, interessen_vector[interesse])
                print('added user with id '+str(person_id))
                return person_id
            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise
                return -1
        except:
            #do not add user but return -1
            print("Unexpected error:", sys.exc_info()[0])
            raise
            return -1

    @staticmethod
    def update_user(json_input, person_id):
        if Database.check_if_user_exists(person_id):
            Database.deleteuser(person_id)
            print("deleted user with id:" +str(person_id))
            return Database.add_user(json_input,person_id)
        else:
            return -1

    @staticmethod
    def add_to_permant_tables(personid,articleid,feedback):
        try:
            with Database.connection.cursor() as cursor:
                sql = "INSERT INTO feedback_permanent (id,nutzerid,feedback) VALUES (%s,%s,%s);"
                cursor.execute(sql, (articleid, personid, feedback))
                Database.connection.commit()

            id = ''
            titel = ''
            text = ''
            tags = ''
            datum = ''
            ressort = ''
            seite = ''
            anzahl_woerter = ''
            query = 'Select distinct id,titel,text,tags,datum, ressort, seite, anzahl_woerter from artikel where id=%s;'
            with Database.connection.cursor() as cursor:
                cursor.execute(query, articleid)
                for row in cursor:
                    id = row.get('id')
                    titel = row.get('titel')
                    text = row.get('text')
                    tags = row.get('tags')
                    datum = row.get('datum')
                    ressort = row.get('ressort')
                    seite = row.get('seite')
                    anzahl_woerter = row.get('anzahl_woerter')
            with Database.connection.cursor() as cursor:
                sql = "INSERT INTO artikel_permanent (id,titel,text,tags,datum, ressort, seite, anzahl_woerter) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);"
                cursor.execute(sql, (id, titel, text, tags, datum, ressort, seite, anzahl_woerter))
                Database.connection.commit()

        except:
            print("Unexpected error:", sys.exc_info()[0])
            with Database.connection.cursor() as cursor:
                sql = 'DELETE FROM feedback_permanent WHERE nutzerid=%s and id=%s;'
                cursor.execute(sql, (personid,articleid))
                Database.connection.commit()
            raise

    @staticmethod
    def update_feedback(personid,articleid,feedback):
        try:
            with Database.connection.cursor() as cursor:
                sql = "INSERT INTO feedback_tmp (id,nutzerid,feedback) VALUES (%s,%s,%s);"
                cursor.execute(sql, (articleid, personid, feedback))
                Database.connection.commit()
                Database.add_to_permant_tables(personid,articleid,feedback)
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

    @classmethod
    def check_if_user_exists(cls, person_id):
        informations = Database.getuserinformations(person_id)
        if len(informations) == 0:
            return False
        else:
            return True










