from flask import Flask
import MeCab
from flask_restful import Api
from flask_restful import Resource
from flask_restful import reqparse


class tagger(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("string", required=True, type=str)
            args = parser.parse_args()
            result = mor.parse(args["string"])
            return {"result" : result}
        except Exception as err:
            return str(err)

class taggerlist(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("string", required=True, action="append")
            args=parser.parse_args()
            result=[]
            for each in args["string"]:
                result.append(mor.parse(each))
            return {"result":result}
        except Exception as err:
            return str(err)


if __name__ == '__main__':
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(tagger, "/tagger")
    api.add_resource(taggerlist, "/taggerlist")
    mor = MeCab.Tagger()
    app.run(host="0.0.0.0", port=5001, debug=True)
