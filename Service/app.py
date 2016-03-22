# -*- coding: utf-8 -*-
from flask import Flask, jsonify
from database import Database

app = Flask(__name__)
host = 'localhost'
user = 'wikipedia_new'
password = '1234567'
db = 'wikipedia_new'

database = Database(host, user, password, db)


@app.route('/personalization/<int:person_id>', methods=['GET'])
def get_articles(person_id):
    results = database.getpersonalizedarticles(person_id)
    return jsonify({'Personalisierung': results})


#@app.route('/article/<string:article_id>', methods=['GET'])
#def get_articletext(article_id):
#    results = database.getarticletext(article_id)
#    return jsonify({'Artikel': results})


#@app.errorhandler(404)
#def not_found(error):
#    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=False)