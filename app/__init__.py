from flask import Flask, Blueprint
from app import modules
from flask import url_for
from flask_cors import CORS
import pymongo

app = Flask(__name__)
app.config.from_object("config")
CORS(app)

try:
    uname = app.config["DB_USERNAME"]
    pw = app.config["DB_PASSWORD"]
    cluster_code = app.config["DB_CLUSTER_CODE"]
    conn = pymongo.MongoClient(
        f"mongodb+srv://{uname}:{pw}{cluster_code}.mongodb.net/?retryWrites=true&w=majority"
    )
    db = conn.portal
except Exception as e:
    print(e)
    print("An error has occurred while trying to connect to the database.")

module = Blueprint("/", __name__)


@module.route("/")
def ping():
    return "Root"


modules.register()
