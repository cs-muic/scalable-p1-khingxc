import json
import sqlalchemy
from flask import Flask, request, jsonify
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Text
from sqlalchemy import DateTime
from datetime import datetime

app = Flask(__name__)
app.config["DEBUG"] = True

# Define the MariaDB engine using MariaDB Connector/Python
engine = sqlalchemy.create_engine("mariadb+mariadbconnector://root:hardpass@127.0.0.1:3307/pastebin")

Base = declarative_base()


class Pastebin(Base):
    __tablename__ = 'pastebin'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    title = sqlalchemy.Column(sqlalchemy.String(length=100))
    content = sqlalchemy.Column(Text)
    created_at = sqlalchemy.Column(DateTime)


Base.metadata.create_all(engine)


# Create a session
Session = sqlalchemy.orm.sessionmaker()
Session.configure(bind=engine)
session = Session()


def add_new_paste(title: str, content: str, created_at: DateTime):
    new_paste = Pastebin(title, content, created_at)
    session.add(new_paste)
    session.commit()
    return new_paste.id


def get_latest_hundred():
    latest_hundred = session.query(Pastebin).order_by(Pastebin.created_at.desc()).limit(100)
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
        date_time = (datetime.utcnow()).replace(microsecond=0)
        returned_id = add_new_paste(title,
                                    content,
                                    date_time)
        response = {"id": str(returned_id)}
    except:
        response = {"error": "failed to create a paste due to some missing data"}
    if "id" in response:
        return jsonify(response), 200
    else:
        return jsonify(response), 400


@app.route("/api/<ID>", methods=['GET'])
def search_from_id(ID):
    response = session.query(Pastebin).get(ID)
    if response is None:
        return jsonify({}), 404
    else:
        return jsonify({"title": response.title,
                        "content": response.content,
                        "createdAt": str(response.created_at)}), 200


@app.route("/api/recents", methods=['POST'])
def recents():
    return json.dumps(get_latest_hundred())

# app.run()
