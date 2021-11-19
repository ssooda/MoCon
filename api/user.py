from flask import request,make_response
from flask_restx import Resource, Namespace
from bson.objectid import ObjectId
from pymongo.message import query

import mongo

mongodb = mongo.MongoHelper()

User = Namespace("user", description="API about user")
@User.route("")
class UserControl(Resource):
    def post(self):
        print("User")
        request_info = request.get_json()

        """
        # request
        {
            "_id": string,
            "nickname": string,
            "password": string,
            "profileImage": 
                [
                    {
                        "key": null,
                        "body": string
                    }
                ]
        }
        #  return
        {
            "_id": string,
            "nickname": string,
            "password": string,
            "profileImage": 
                [
                    {
                        "key": null,
                        "body": string
                    }
                ],
            "badge":
                {
                    "gold": [],
                    "silver": [],
                    "bronze": [],
                    "participant": [],
                    "audience": [],
                    "mc": []
                }
        }
        """
        # save profileImage


        # processing reqeust_info
        request_info["badge"] = {
            "gold": [],
            "silver": [],
            "bronze": [],
            "participant": [],
            "audience": [],
            "mc": []
        }
        print(request_info)

        # collection
        collection = "user" 

        # save data
        user_id = mongodb.insert_one(data=request_info, collection_name=collection)

        if not user_id:
            result = make_response({"queryStatus": "save fail"}, 500)
            return result

        # get data for return
        user = mongodb.find_one(query={"_id":user_id}, collection_name=collection)

        if not user:
            result = make_response({"queryStatus": "get fail"}, 404)
            return result

        # delete password
        del user["password"]
        result = make_response({"queryStatus": user}, 200)
        return result
    
    
    def get(self):
        user_id = request.args.get("id")

        # collection_name
        collection = "user"

        user = mongodb.find_one(query={"_id":user_id}, collection_name=collection)

        if not user:
            result = make_response({"queryStatus": "get fail"}, 404)
            return result
        
        result = make_response({"queryStatus": user}, 200)
        return result