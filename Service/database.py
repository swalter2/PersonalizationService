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

        if mode == 0:
            Database.results_alle[term] = results

        if mode == 1:
            Database.results_personen[term] = results

        if mode == 2:
            Database.results_ohne_personen[term] = results

        return results


    @staticmethod
    def getuserinformation(person_id):
        information = []
        query = 'Select distinct interest from nutzer where id=%s'
        try:
            with Database.connection.cursor() as cursor:
                cursor.execute(query, person_id)
                for row in cursor:
                    information.append(row.get('interest'))
        except :
            print("Unexpected error:", sys.exc_info()[0])
            raise
        return information

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
    def checkanddeletearticleexceptdate(date):
        dates = set()
        try:
            with Database.connection.cursor() as cursor:
                sql = "Select datum from artikel"
                cursor.execute(sql)
                for row in cursor:
                    dates.add(row.get('datum'))
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

        ids = set()
        if date in dates:
            for d in dates:
                if d != date:
                    try:
                        with Database.connection.cursor() as cursor:
                            sql = "Select id from artikel where datum=%s"
                            cursor.execute(sql,date)
                            for row in cursor:
                                ids.add(row.get('id'))
                    except:
                        print("Unexpected error:", sys.exc_info()[0])
                        raise

            for id in ids:
                try:
                    with Database.connection.cursor() as cursor:
                        #delete everythig except the actual day
                        sql = 'DELETE FROM `artikel` WHERE id=%s'
                        cursor.execute(sql, date)
                except:
                    print("Unexpected error:", sys.exc_info()[0])
                    raise