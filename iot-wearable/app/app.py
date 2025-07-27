import os
import json
import paho.mqtt.client as mqtt
import mysql.connector
from pymongo import MongoClient
from py2neo import GraphDatabase

from flask import Flask
app = Flask(__name__)

mysql_conn = mysql.connector.connect(
    host = os.getenv("MYSQL_HOST", "mysql"),
    user = os.getenv("MYSQL_USER", "iotuser"),
    password = os.getenv("MYSQL_PASSWORD", "iotpass"),
    database = os.getenv("MYSQL_DB", "iotdb")
)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
