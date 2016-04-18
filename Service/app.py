# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request
from database import Database
from learning import Learning
import datetime
import sys

app = Flask(__name__)
host = 'localhost'
user = 'wikipedia_new'
password = '1234567'
db = 'wikipedia_new'
today = datetime.datetime.now()
datum = today.strftime("%d%m%Y")

database = Database(host, user, password, db)
learning = Learning(host, user, password, db, datum)


# curl -i http://localhost:5000/personalization/?personid=1&interests=Kunst
@app.route('/personalization/', methods=['GET'])
def get_articles():
    for x in request.args:
        print(x)
    userid= int(request.args.get('personid'))
    interests = []
    try:
        tmp = request.args.get('interests')
        if tmp != None:
            print(tmp)
            if "," in tmp:
                for i in tmp.split(","):
                    interests.append(i.replace('_'),' ')
            else:
                interests.append(tmp.replace('_', ' '))
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
    if len(interests) > 0:
        learning.relearn(interests,userid)
    results = database.getpersonalizedarticles(userid)
    return jsonify({'Personalisierung': results})


#@app.route('/article/<string:article_id>', methods=['GET'])
#def get_articletext(article_id):
#    results = database.getarticletext(article_id)
#    return jsonify({'Artikel': results})


#@app.errorhandler(404)
#def not_found(error):
#    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)