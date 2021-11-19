from flask import request,make_response
from flask_restx import Resource, Namespace
from bson.objectid import ObjectId

import mongo

mongodb = mongo.MongoHelper()

ContestList = Namespace("contestList", description="API about list of contest")

@ContestList.route("")
class ContestListControl(Resource):
    def get(self):
        print("PresentContestList")
        """
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
            "participant": [],
            "audience": [],
            "mc": [],
            "result": 
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
        contest_state = request.args.get("state")  # 현재는 "present"
        # collection_name
        collection = "contest"

        contest_list = list(mongodb.find(query={"state":contest_state}, collection_name=collection))

        if not contest_list:
            result = make_response({"queryStatus": []}, 200)
            return result
        
        # convert
        for contest in contest_list:
            contest["_id"] = str(contest["_id"])

        result = make_response({"queryStatus": contest_list}, 200)
        return result