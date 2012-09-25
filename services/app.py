import json
from flask import Flask, session, redirect, url_for, escape, request
import mydal

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST', 'PUT', 'DELETE'])
def hello(id=None, name=None, address=None, phone=None, email=None):
    if request.method == 'GET':
        thejson = json.dumps(mydal.getcontacts())
        return thejson
    elif request.method == 'POST':
        thejson = json.dumps(mydal.addcontact(name, address, phone, email))
        return thejson
    elif request.method == 'PUT':
        thejson = json.dumps(mydal.changecontact(id, name, address, phone, email))            
        return thejson
    elif request.method == 'DELETE':
        thejson = json.dumps(mydal.delcontact(id))
        return thejson
    else:
        #throw exception
        return json.dumps({"error": "unknown http type"})
    
if __name__ == "__main__":
    app.run(port=2000)
