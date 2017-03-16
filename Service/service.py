# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request
from database import Database
from learning import Learning
import sys
import datetime
import re

service = Flask(__name__)

ONLY_PERSONS = 0
WITHOUT_PERSONS = 1
ALL_ARTICLES = 2

host = 'localhost'
user = 'wikipedia_new'
password = '1234567'
db = 'wikipedia_new'

#
# ######FOR LOCAL TESTING#######
# host = 'localhost'
# user = 'root'
# password = 'root'
# db = 'nw_esa'
# ##############################


today = datetime.datetime.now()
datum = today.strftime("%d%m%Y")


# /service
# curl -X POST --data "{\"personid\":\"116\"}"  http://kognihome.sebastianwalter.org/service --header "Content-type:application/json"
#
# /serviceArticles
# curl -X POST --data "{\"datum\":\"12032017\"}"  http://kognihome.sebastianwalter.org/serviceArticles --header "Content-type:application/json"
#
# /servicePersonalization
# curl -X POST --data "{\"personid\":\"116\"}"  http://kognihome.sebastianwalter.org/servicePersonalization --header "Content-type:application/json"

#json-{"age":" 25","educationlevel":" Hochschulabschluss",
# "interestratings":[{"culture":"3",
# "economy":"3","
# interest_musics":[{"electro":"5","hiphop":"4","jazz":"2","metal":"1","other_music":"4","pop":"5","rock":"4"}],
# "interest_sports":[{"basketball":"3","cycling":"3","golf":"2","handball":"3",
# "others_sport":"5","riding":"5","soccer":"1","swimming":"5","tennis":"4","wintersport":"1"}],
# "localnews":"2","politics":"1"}],"location":" Bielefeld","name":" Sabrina ","sex":" Weiblich"}

#http://blog.luisrei.com/articles/flaskrest.html
#def check_auth(username, password):
#    return username == 'admin' and password == 'secret'
#
#def authenticate():
#    message = {'message': "Authenticate."}
#    resp = jsonify(message)
#
#    resp.status_code = 401
#    resp.headers['WWW-Authenticate'] = 'Basic realm="Example"'
#
#    return resp
#
#def requires_auth(f):
#    @wraps(f)
#    def decorated(*args, **kwargs):
#        auth = request.authorization
#        if not auth:
#            return authenticate()
#
#        elif not check_auth(auth.username, auth.password):
#            return authenticate()
#        return f(*args, **kwargs)
#    return decorated
#@requires_auth

#############THIS IS THE CURRENT EXAMPLE CONTAINING personalizationLevel
# json:  {"age":"25",
#         "educationlevel":"Hochschulabschluss",
#         "interestratings":[{"culture":"4",
#                             "economy":"4",
#                             "interest_musics":[{"electro":"3","hiphop":"5","jazz":"2","metal":"4","other_music":"1","pop":"5","rock":"5"}],
#                             "interest_sports":[{"basketball":"2","cycling":"4","golf":"3","handball":"1","others_sport":"3","riding":"5","soccer":"2","swimming":"5","tennis":"2","wintersport":"1"}],
#                             "localnews":"4","politics":"3"}],
#         "location":"Bielefeld",
#         "name":"Sabrina ",
#         "personalizationlevel":"medium",
#         "sex":"Weiblich"}

#curl http://localhost:5000/service/\?personid\='1'
@service.route('/user', methods=['POST'])
def update_user():
    if request.headers['Content-Type'] == 'application/json':
        json_input = request.json
        print(json_input)
        try:
            person_id = 0
            database = Database(host, user, password, db)
            if 'personid' in json_input:        #this seems to be used for updating
                person_id = json_input['personid']
                result = database.update_user(json_input,person_id)
                if result == -1:
                    database.close()
                    return "500 - error in json input"
                else:
                    learning = Learning(host, user, password, db, datum)
                    learning.single_learn(person_id)
                    print("done with user update with id ",person_id)
                    learning.close()
                    sys.stdout.flush()
            else:       # if no personId is given in the json, a new user is created instead
                person_id = database.add_user(json_input)
                if person_id == -1:
                    database.close()
                    return "500 - error in json input"
                else:
                    learning = Learning(host, user, password, db, datum)
                    learning.single_learn(person_id)
                    learning.close()
                    print("done with adding new user")
            database.close()
            return jsonify({"personid":person_id})
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
            return "500 - error in json input"
    else:
        return "415 Unsupported Media Type ;)"

@service.route('/feedback', methods=['POST'])
def give_feedback():
    if request.headers['Content-Type'] == 'application/json':
        json_input = request.json
        print(json_input)
        try:
            person_id = json_input['personid']
            article_id = json_input['articleid']
            feedback = json_input['feedback']
            database = Database(host, user, password, db)
            database.update_feedback(person_id, article_id, feedback)
            database.close()
            return jsonify({"personid": person_id})
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
            return "500 - error in json input"
    else:
        return "415 Unsupported Media Type ;)"


#curl http://localhost:5000/service/\?personid\='1'
@service.route('/service', methods=['POST'])
def get_articles_for_id():
    if request.headers['Content-Type'] == 'application/json':
        json_input = request.json
        try:
            database = Database(host, user, password, db)
            personid = int(json_input['personid'])
            try:
                mode = json_input['mode']
            except:
                pass
            results = {}

            result = database.getpersonalizedarticles(personid)
            results['artikel'] = result

            result = database.getpersonalizedevents(personid)
            results['events'] = result

            result = database.getpersonalizedrecipes(personid)
            results['rezepte'] = result

            database.close()
            return jsonify(results)
        except:
            print("500 - error in json input")
            return "500 - error in json input"
    else:
        return "415 Unsupported Media Type ;)"

#get all articles (ids, title, text, page) for a given date
@service.route('/serviceArticles', methods=['POST'])
def get_article_data_for_id():
    if request.headers['Content-Type'] == 'application/json':
        json_input = request.json

        try:
            database = Database(host, user, password, db)

            try:
                date = json_input['datum']
            except:
                date = datum

            if not check_date_format(date):
                return "416 Wrong Date Format: {}. Should be DDMMYYYY in correct ranges.".format(date)
            if not database.checkfordateindb(date):
                return "417 No Issue of the Neue Westfaelische for this Date ({})".format(date)

            try:
                number_articles = json_input['anzahl_artikel']
            except:
                number_articles = 500

            results = {}
            article_data = database.getarticlesfordate(date, number_articles)
            results['artikel'] = article_data

            database.close()
            return jsonify(results)
        except:
            print("500 - error in json input")
            return "500 - error in json input"
    else:
        return "415 Unsupported Media Type ;)"

#get personalization in form of scores for all articles for a given user
@service.route('/servicePersonalization', methods=['POST'])
def get_personalization_for_id():
    if request.headers['Content-Type'] == 'application/json':
        json_input = request.json
        try:
            database = Database(host, user, password, db)
            personid = int(json_input['personid'])
            try:
                date = json_input['datum']
            except:
                date = datum

            if not check_date_format(date):
                return "416 Wrong Date Format: {}. Should be DDMMYYYY in correct ranges.".format(date)
            if not database.checkfordateindb(date):
                return "417 No Issue of the Neue Westfaelische for this Date ({})".format(date)

            results = {}

            result = database.getpersonalizedarticles_justids(personid,date)
            results['artikel'] = result

            database.close()
            return jsonify(results)
        except:
            print("500 - error in json input")
            return "500 - error in json input"
    else:
        return "415 Unsupported Media Type ;)"


if __name__ == '__main__':
    service.run(debug=False)

def check_date_format(date_str):
    match = re.search('([0-2][0-9]|[3][0-1]){1}([0][0-9]|[1][0-2]){1}(\d){4}$', date_str)
    if match:
        print(match.group(0))
        return True
    else:
        return False