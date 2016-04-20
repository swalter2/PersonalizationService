# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request
from webargs import fields
from webargs.flaskparser import use_args
from database import Database

service = Flask(__name__)


host = 'localhost'
user = 'wikipedia_new'
password = '1234567'
db = 'wikipedia_new'


database = Database(host, user, password, db)

article_args = {
    'id': fields.Str(required=True),
    'mode': fields.Str(required=False)
}

#curl http://localhost:5000/service/\?id\=5
@service.route('/service/', methods=['GET'])
@use_args(article_args)
def get_articles_for_id(args):
    id = args['id']
    try:
        mode = args['mode']
    except:
        pass
    result = database.getpersonalizedarticles(id)

    #return jsonify({'Works': 'bla'})
    return jsonify(result)


#curl http://localhost:5000/getinterestscores/\?id\=1
@service.route('/getinterestscores/', methods=['GET'])
@use_args(article_args)
def get_scores_for_id(args):
    id = args['id']
    result = database.getuserinterests(id)

    #return jsonify({'Works': 'bla'})
    return jsonify(result)


if __name__ == '__main__':
    service.run(debug=False)