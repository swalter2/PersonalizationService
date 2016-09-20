# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request
from database import Database
from learning import Learning
import sys
import datetime

service = Flask(__name__)

ONLY_PERSONS = 0
WITHOUT_PERSONS = 1
ALL_ARTICLES = 2

host = 'localhost'
user = 'wikipedia_new'
password = '1234567'
db = 'wikipedia_new'

today = datetime.datetime.now()
datum = today.strftime("%d%m%Y")



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

#curl http://localhost:5000/service/\?personid\='1'
@service.route('/user', methods=['POST'])
def update_user():
    if request.headers['Content-Type'] == 'application/json':
        json_input = request.json
        print(json_input)
        try:
            person_id = 0
            database = Database(host, user, password, db)
            if 'personid' in json_input:
                person_id = json_input['personid']
                result = database.update_user(json_input,person_id)
                if result == -1:
                    return "500 - error in json input"
                else:
                    learning = Learning(host, user, password, db, datum)
                    learning.single_learn(person_id)
                    print("done with user update with id ",person_id)
                    sys.stdout.flush()
            else:
                person_id = database.add_user(json_input)
                if person_id == -1:
                    return "500 - error in json input"
                else:
                    learning = Learning(host, user, password, db, datum)
                    learning.single_learn(person_id)
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
        #print("Input:", json_input)
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



if __name__ == '__main__':
    service.run(debug=False)