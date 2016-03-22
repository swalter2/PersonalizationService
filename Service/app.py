from flask import Flask, jsonify
from database import Database

app = Flask(__name__)
host = 'localhost'
user = 'wikipedia_new'
password = '1234567'
db = 'wikipedia_new'

database = Database(host, user, password, db)


@app.route('/personalization/<int:task_id>', methods=['GET'])
def get_task(task_id):
    results = database.getpersonalizedarticles(int(task_id))

    return jsonify({'Personalisierung': results})


#@app.errorhandler(404)
#def not_found(error):
#    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=False)