from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort
from flask_mysqldb import MySQL


import json

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('nama', required=True, dest='sth')
parser.add_argument('uploadDate', type=int, required=False)

with open ('dataUser.json','r') as f:
    dataUser=json.load(f)

def write_changes_to_file():
    global dataUser

    with open('dataUser.json','w') as f:
        json.dump(dataUser, f)

write_changes_to_file()

 
class Data(Resource):
    def get(self, data_id):
        if data_id == "all":
            return dataUser
        if data_id not in dataUser:
            abort(404, message="data {data_id} not found")
        return dataUser[data_id]

    def put(self, data_id):
        args = request.args
        dataUser[data_id] = {'nama': args["nama"],
                             'uploadDate': args["uploadDate"]}
        write_changes_to_file()
        return {data_id: dataUser[data_id]}, 201

    def delete(self, data_id):
        if data_id not in dataUser:
            abort(404, message=f"data {data_id} not found")
        del dataUser[data_id]
        write_changes_to_file()
        return "", 204


class DataInput(Resource):
    def get(self):
        return dataUser

    def post(self):
        args = request.args
        data_id = max(int(DU.lstrip('dataUser')) for DU in dataUser.keys())+1
        data_id = f"data{data_id}"
        dataUser[data_id] = {'nama': args["nama"],
                             'uploadDate': args["uploadDate"]}
        write_changes_to_file()
        return dataUser[data_id], 201


api.add_resource(Data, "/dataUser/<data_id>")
api.add_resource(DataInput, '/dataUser')

if __name__ == '__main__':
    app.run(debug=True)
