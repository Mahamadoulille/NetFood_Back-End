from urllib import request, response
from flask import Flask, Response,request
import pymongo
import json
from bson.objectid import ObjectId
app = Flask(__name__)

try:
    mongo = pymongo.MongoClient(
    host="mongodb", 
    port=27017,
    username='root', 
    password='pass',
    authSource="admin", 
    serverSelectionTimeoutMS = 1000
    )
    db =mongo.netfood
    mongo.server_info() # trigger exception if cannot connect to bdd
except:
    print("ERROR - Cannot connect to BDD")

##############
@app.route("/plats", methods=["GET"])
def get_some_plats():
    try:
        data = list(db.plats.find())
        for plat in data:
            plat["_id"] = str(plat["_id"])
        return Response(
            response= json.dumps(data),
            status=500,
            mimetype="application/json"
        )
    except Exception as ex:
        print(ex)
        return Response(response= json.dumps({"message":"cannot read plats", "id":f"{dbResponse.inserted_id}"}),status=200,mimetype="application/json")

##############
@app.route("/plats", methods=["POST"])
def create_plat():
    try:
        plat = {"nom__plat" : request.form["nom__plat"],
        "theme_plat" : request.form["theme_plat"],
        "ingredient_plat" : request.form["ingredient_plat"],
        "illustration_plat" : request.form["illustration_plat"],
        }
        dbResponse = db.plats.insert_one(plat)
        print(db.plats.insert_id)
        # for attr in dir(dbResponse):
        #     print(attr)
        return Response(
            response= json.dumps({"message":"plat created", "id":f"{dbResponse.inserted_id}"}),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print("*************")
        print(ex)
        print("*************")


############################
@app.route("/plats/<id>", methods=["PATCH"])
def update_plat(id):
    try:
        dbResponse = db.plats.update_many(
            {"_id":ObjectId(id)},
            {"$set":{"nom__plat":request.form["nom__plat"],"theme_plat":request.form["theme_plat"],
            "ingredient_plat":request.form["ingredient_plat"],"illustration_plat":request.form["illustration_plat"]}}
        )
        # for attr in dir(dbResponse):
        #     print(f"*****{attr}*****")
        if dbResponse.modified_count == 1  :      
            return Response(
                response= json.dumps({
                    "message":"plat updated"}),
                status=200,
                mimetype="application/json"
            )
        return Response(
            response= json.dumps({
                "message":"nothing to update"}),
            status=200,
            mimetype="application/json"
        ) 
    except Exception as ex:
            print("*************")
            print(ex)
            print("*************") 
            return Response(
            response= json.dumps({"message":"sorry cannot update plat", "id":f"{dbResponse.inserted_id}"}),
            status=500,
            mimetype="application/json"
        )   
############################
@app.route("/plats/<id>", methods=["DELETE"])
def delete_plat(id):
    try:
        dbResponse = db.plats.delete_one({"_id":ObjectId(id)})
        # for attr in dir(dbResponse):
        #      print(f"*****{attr}*****")
        if dbResponse.deleted_count == 1:
            return Response(response= json.dumps({"message":"plat deleted", "id":f"{id}"}),status=200,mimetype="application/json")
        return Response(response= json.dumps({"message":"plat not found", "id":f"{id}"}),status=200,mimetype="application/json")
            
    except Exception as ex:
        print("*************")
        print(ex)
        print("*************") 
        return Response(
        response= json.dumps({"message":"sorry cannot delete plat"}),
        status=500,
        mimetype="application/json"
    ) 
############################

if __name__ == "__main__":
    app.run(port=80, debug=True)
