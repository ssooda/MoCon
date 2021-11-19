from flask import Flask, request
from flask_restx import Api
from utils import APP_SECRET_KEY
import mongo

from api.contest import Contest, Register
from api.list import ContestList
from api.user import User
from api.vote import Vote

app = Flask(__name__)

app.config.update(
    DEBUG = True,
    SECRET_KEY = APP_SECRET_KEY
)

api = Api(app)

api.add_namespace(Contest, "/contest")
api.add_namespace(Register, "/register")
api.add_namespace(ContestList, "/contestlist")
api.add_namespace(User, "/user")
api.add_namespace(Vote, "/vote")

@app.after_request 
def close_mongo(response):  # close Mongodb after api reqeust end
    mongodb = mongo.MongoHelper()
    result = mongodb.close()
    print(result)
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")