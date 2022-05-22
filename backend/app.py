import sqlalchemy
from flask import Flask
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Text
from sqlalchemy import DateTime

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
   createdAt = sqlalchemy.Column(DateTime)

Base.metadata.create_all(engine)

# Create a session
Session = sqlalchemy.orm.sessionmaker()
Session.configure(bind=engine)
session = Session()

# app.run()