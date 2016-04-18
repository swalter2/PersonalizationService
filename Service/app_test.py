# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request


app_test = Flask(__name__)


# curl -i http://localhost:5000/personalization/?personid=1&interests=Kunst
@app_test.route('/', methods=['GET'])
def get_articles():
    print("a:"+str(request.args.get('a')))
    print("b:"+str(request.args.get('b')))

    return jsonify({'Works': 'bla'})

if __name__ == '__main__':
    app_test.run(debug=True)





## -*- coding: utf-8 -*-
#from flask import Flask, jsonify, request
#from webargs import fields
#from webargs.flaskparser import use_args
#
#
#app_test = Flask(__name__)
#
#hello_args = {
#    'a': fields.Str(required=True),
#    'b': fields.Str(required=True)
#}
#
## curl -i http://localhost:5000/personalization/?personid=1&interests=Kunst
##curl http://localhost:5000/\?a\='1'\&b\='2'
#@app_test.route('/', methods=['GET'])
#@use_args(hello_args)
#def get_articles(args):
#    print("a:"+str(args['a']))
#    print("b:"+str(args['b']))
#
#    return jsonify({'Works': 'bla'})
#
#if __name__ == '__main__':
#    app_test.run(debug=True)