# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request
from database import Database
from learning import Learning
import datetime
from feature import *

service = Flask(__name__)

ONLY_PERSONS = 0
WITHOUT_PERSONS = 1
ALL_ARTICLES = 2

host = 'localhost'
user = 'wikipedia_new'
password = '1234567'
db = 'wikipedia_new'



#curl http://localhost:5000/service/\?personid\='1'
@service.route('/service', methods=['POST'])
def get_articles_for_id():
    if request.headers['Content-Type'] == 'application/json':
        json_input = request.json
        database = Database(host, user, password, db)
        id = int(json_input['personid'])
        try:
            mode = json_input['mode']
        except:
            pass
        result = database.getpersonalizedarticles(id)

        database.close()
        return jsonify(result)
    else:
        return "415 Unsupported Media Type ;)"


#curl http://localhost:5000/getinterestscores/\?personid\='1'
@service.route('/getinterestscores', methods=['POST'])
def get_scores_for_id():
    if request.headers['Content-Type'] == 'application/json':
        json_input = request.json
        database = Database(host, user, password, db)
        id = int(json_input['personid'])
        result = database.getuserinterests(id)

        database.close()

        return jsonify(result)
    else:
        return "415 Unsupported Media Type ;)"


#updates a score, but also temporary adds a new interest with score (last one takes longer)
#curl http://localhost:5000/servicewithupdatedscoretemp/\?personid\='1'\&interestname\='fussball'\&score\='0'
@service.route('/servicewithupdatedscoretemp', methods=['POST'])
def update_score_temp():
    if request.headers['Content-Type'] == 'application/json':
        json_input = request.json
        today = datetime.datetime.now()
        date = today.strftime("%d%m%Y")
        database = Database(host, user, password, db)
        learning = Learning(host, user, password, db, date)
        userid = int(json_input['personid'])
        user_information =  Learning.database.getuserinformations(userid)
        user_information.append(Learning.database.getuserinterests(userid))

        interestname = json_input['interestname']
        score = json_input['score']
        tmp = {}
        if ',' in interestname:
            for x in interestname.split(','):
                tmp[x] = score
        else:
            tmp[interestname] = score

        articleids = database.getarticleidswithoutdate()
        article_informations = {}
        for id in articleids:
            article_informations[id] = Learning.database.getarticleinformations(id)

        results = Learning.learn(tmp, articleids, userid, ALL_ARTICLES, user_information, article_informations)
        prediction = {}
        for articleid in results:
            score = results[articleid]
            if score > 0.0:
                artikel = database.getarticletext(articleid)
                artikel_tmp = {}
                artikel_tmp['id'] = articleid
                artikel_tmp['score'] = score
                artikel_tmp['titel'] = artikel[0].get('titel')
                artikel_tmp['text'] = artikel[0].get('text')
                prediction[articleid] = artikel_tmp
        try:
            learning.close()
        except:
            pass
        try:
            database.close()
        except:
            pass
        return jsonify(prediction)
    else:
        return "415 Unsupported Media Type ;)"





##curl http://localhost:5000/getinterestscores/\?id\=1
#@service.route('/adduser/', methods=['GET'])
#@use_args(user_args)
#def add_user(args):
#    name = args['name']
#    vorname = args['name']
#    alter = args['age']
#    result = database.getuserinterests(id)
#
#    #return jsonify({'Works': 'bla'})
#    return jsonify(result)



if __name__ == '__main__':
    service.run(debug=False)