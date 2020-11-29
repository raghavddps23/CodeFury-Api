from flask import Flask,request
from flask import jsonify
import firebase_admin
from firebase_admin import credentials,firestore

from flask_cors import CORS,cross_origin

import json
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

cred = credentials.Certificate("serviceAccount.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
product_ref = db.collection('products')

@app.route('/')
def index():
    response =  jsonify("Hello World")
    return response

contractors = db.collection('contractors')
@app.route('/signup',methods=['POST'])
@cross_origin()
def sign_up():
    data = request.json
    print(data)
    try:
        contractorEmail = data['email']
        a = contractors.document(contractorEmail).get().to_dict()
        if a != None:
            return {"success":False,"details":"Email already exists"}, 400
        contractors.document(contractorEmail).set(data)
        response = jsonify({"success":True})
        return response
    except Exception as e:
        return f"An Error Occured: {e}",404
    

@app.route('/login',methods=['GET','POST'])
@cross_origin()
def login():
    data = request.json
    try:
        email = data['email_id']
        contractor = contractors.document(email).get().to_dict()
        print(contractor)
        if contractor == None:
            return {"success":False,"details":"Vendor does not exist"}, 404
        else:
            actualPassword = contractor['password']
            sentPassword = data['pass']
            if actualPassword == sentPassword:
                response =  jsonify({"success":True,"email":contractor['email'],"address":contractor['address'],"name":contractor['username']})
                return response
            else:
                response =  jsonify({"success":False, "details":"Invalid password"})
                return response
    except Exception as e:
        return f"An Error Occured: {e}"


@app.route('/getAllLabourers',methods=['GET'])
@cross_origin()
def getAllLabourers():
    args = request.args
    labourers = db.collection('labourers')
    
    try:
        all_labourers = [labourer.to_dict() for labourer in labourers.stream()]
        response = jsonify(all_labourers)
        return response , 200
    except Exception as e:
        return f"An Error Occured: {e}", 500

@app.route('/getALabourer')
@cross_origin()
def specificOrder():
    labourerId = request.args['labourerId']
    labourers = db.collection('labourers')
    try:
        labourer = labourers.document(labourerId).get().to_dict()
        response = jsonify(labourer)
        return response, 200
    except Exception as e:
        return f"An Error Occured: {e}"

workDict = {'1':"Plumbing",'2':"Carpenter",'3':"Daily Wage Worker",'4':"House hold worker"}

@app.route('/getPlumbers',methods=['GET'])
def getPlumbers():
    args = request.args
    labourers = db.collection('labourers')
    
    try:
        all_labourers = [labourer.to_dict() for labourer in labourers.stream() if labourer.to_dict()['workId'] == 1]
        response = jsonify(all_labourers)
        return response , 200
    except Exception as e:
        return f"An Error Occured: {e}", 500


@app.route('/getCarpenters',methods=['GET'])
def getCarpenters():
    args = request.args
    labourers = db.collection('labourers')
    
    try:
        all_labourers = [labourer.to_dict() for labourer in labourers.stream() if labourer.to_dict()['workId'] == 2]
        response = jsonify(all_labourers)
        return response , 200
    except Exception as e:
        return f"An Error Occured: {e}", 500

@app.route('/getDailyWage',methods=['GET'])
def getDailyWage():
    args = request.args
    labourers = db.collection('labourers')
    
    try:
        all_labourers = [labourer.to_dict() for labourer in labourers.stream() if labourer.to_dict()['workId'] == 3]
        response = jsonify(all_labourers)
        return response , 200
    except Exception as e:
        return f"An Error Occured: {e}", 500

@app.route('/getHomeWorkers',methods=['GET'])
def getHomeWorkers():
    args = request.args
    labourers = db.collection('labourers')
    
    try:
        all_labourers = [labourer.to_dict() for labourer in labourers.stream() if labourer.to_dict()['workId'] == 4]
        response = jsonify(all_labourers)
        return response , 200
    except Exception as e:
        return f"An Error Occured: {e}", 500

@app.route('/getWorkersInCity',methods=['GET'])
def getWorkersInCity():
    city = request.args['city'].lower().strip()
    labourers = db.collection('labourers')
    try:
        all_labourers = [labourer.to_dict() for labourer in labourers.stream() if labourer.to_dict()['place'] == city]
        response = jsonify(all_labourers)
        return response , 200
    except Exception as e:
        return f"An Error Occured: {e}", 500


if __name__ == '__main__':
    app.run(debug=True,port=3000)