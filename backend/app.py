import os
import json
import sqlalchemy
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Text
from sqlalchemy import DateTime
from datetime import datetime
from sqlalchemy_utils import database_exists, create_database

# app.config["DEBUG"] = True

# Define the MariaDB engine using MariaDB Connector/Python
url = "mariadb+mariadbconnector://" + os.environ['MARIADB_ROOT_USERNAME'] + ":" + os.environ['MARIADB_ROOT_PASSWORD'] + "@" + os.environ['MARIADB_DATABASE'] + "/pastebin"

if not database_exists(url):
    create_database(url)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = url
db = SQLAlchemy(app)


class Pastebin(db.Model):
    __tablename__ = 'pastebin'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(length=100))
    content = db.Column(Text)
    created_at = db.Column(DateTime)


db.create_all()

def add_new_paste(title: str, content: str, created_at: DateTime):
    new_paste = Pastebin(title=title, content=content, created_at=created_at)
    db.session.add(new_paste)
    db.session.commit()
    return str(new_paste.id)


def get_latest_hundred():
    latest_hundred = Pastebin.query.order_by(Pastebin.created_at.desc()).limit(100)
    data_list = []
    for the_paste in latest_hundred:
        data_list.append({"title": the_paste.title,
                          "content": the_paste.content,
                          "createdAt": str(the_paste.created_at)})
    return data_list


@app.route("/api/paste", methods=['POST'])
def paste():
    try:
        title = request.json["title"]
        content = request.json["content"]
        date_time = datetime.utcnow()
        returned_id = add_new_paste(title,
                                    content,
                                    date_time.replace(microsecond=0))
        response = {"id": returned_id}
    except:
        response = {"error": "failed to create a paste due to some missing data"}
    if "id" in response:
        return jsonify(response), 200
    else:
        return jsonify(response), 400


@app.route("/api/<ID>", methods=['GET'])
def search_from_id(ID):
    response = Pastebin.query.get(ID)
    if response is None:
        return jsonify({}), 404
    else:
        return jsonify({"title": response.title,
                        "content": response.content,
                        "createdAt": str(response.created_at)}), 200


@app.route("/api/recents", methods=['POST'])
def recents():
    return json.dumps(get_latest_hundred())

app.run()