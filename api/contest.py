from flask import request,make_response
from flask_restx import Resource, Namespace
from bson.objectid import ObjectId

import mongo

mongodb = mongo.MongoHelper()

Contest = Namespace("contest", description="API about contest")

@Contest.route("")
class ContestControl(Resource):
    def post(self):
        print("Contest")
        request_info = request.get_json()
        """
        # request
        {
            "host": string,
            "name": string,
            "date": string,
            "type": string,
            "state": string
        }
        # return
        {
            "_id": string,
            "host":
                {
                    "_id": string,
                    "nickname": string,
                    "profileImage": 
                        [
                            {
                                "key": null,
                                "body": string
                            }
                        ]
                },
            "name": string,
            "date": string,
            "type": string,
            "state": string,
            "likes": [],
            "participant": [],
            "audience": [],
            "mc": [],
            "voteResult":
                {
                    "user_id": integer
                }
            "finalResult": 
                [ # 순서에 따라 1,2,3 등
                    {
                        "_id": string,
                        "nickname": string,
                        "profileImage": 
                            {
                                "key": null,
                                "body": string
                            }
                    },
                    {
                        "_id": string,
                        "nickname": string,
                        "profileImage":
                            {
                                "key": null,
                                "body": string
                            }
                    }
                ]
        }
        """
        # collection_name
        collection = "user"

        # host user information
        host = request_info["host"]
        user_info = mongodb.find_one(query={"_id":host}, collection_name=collection)
        
        del user_info["password"]
        del user_info["badge"]
        
        # process profileImage

        request_info["host"] = user_info

        # add likes, participant, audience, mc
        request_info["likes"] = []
        request_info["participant"] = []
        request_info["audience"] = []
        request_info["mc"] = []
        request_info["voteResult"] = {}
        request_info["finalResult"] = []

        # collection_name
        collection = "contest"

        # save data 
        contest_id = mongodb.insert_one(data=request_info, collection_name=collection)
        
        if not contest_id:
            result = make_response({"queryStatus": "save fail"}, 500)
            return result
        
        # get data for return
        contest = mongodb.find_one(query={"_id":ObjectId(contest_id)}, collection_name=collection)

        if not contest:
            result = make_response({"queryStatus": "get fail"}, 404)
            return result


        # convert _id
        contest["_id"] = str(contest["_id"])

        result = make_response({"queryStatus": contest}, 200)
        return result

    def get(self):
        contest_id = request.args.get("contestId")

        # collection_name
        collection = "contest"

        contest = mongodb.find_one(query={"_id":ObjectId(contest_id)}, collection_name=collection)

        if not contest:
            result = make_response({"queryStatus": "get fail"}, 404)
            return result
        
        # convert
        contest["_id"] = str(contest["_id"])

        result = make_response({"queryStatus": contest}, 200)
        return result


Register = Namespace("register", description="API about register")

@Register.route("/<string:register_type>")
class RegisterControl(Resource):
    def post(self, register_type):
        request_info = request.get_json()
        """
        {
            "contestId": "string", //contest_id
            "user": "string" // user_id
        }
        """
        # contest_id
        contest_id = request_info["contestId"]
        contest_collection = "contest"
        # user_id
        user_id = request_info["user"]
        user_collection = "user"

        # get user_info
        user_info = mongodb.find_one(query={"_id":user_id}, collection_name=user_collection)
        del user_info["password"]
        del user_info["badge"]
        
        # Revise user_info

        # Revise contest information
        result = mongodb.update_one(query={"_id":ObjectId(contest_id)}, collection_name=contest_collection, modify={"$addToSet": {register_type:user_info}})

        if result.raw_result["n"] ==0:
            return_result = make_response({"queryStatus": "register fail"}, 500)
            return return_result
        
        return_result = make_response({"queryStatus": "register success"}, 200)
        return return_result
    
    def delete(self, register_type):
        request_info = request.get_json()
        """
        {
            "contestId": "string", //contest_id
            "user": "string" // user_id
        }
        """
        # contest_id
        contest_id = request_info["contestId"]
        contest_collection = "contest"
        # user_id
        user_id = request_info["user"]
        user_collection = "user"

        # get user_info
        user_info = mongodb.find_one(query={"_id":user_id}, collection_name=user_collection)
        del user_info["password"]
        del user_info["badge"]
        
        # Revise user_info

        # Revise contest information
        result = mongodb.update_one(query={"_id":ObjectId(contest_id)}, collection_name=contest_collection, modify={"$pull": {register_type:user_info}})

        if result.raw_result["n"] ==0:
            return_result = make_response({"queryStatus": "cancle fail"}, 500)
            return return_result
        
        return_result = make_response({"queryStatus": "cancle success"}, 200)
        return return_result



