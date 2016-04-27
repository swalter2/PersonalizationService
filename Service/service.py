# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request
from webargs import fields
from webargs.flaskparser import use_args
from database import Database
from learning import Learning


service = Flask(__name__)

ONLY_PERSONS = 0
WITHOUT_PERSONS = 1
ALL_ARTICLES = 2

host = 'localhost'
user = 'wikipedia_new'
password = '1234567'
db = 'wikipedia_new'



article_args = {
    'id': fields.Str(required=True),
    'mode': fields.Str(required=False)
}

user_args = {
    'name': fields.Str(required=True),
    'vorname': fields.Str(required=True),
    'alter': fields.Str(required=True)
}

score_args = {
    'personid': fields.Str(required=True),
    'interestid': fields.Str(required=True),
    'score': fields.Str(required=True)
}


#curl http://localhost:5000/service/\?id\=5
@service.route('/service/', methods=['GET'])
@use_args(article_args)
def get_articles_for_id(args):
    database = Database(host, user, password, db)
    id = int(args['id'])
    try:
        mode = args['mode']
    except:
        pass
    result = database.getpersonalizedarticles(id)

    database.close()

    return jsonify(result)


#curl http://localhost:5000/getinterestscores/\?id\=1
@service.route('/getinterestscores/', methods=['GET'])
@use_args(article_args)
def get_scores_for_id(args):
    database = Database(host, user, password, db)
    id = int(args['id'])
    result = database.getuserinterests(id)

    database.close()

    return jsonify(result)


#curl http://localhost:5000/getinterestscores/\?id\=1
@service.route('/servicewithupdatedscoretemp/', methods=['GET'])
@use_args(score_args)
def update_score_temp(args):
    database = Database(host, user, password, db)
    learning = Learning(host, user, password, db)
    userid = int(args['personid'])
    interestid = int(args['interestid'])
    score = args['score']
    tmp = {}
    tmp[interestid] = score

    articleids = database.getarticleidswithoutdate()

    results = learning.learn(tmp, articleids, userid, ONLY_PERSONS)

    database.deleteuserinterestvector(userid)

    #for articleid in results:
    #    score = results[articleid]
    #    if score > 0.0:
    #        database.add_personalization_person_userarticle(userid, articleid, score)
    #print('learned mode 0')
    #
    #results = Learning.learn(tmp, articleids, userid, WITHOUT_PERSONS)
    #for articleid in results:
    #    score = results[articleid]
    #    if score > 0.0:
    #        database.add_personalization_without_person_userarticle(userid, articleid, score)
    #print('learned mode 1')
    #
    results = Learning.learn(tmp, articleids, userid, ALL_ARTICLES)
    for articleid in results:
        score = results[articleid]
        if score > 0.0:
            database.add_personalization_all_userarticle(userid, articleid, score)

    result = database.getpersonalizedarticles(userid)

    learning.close()
    database.close()
    return jsonify(result)


    #return jsonify({'Works': 'bla'})
    #return jsonify({})




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