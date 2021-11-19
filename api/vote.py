from flask import request,make_response
from flask_restx import Resource, Namespace
from bson.objectid import ObjectId

import mongo

mongodb = mongo.MongoHelper()

Vote = Namespace("vote", description="API about vote")


@Vote.route("")
class VoteControl(Resource):
    def post(self):  # each audience vote
        request_info = request.get_json()
        """
        {
            "contestId": "string"
            "choice": "string"
        }
        """
        # contest_id
        contest_id = request_info["contestId"]
        contest_collection = "contest"
        # choice
        choice = request_info["choice"]

        contest_info = mongodb.find_one({"_id":ObjectId(contest_id)}, collection_name=contest_collection)
        contest_vote_result = contest_info["voteResult"]
        
        if not (choice in contest_vote_result):
            contest_vote_result[choice] = 1
            result = mongodb.update_one({"_id":ObjectId(contest_id)}, collection_name=contest_collection, modify={"$set":{"voteResult": contest_vote_result}})
        
        else:
            result = mongodb.update_one({"_id":ObjectId(contest_id)}, collection_name=contest_collection, modify={"$inc":{"voteResult.{}".format(choice):1}})

        if result.raw_result["n"] == 0:
            return_result = make_response({"queryStatus":"vote fail"}, 500)
            return return_result
        
        return_result = make_response({"queryStatus": "vote success"}, 200)
        return return_result
        

    def get(self):  # check result of vote
        contest_id = request.args.get("contestId")
        contest_collection = "contest"
        contest_info = mongodb.find_one({"_id":ObjectId(contest_id)}, collection_name=contest_collection)
        print(contest_info)
        vote_result = contest_info["voteResult"]

        # 동점은 어떡하지?
        # gold
        gold = max(vote_result, key=vote_result.get)
        del vote_result[gold]

        # silver
        silver = ""
        if vote_result:
            silver = max(vote_result, key=vote_result.get)
            del vote_result[silver]

        # bronze
        bronze = ""
        if vote_result:
            bronze = max(vote_result, key=vote_result.get)

        # gold, silver, bronze 가져오기
        user_collection = "user"
        result_list = []
        if gold:
            gold_info = mongodb.find_one(query={"_id":gold}, collection_name=user_collection)
            del gold_info["password"]
            del gold_info["badge"]
            result_list.append(gold_info)
        
        if silver:
            silver_info = mongodb.find_one(query={"_id":silver}, collection_name=user_collection)
            del silver_info["password"]
            del silver_info["badge"]
            result_list.append(silver_info)

        if bronze:
            bronze_info = mongodb.find_one(query={"_id":bronze}, collection_name=user_collection)
            del bronze_info["password"]
            del bronze_info["badge"]
            result_list.append(bronze_info)

        final_result = {
            "finalResult": result_list
        }

        result = mongodb.update_one(query={"_id":ObjectId(contest_id)}, collection_name=contest_collection, modify={"$set":final_result})
        
        if result.raw_result["n"] == 0:
            return_result = make_response({"queryStatus": "update fail"}, 500)
            return return_result
        
        contest_info = mongodb.find_one(query={"_id":ObjectId(contest_id)}, collection_name=contest_collection)
        contest_info["_id"] = str(contest_info["_id"])
        
        return_result = make_response({"queryStatus": contest_info}, 200)
        return return_result

