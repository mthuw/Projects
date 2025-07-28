import os
import json
import paho.mqtt.client as mqtt
import mysql.connector
from pymongo import MongoClient
from py2neo import GraphDatabase

from flask import Flask
app = Flask(__name__)

#Load config from env
MQTT_Broker = os.getenv("MQTT_BROKER", "mosquitto")
MONGO_URI = os.getenv("MONGO_HOST", "mongodb")
mysql_conn = mysql.connector.connect(
    host = os.getenv("MYSQL_HOST", "mysql"),
    user = os.getenv("MYSQL_USER", "iotuser"),
    password = os.getenv("MYSQL_PASSWORD", "iotpass"),
    database = os.getenv("MYSQL_DB", "iotdb")
)
NEO4J_URI = os.getenv("NEO4J_URI","bolt://neo4j:7687")
NEO4J_AUTH = (os.getenv("NEO4J_USER","neo4j"), os.getenv("NEO4J_PASSWORD", "testpass"))

#Initialize clients
mongo = MongoClient(MONGO_URI).wearables
neo4j = GraphDatabase.driver(NEO4J_URI, auth=NEO4J_AUTH)

with mysql_conn.cursor() as cur:
    cur.execute("""
CREATE TABLE IF NOT EXISTS metrics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    device_id VARCHAR(100),
    metric VARCHAR(100),
    value FLOAT,
    time DATETIME
    )
""")
mysql_conn.commit()

def store_in_mongo(payload):
    mongo.raw.insert_one(payload)
def store_in_mysql(payload):
    with mysql_conn.cursor() as cur:
        cur.execute(
            "INSERT INTO metrics (devide_id, metric, value, time) VALUE(%s,%s,%s,%s)",
            (payload['device_id'], payload['metric'], payload['value'], payload['time'])
        )
    mysql_conn.commit()
def store_in_neo4j(payload):
    with neo4j.session() as session:
        session.run(
            """
            MERGE (d:Device {id: $device_id})
            CREATE (m:Measurement {metric: $metric, $value: value, $time: time})
            CREATE (d)-[:RECORDED]->(m)
            """,
            payload
        )    

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        store_in_mongo(data)
        store_in_mysql(data)
        store_in_neo4j(data)
        print(f"Store {data}")
    except Exception as e:
        print(e)

def main():
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(MQTT_Broker, 1883)
    client.subscribe("wearables/+/metrics")
    client.loop_forever()
if __name__ == "__main__":
    main()
