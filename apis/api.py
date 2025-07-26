#! /usr/bin/python3
from flask import Flask
from flask_restful import Api,Resource
import sqlalchemy
from .. import models
app=Flask(__name__)
api=Api(app)

students={"tim": {"age":21,"height":"tall"},
          "king": {"age":22, "height":"short"}}

class MainApp(Resource):
    def get(self,student):
        return students[student]
    def post(self,student):
        students[student]={"age":21,"height":"tall"}
        return students[student]
api.add_resource(MainApp,"/Welcome/<string:student>")

if __name__=='__main__':
    app.run(debug=True)
